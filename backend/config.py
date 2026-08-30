import os
import secrets
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


def _boolean(name, default=False):
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _cors_origins():
    value = os.getenv("HELMET_CORS_ORIGINS", "*").strip()
    if value == "*":
        return "*"
    return [item.strip() for item in value.split(",") if item.strip()]


class Config:
    DATA_DIR = Path(os.getenv("HELMET_DATA_DIR", BASE_DIR / "data")).resolve()
    DATABASE_PATH = str(
        Path(os.getenv("HELMET_DATABASE_PATH", DATA_DIR / "helmet.db")).resolve()
    )
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{Path(DATABASE_PATH).as_posix()}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {"timeout": 10, "check_same_thread": False},
        "pool_pre_ping": True,
    }

    SECRET_KEY = os.getenv("HELMET_SECRET_KEY") or secrets.token_hex(32)
    INGEST_API_TOKEN = os.getenv("HELMET_INGEST_API_TOKEN", "")
    CORS_ORIGINS = _cors_origins()
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = os.getenv("HELMET_SESSION_COOKIE_SAMESITE", "Lax")
    SESSION_COOKIE_SECURE = _boolean("HELMET_SESSION_COOKIE_SECURE")
    PERMANENT_SESSION_LIFETIME = timedelta(
        hours=float(os.getenv("HELMET_SESSION_HOURS", "8"))
    )
    LOGIN_MAX_ATTEMPTS = int(os.getenv("HELMET_LOGIN_MAX_ATTEMPTS", "5"))
    LOGIN_WINDOW_SECONDS = int(os.getenv("HELMET_LOGIN_WINDOW_SECONDS", "300"))

    HOST = os.getenv("HELMET_HOST", "0.0.0.0")
    PORT = int(os.getenv("HELMET_PORT", "5000"))
    DATA_RECONCILE_INTERVAL = float(
        os.getenv(
            "HELMET_DATA_RECONCILE_INTERVAL",
            os.getenv("HELMET_DATA_PUSH_INTERVAL", "60"),
        )
    )

    RTSP_URL = os.getenv("HELMET_RTSP_URL", "rtsp://localhost:8554/output")
    VIDEO_FRAME_RATE = float(os.getenv("HELMET_VIDEO_FRAME_RATE", "12"))
    VIDEO_JPEG_QUALITY = int(os.getenv("HELMET_VIDEO_JPEG_QUALITY", "80"))
    VIDEO_OPEN_TIMEOUT_MS = int(os.getenv("HELMET_VIDEO_OPEN_TIMEOUT_MS", "3000"))
    VIDEO_READ_TIMEOUT_MS = int(os.getenv("HELMET_VIDEO_READ_TIMEOUT_MS", "3000"))
    VIDEO_RECONNECT_INITIAL = float(
        os.getenv("HELMET_VIDEO_RECONNECT_INITIAL", "0.5")
    )
    VIDEO_RECONNECT_MAX = float(os.getenv("HELMET_VIDEO_RECONNECT_MAX", "10"))
    MEDIAMTX_PATH = os.getenv(
        "HELMET_MEDIAMTX_PATH",
        r"E:\work\mediamtx_v1.8.0_windows_amd64\mediamtx.exe",
    )
    START_MEDIAMTX = _boolean("HELMET_START_MEDIAMTX")

    CONDA_EXE = os.getenv(
        "HELMET_CONDA_EXE",
        r"D:\software\miniconda\Scripts\conda.exe",
    )
    PADDLE_ENV_NAME = os.getenv("HELMET_PADDLE_ENV_NAME", "PaddleDetection")
    PADDLE_INFER_SCRIPT = os.getenv(
        "HELMET_PADDLE_INFER_SCRIPT",
        r"E:\work\PaddleDetection\deploy\python\infer.py",
    )
    PADDLE_MODEL_DIR = os.getenv(
        "HELMET_PADDLE_MODEL_DIR",
        r"E:\work\PaddleDetection\inference_model\ppyoloe_plus_crn_l_80e_coco",
    )
    PADDLE_DEVICE = os.getenv("HELMET_PADDLE_DEVICE", "gpu")
    PADDLE_PUSH_URL = os.getenv(
        "HELMET_PADDLE_PUSH_URL", "rtsp://localhost:8554/"
    )
    CAMERA_ID = int(os.getenv("HELMET_CAMERA_ID", "0"))
    START_DETECT = _boolean("HELMET_START_DETECT")
