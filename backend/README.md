# Helmet Vision Platform Backend

安全帽检测系统的 Flask 后端，负责登录、SQLite 数据存储、Socket.IO 数据推送，以及将 RTSP 检测视频转换为浏览器可显示的 MJPEG 流。

PaddleDetection 和 MediaMTX 是独立外部服务，不包含在本仓库中。Flask 后端固定使用现有的 `py13` Conda 环境运行。

## 组成

- `app.py`：HTTP、Socket.IO、视频流和外部服务启动入口。
- `models.py`：`users`、`log`、`traffic` 三个 SQLite 数据模型。
- `video_stream.py`：单 RTSP 连接、共享 JPEG、断线重连和状态监测。
- `config.py`：从环境变量或 `.env` 读取配置。
- `init_db.py`：初始化数据库和管理员账号。
- `data/helmet.db`：默认运行数据库，不提交到 Git。

## 初始化

复制 `.env.example` 为 `.env`，按实际情况修改配置。然后创建管理员：

```powershell
D:\software\miniconda\envs\py13\python.exe E:\work\helmet-vision-platform\backend\init_db.py --username admin
```

密码会在终端中隐藏输入。也可以通过 `HELMET_ADMIN_PASSWORD` 临时环境变量传入。

## 启动后端

```powershell
E:\work\helmet-vision-platform\backend\start_backend.ps1
```

或直接运行：

```powershell
D:\software\miniconda\envs\py13\python.exe E:\work\helmet-vision-platform\backend\app.py
```

默认监听 `http://localhost:5000`。访问 `/health` 可以检查后端、SQLite 和视频线程状态。

首次正式运行前，应在 `.env` 中填写持久的 `HELMET_SECRET_KEY` 和 `HELMET_INGEST_API_TOKEN`。写入 Token 留空时，数据写入接口会关闭并返回 503。

如果前端与后端端口不同，HTTP 请求必须启用 Cookie，例如 Fetch 使用 `credentials: "include"`，Socket.IO 客户端使用 `withCredentials: true`。同时应把 `HELMET_CORS_ORIGINS` 改成真实前端地址，不要在局域网部署时继续使用 `*`。

## 接口

- `POST /login`：用户登录并建立 HttpOnly Cookie 会话。
- `POST /logout`：退出并清除会话。
- `GET /api/me`：读取当前登录用户。
- `GET /video_feed`：需要登录；返回共享的 MJPEG 检测视频。
- `GET /api/data`：需要登录；读取最新 50 条告警和 20 条交通统计。
- `POST /api/logs`：写入检测告警。
- `POST /api/traffic`：按日期新增或更新交通统计。
- Socket.IO `data_update`：需要登录；连接时推送完整快照，并按配置周期校准。
- Socket.IO `log_created`、`traffic_updated`：数据写入后的增量事件。

数据写入请求必须携带与 `HELMET_INGEST_API_TOKEN` 相同的 `X-API-Token` 请求头。告警还必须携带全局唯一且重试时保持不变的 `event_id`：

```json
{
  "event_id": "camera-01-20260830-000001",
  "type": "noHelmet",
  "camera": "camera-01",
  "score": 0.97
}
```

首次写入返回 201；相同 `event_id` 重试返回 200 和 `duplicate: true`，数据库中只保留一条记录。数据库提交成功后，即使 Socket.IO 临时离线，HTTP 写入仍会返回成功。

视频流只建立一条 RTSP 连接，所有已登录浏览器共享编码后的最新帧。RTSP 不可用时会输出占位画面并自动重连，最后一位观看者离开后释放连接。

## 外部检测服务

`HELMET_START_MEDIAMTX` 和 `HELMET_START_DETECT` 默认均为 `false`，所以启动 Flask 不会自动启动 MediaMTX 或 PaddleDetection。

确认独立的 PaddleDetection 环境和 MediaMTX 路径可用后，才应在 `.env` 中开启对应选项。当前 `py13` 环境不包含 PaddlePaddle，不应直接用于模型推理。
