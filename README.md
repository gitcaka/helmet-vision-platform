# Helmet Vision Platform

非机动车头盔佩戴智能检测平台，前后端统一位于 `E:\work\helmet-vision-platform`，并作为一个 Git 仓库维护。

## 在线演示

GitHub Pages 部署前端示例数据模式，不依赖 Flask、SQLite 或摄像头：

https://gitcaka.github.io/helmet-vision-platform/

每次推送 `main` 分支后，`.github/workflows/pages.yml` 会自动构建并发布前端。GitHub Pages 仅托管静态页面，真实后端和视频流仍需按下文在本地或服务器单独部署。

```text
E:\work\helmet-vision-platform\
├─ backend\     Flask、SQLite、Socket.IO、RTSP 转 MJPEG
└─ frontend\    Vue 3、Vuetify、ECharts、百度地图
```

## 最快启动：只看前端演示

前端默认使用示例数据，不需要数据库、Flask 或摄像头：

```powershell
Set-Location E:\work\helmet-vision-platform\frontend
npm ci
npm run dev
```

打开 `http://localhost:3000`，使用 `admin / 123456` 登录。

## 完整启动：前端连接 Flask

### 1. 初始化后端

```powershell
Set-Location E:\work\helmet-vision-platform\backend
Copy-Item .env.example .env
```

编辑 `.env`，至少填写：

```dotenv
HELMET_SECRET_KEY=一个持久随机值
HELMET_INGEST_API_TOKEN=检测程序写入数据使用的Token
HELMET_CORS_ORIGINS=http://localhost:3000
```

可使用 `py13` 生成随机值：

```powershell
D:\software\miniconda\envs\py13\python.exe -c "import secrets; print(secrets.token_hex(32))"
```

初始化 SQLite 和管理员账号：

```powershell
D:\software\miniconda\envs\py13\python.exe E:\work\helmet-vision-platform\backend\init_db.py --username admin
```

### 2. 启动后端

在第一个 PowerShell 窗口运行：

```powershell
Set-Location E:\work\helmet-vision-platform\backend
powershell -ExecutionPolicy Bypass -File .\start_backend.ps1
```

访问 `http://localhost:5000/health` 检查状态。

### 3. 切换并启动前端

在 `frontend\.env.local` 中设置：

```dotenv
VITE_USE_MOCK_DATA=false
VITE_API_URL=http://localhost:5000
VITE_BAIDU_MAP_AK=填写百度地图浏览器端AK
```

在第二个 PowerShell 窗口运行：

```powershell
Set-Location E:\work\helmet-vision-platform\frontend
npm run dev
```

打开 `http://localhost:3000`，使用初始化数据库时创建的账号登录。停止服务时分别在两个窗口按 `Ctrl+C`。

## 当前能力边界

- 登录、会话恢复、退出、统计查询和 Socket.IO 实时事件已经完成前后端衔接。
- 示例模式会生成本地统计变化和抓拍记录，管理员审批及注册页面也是明确标记的演示交互。
- 真实视频由 Flask `/video_feed` 提供；MediaMTX、RTSP 摄像头和 PaddleDetection 仍是独立外部服务。
- 未配置真实视频链路时，Flask 仍可提供登录、SQLite 和普通 API，但实时画面只能显示后端占位或重连状态。

## 验证命令

前端：

```powershell
Set-Location E:\work\helmet-vision-platform\frontend
npm run typecheck
npm run build
npm audit
```

后端：

```powershell
Set-Location E:\work\helmet-vision-platform\backend
D:\software\miniconda\envs\py13\python.exe -m unittest discover -s tests -v
```
