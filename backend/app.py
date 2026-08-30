import hmac
import subprocess
import threading
import time
from collections import defaultdict, deque
from datetime import date as date_type
from datetime import datetime
from functools import wraps
from pathlib import Path

from flask import Flask, Response, g, jsonify, request, session
from flask_cors import CORS
from flask_socketio import SocketIO
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from config import Config
from models import Log, Traffic, User, db
from video_stream import SharedVideoStream


app = Flask(__name__)
app.config.from_object(Config)

CORS(
    app,
    resources={r"/*": {"origins": app.config["CORS_ORIGINS"]}},
    supports_credentials=True,
)
db.init_app(app)
socketio = SocketIO(
    app,
    cors_allowed_origins=app.config["CORS_ORIGINS"],
    async_mode="threading",
)
video_stream = SharedVideoStream(
    app.config["RTSP_URL"],
    frame_rate=app.config["VIDEO_FRAME_RATE"],
    jpeg_quality=app.config["VIDEO_JPEG_QUALITY"],
    open_timeout_ms=app.config["VIDEO_OPEN_TIMEOUT_MS"],
    read_timeout_ms=app.config["VIDEO_READ_TIMEOUT_MS"],
    reconnect_initial=app.config["VIDEO_RECONNECT_INITIAL"],
    reconnect_max=app.config["VIDEO_RECONNECT_MAX"],
)

_background_task = None
_background_task_lock = threading.Lock()
_connected_clients = set()
_external_processes = []
_login_attempts = defaultdict(deque)
_login_attempts_lock = threading.Lock()


def ensure_database():
    Path(app.config["DATABASE_PATH"]).parent.mkdir(parents=True, exist_ok=True)
    with app.app_context():
        db.create_all()


def _start_process(command, service_name):
    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except OSError as exc:
        app.logger.error("无法启动%s：%s", service_name, exc)
        return None

    _external_processes.append(process)
    app.logger.info("已启动%s，PID=%s", service_name, process.pid)
    return process


def start_rtsp_server():
    executable = Path(app.config["MEDIAMTX_PATH"])
    if not executable.is_file():
        app.logger.warning("未启动 MediaMTX，文件不存在：%s", executable)
        return None
    return _start_process([str(executable)], "MediaMTX")


def start_detect():
    conda_executable = Path(app.config["CONDA_EXE"])
    inference_script = Path(app.config["PADDLE_INFER_SCRIPT"])
    model_directory = Path(app.config["PADDLE_MODEL_DIR"])

    missing = [
        str(path)
        for path in (conda_executable, inference_script, model_directory)
        if not path.exists()
    ]
    if missing:
        app.logger.warning("未启动 PaddleDetection，以下路径不存在：%s", ", ".join(missing))
        return None

    command = [
        str(conda_executable),
        "run",
        "-n",
        app.config["PADDLE_ENV_NAME"],
        "python",
        str(inference_script),
        f"--model_dir={model_directory}",
        f"--camera_id={app.config['CAMERA_ID']}",
        f"--device={app.config['PADDLE_DEVICE']}",
        "--pushurl",
        app.config["PADDLE_PUSH_URL"],
    ]
    return _start_process(command, "PaddleDetection")


def _latest_data():
    logs = Log.query.order_by(Log.id.desc()).limit(50).all()
    traffic = Traffic.query.order_by(Traffic.id.desc()).limit(20).all()
    return [item.to_dict() for item in logs], [item.to_dict() for item in traffic]


def _request_json():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise ValueError("请求体必须是 JSON 对象")
    return data


def _text_value(data, field, *, required=False, default="", max_length=80):
    value = data.get(field, default)
    if value is None:
        value = default
    value = str(value).strip()
    if required and not value:
        raise ValueError(f"缺少字段：{field}")
    if len(value) > max_length:
        raise ValueError(f"字段 {field} 不能超过 {max_length} 个字符")
    return value


def _non_negative_integer(data, field):
    try:
        value = int(data.get(field, 0))
    except (TypeError, ValueError) as exc:
        raise ValueError(f"字段 {field} 必须是整数") from exc
    if value < 0:
        raise ValueError(f"字段 {field} 不能小于 0")
    return value


def _login_key(username):
    return f"{request.remote_addr or 'unknown'}:{username.casefold()}"


def _login_retry_after(key):
    now = time.monotonic()
    window = app.config["LOGIN_WINDOW_SECONDS"]
    maximum = app.config["LOGIN_MAX_ATTEMPTS"]
    with _login_attempts_lock:
        attempts = _login_attempts[key]
        while attempts and now - attempts[0] >= window:
            attempts.popleft()
        if len(attempts) < maximum:
            return 0
        return max(1, int(window - (now - attempts[0])))


def _record_login_failure(key):
    with _login_attempts_lock:
        _login_attempts[key].append(time.monotonic())


def _clear_login_failures(key):
    with _login_attempts_lock:
        _login_attempts.pop(key, None)


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        user_id = session.get("user_id")
        user = db.session.get(User, user_id) if user_id is not None else None
        if user is None:
            session.clear()
            return jsonify({"ok": False, "text": "请先登录"}), 401
        g.current_user = user
        return view(*args, **kwargs)

    return wrapped


def require_ingest_auth(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        configured_token = app.config["INGEST_API_TOKEN"]
        if not configured_token:
            return jsonify({"ok": False, "text": "服务端尚未配置数据写入 Token"}), 503

        provided_token = request.headers.get("X-API-Token", "")
        if not hmac.compare_digest(provided_token, configured_token):
            return jsonify({"ok": False, "text": "无权写入检测数据"}), 401
        return view(*args, **kwargs)

    return wrapped


def _broadcast_change(event_name, payload):
    try:
        socketio.emit(event_name, payload)
    except Exception:
        app.logger.exception("Socket.IO 增量事件推送失败：%s", event_name)

    try:
        socketio.emit("data_update", _latest_data())
    except Exception:
        app.logger.exception("Socket.IO 兼容快照推送失败")


@app.get("/")
def index():
    return jsonify(
        {
            "name": "helmet-flask",
            "ok": True,
            "endpoints": [
                "/health",
                "/login",
                "/logout",
                "/api/me",
                "/video_feed",
                "/api/data",
                "/api/logs",
                "/api/traffic",
            ],
        }
    )


@app.get("/health")
def health():
    try:
        db.session.execute(text("SELECT 1"))
    except Exception:
        app.logger.exception("数据库健康检查失败")
        return jsonify({"ok": False, "database": "error"}), 503
    return jsonify(
        {
            "ok": True,
            "database": "sqlite",
            "video": video_stream.status(),
        }
    )


@app.get("/video_feed")
@login_required
def video_feed():
    return Response(
        video_stream.generate(),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


@app.post("/login")
def login():
    try:
        data = _request_json()
        username = _text_value(data, "username", required=True)
        password = _text_value(data, "password", required=True, max_length=256)
        key = _login_key(username)
        retry_after = _login_retry_after(key)
        if retry_after:
            return (
                jsonify(
                    {
                        "ok": False,
                        "text": "登录失败次数过多，请稍后重试",
                        "retry_after": retry_after,
                    }
                ),
                429,
            )

        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            _record_login_failure(key)
            return jsonify({"ok": False, "text": "用户名或密码错误"}), 401

        _clear_login_failures(key)
        session.clear()
        session["user_id"] = user.id
        session.permanent = True
        return jsonify({"ok": True, "text": user.to_dict()})
    except ValueError as exc:
        return jsonify({"ok": False, "text": str(exc)}), 400
    except Exception:
        app.logger.exception("登录接口异常")
        return jsonify({"ok": False, "text": "登录服务暂时不可用"}), 500


@app.post("/logout")
def logout():
    session.clear()
    return jsonify({"ok": True})


@app.get("/api/me")
@login_required
def current_user():
    return jsonify({"ok": True, "text": g.current_user.to_dict()})


@app.get("/api/data")
@login_required
def get_data():
    logs, traffic = _latest_data()
    return jsonify({"ok": True, "logs": logs, "traffic": traffic})


@app.post("/api/logs")
@require_ingest_auth
def create_log():
    try:
        data = _request_json()
        event_id = _text_value(data, "event_id", required=True, max_length=64)
        existing = Log.query.filter_by(event_id=event_id).first()
        if existing:
            return jsonify({"ok": True, "duplicate": True, "text": existing.to_dict()}), 200

        item = Log(
            event_id=event_id,
            type=_text_value(data, "type", required=True),
            time=_text_value(
                data,
                "time",
                default=datetime.now().astimezone().isoformat(timespec="seconds"),
            ),
            camera=_text_value(data, "camera"),
            score=_text_value(data, "score"),
            title=_text_value(data, "title"),
            location=_text_value(data, "location"),
            img=_text_value(data, "img", max_length=512),
        )
        db.session.add(item)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            existing = Log.query.filter_by(event_id=event_id).first()
            if existing:
                return (
                    jsonify({"ok": True, "duplicate": True, "text": existing.to_dict()}),
                    200,
                )
            raise

        result = item.to_dict()
        _broadcast_change("log_created", result)
        return jsonify({"ok": True, "duplicate": False, "text": result}), 201
    except ValueError as exc:
        return jsonify({"ok": False, "text": str(exc)}), 400
    except Exception:
        db.session.rollback()
        app.logger.exception("写入检测日志失败")
        return jsonify({"ok": False, "text": "检测日志写入失败"}), 500


@app.post("/api/traffic")
@require_ingest_auth
def upsert_traffic():
    try:
        data = _request_json()
        date = _text_value(data, "date", required=True)
        try:
            date_type.fromisoformat(date)
        except ValueError as exc:
            raise ValueError("字段 date 必须使用 YYYY-MM-DD 格式") from exc

        total = _non_negative_integer(data, "total")
        ele = _non_negative_integer(data, "ele")
        helmet = _non_negative_integer(data, "helmet")
        no_helmet = _non_negative_integer(data, "noHelmet")
        if ele > total:
            raise ValueError("字段 ele 不能大于 total")
        if helmet + no_helmet > ele:
            raise ValueError("helmet 与 noHelmet 之和不能大于 ele")

        item = Traffic.query.filter_by(date=date).first()
        created = item is None
        if created:
            item = Traffic(date=date)
            db.session.add(item)

        item.total = total
        item.ele = ele
        item.helmet = helmet
        item.noHelmet = no_helmet
        db.session.commit()

        result = item.to_dict()
        _broadcast_change("traffic_updated", result)
        return jsonify({"ok": True, "text": result}), 201 if created else 200
    except ValueError as exc:
        return jsonify({"ok": False, "text": str(exc)}), 400
    except Exception:
        db.session.rollback()
        app.logger.exception("写入交通统计失败")
        return jsonify({"ok": False, "text": "交通统计写入失败"}), 500


@socketio.on("connect")
def handle_connect(_auth=None):
    global _background_task
    user_id = session.get("user_id")
    if user_id is None or db.session.get(User, user_id) is None:
        return False

    with _background_task_lock:
        _connected_clients.add(request.sid)
        if _background_task is None:
            _background_task = socketio.start_background_task(background_data_push)
    logs, traffic = _latest_data()
    socketio.emit("data_update", (logs, traffic), to=request.sid)
    return None


@socketio.on("disconnect")
def handle_disconnect(_reason=None):
    with _background_task_lock:
        _connected_clients.discard(request.sid)


def background_data_push():
    global _background_task
    with app.app_context():
        while True:
            with _background_task_lock:
                if not _connected_clients:
                    _background_task = None
                    return
            try:
                socketio.emit("data_update", _latest_data())
            except Exception:
                app.logger.exception("后台快照推送异常")
                db.session.rollback()
            socketio.sleep(app.config["DATA_RECONCILE_INTERVAL"])


ensure_database()


if __name__ == "__main__":
    if app.config["CORS_ORIGINS"] == "*":
        app.logger.warning("当前允许任意 CORS 来源，局域网部署前应在 .env 中限制来源")
    if not app.config["INGEST_API_TOKEN"]:
        app.logger.warning("尚未配置 HELMET_INGEST_API_TOKEN，数据写入接口将返回 503")

    if app.config["START_MEDIAMTX"]:
        start_rtsp_server()
    if app.config["START_DETECT"]:
        start_detect()

    socketio.run(
        app,
        host=app.config["HOST"],
        port=app.config["PORT"],
        debug=False,
        allow_unsafe_werkzeug=True,
    )
