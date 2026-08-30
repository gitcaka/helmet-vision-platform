# 头盔佩戴检测 Web 大屏

Vue 3 + Vuetify 前端，提供登录、大屏统计、多画面监控、记录分析和管理员演示页面。项目支持“示例数据”和“真实后端”两种模式，页面代码无需切换分支。

在线示例数据演示：https://gitcaka.github.io/helmet-vision-platform/

## 环境要求

- Node.js 20.19 或更高版本
- npm 10 或更高版本
- 百度地图浏览器端 AK（地图功能需要）

## 配置

首次使用时创建本地配置：

```powershell
Set-Location E:\work\helmet-vision-platform\frontend
Copy-Item .env.example .env.local
```

主要变量：

```dotenv
VITE_USE_MOCK_DATA=true
VITE_API_URL=http://localhost:5000
VITE_BAIDU_MAP_AK=填写百度地图浏览器端AK
```

- `VITE_USE_MOCK_DATA=true`：不需要 Flask、数据库或摄像头即可演示。
- `VITE_USE_MOCK_DATA=false`：使用 Flask 的 Cookie 会话、REST、Socket.IO 和 `/video_feed`。
- `.env.local` 已被 Git 忽略，不要提交真实 AK。

## 启动

```powershell
Set-Location E:\work\helmet-vision-platform\frontend
npm ci
npm run dev
```

浏览器打开 `http://localhost:3000`。示例模式账号：

```text
用户名：admin
密码：123456
```

开发服务器仅绑定 `127.0.0.1`，且端口 3000 被占用时会直接报错，避免自动换端口后导致后端 CORS 地址不一致。

## 质量检查

```powershell
npm run typecheck
npm run build
npm audit
```

生产文件输出到 `dist`。当前只打包一个演示视频并供多个监控卡片复用；切换真实模式后页面显示后端 MJPEG 视频流。

## 关键目录

```text
src/
├─ config.ts              环境变量和服务地址
├─ services/http.ts       Axios 实例、Cookie 和错误处理
├─ stores/auth.ts         登录与会话恢复
├─ stores/dashboard.ts    示例数据、REST 和 Socket.IO 数据源
├─ plugins/echarts.ts     按需注册 ECharts 模块
└─ views/                 登录、大屏、监控、分析和成员页面
```

## 真实后端模式

1. 先按根目录 README 初始化并启动 Flask。
2. 将 `.env.local` 中的 `VITE_USE_MOCK_DATA` 改为 `false`。
3. 重启 `npm run dev`，环境变量变更不会自动作用于已运行的 Vite 进程。
4. 使用后端数据库中创建的管理员账号登录。

后端需要允许 `http://localhost:3000` 跨域并接受凭据。前端已经统一启用 Axios `withCredentials` 和 Socket.IO `withCredentials`。
