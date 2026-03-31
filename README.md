# 🛵 非机动车骑乘人员头盔佩戴检测系统 - Web 管控大屏

本项目是一个面向智慧交通与安防领域的**非机动车骑乘人员头盔佩戴检测 Web 大屏管控平台**。通过接入路侧摄像头视频流，结合 AI 视觉分析算法，实时检测并统计非机动车流量及头盔佩戴情况，为交通管理部门提供直观、高效的数据可视化支撑。

## ✨ 主要功能

  * **📊 数据可视化大屏**
      * **今日统计**：实时环形图展示非机动车总流量、未佩戴头盔占比（基于 ECharts）。
      * **趋势分析**：小时级数据分布柱状图、未佩戴头盔趋势折线图（基于 ApexCharts）。
  * **🗺️ GIS 融合管控**
      * 集成百度地图 GL (BMap GL)，支持地图缩放、倾斜等 3D 视角操作。
      * 动态绘制监控网点 Marker，支持实时状态反馈与跳跃动画预警。
  * **📹 实时视频与流媒体**
      * 多路摄像头并发监控，支持视频流动态切换与网格化布局（Live 状态灯预警）。
      * Socket.io 实时接收 AI 抓拍数据，毫秒级更新违规抓拍列表（包含抓拍图、置信度、时间、地点）。
  * **🔐 鉴权与后台管理**
      * 基于 Pinia 的状态管理与 Token 鉴权登录。
      * 管理员资格审核模块，支持列表展开、通过/拒绝交互以及动态 Snackbar 消息提示。

## 🛠️ 技术栈

  * **前端框架**: Vue 3 (Composition API, `<script setup>`)
  * **UI 组件库**: Vuetify 3 (Material Design 风格，深度定制 Glassmorphism 毛玻璃 UI)
  * **状态管理**: Pinia
  * **网络通信**: Axios (RESTful API), Socket.io-client (WebSocket 实时数据流)
  * **图表引擎**: ECharts 5, ApexCharts (`vue3-apexcharts`)
  * **地图引擎**: vue3-baidu-map-gl
  * **构建工具**: Vite

## 🚀 快速开始

### 1\. 环境准备

请确保你的计算机上已安装 [Node.js](https://nodejs.org/) (推荐 v16+ 版本) 和 npm/pnpm/yarn。

### 2\. 克隆项目

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 3\. 安装依赖

```bash
npm install
# 或者使用 yarn / pnpm
# yarn install / pnpm install
```

### 4\. 配置环境变量与地图 AK

在运行前，请检查项目中的百度地图 AK 密钥和后端接口地址：

1.  **地图 AK**：在包含 `<BMap>` 的组件中，将 `ak="你的密钥"` 替换为你申请的百度地图开发者 AK。
2.  **后端 API 端口**：当前前端默认请求后端的地址为 `http://localhost:5000`。若需修改，请全局搜索替换或在 Axios 拦截器/`.env` 文件中配置 `baseURL`。

### 5\. 启动开发服务器

```bash
npm run dev
```

运行成功后，终端会输出本地访问地址（通常为 `http://localhost:5173`）。

### 6\. 构建生产版本

```bash
npm run build
```

构建完成后，静态文件将输出在 `dist` 目录中，可直接部署至 Nginx 或其他静态服务器。

## 📁 核心目录结构

```text
├── src/
│   ├── assets/          # 静态资源（视频、图片、图标）
│   ├── components/      # 通用组件
│   ├── router/          # Vue Router 路由配置
│   ├── store/           # Pinia 状态管理 (如 authStore)
│   ├── views/           # 页面视图 (登录页、大屏监控页、后台管理页)
│   ├── App.vue          # 根组件
│   ├── main.ts          # 全局入口文件（挂载 Vuetify, ECharts, 路由等）
├── public/              # 公共静态资源
├── package.json         # 项目依赖
├── vite.config.ts       # Vite 打包与开发配置
└── README.md            # 项目说明文档
```

## ⚠️ 注意事项与最佳实践

  * **模拟模式切换**：如果后端/数据库未开启，可在 `store/authStore.ts` 中将 `ENABLE_BACKEND` 切换为 `false`，使用纯前端 Mock 数据进行 UI 调试和演示。
  * **内存管理**：本项目包含了大量的图表渲染和 WebSocket 通信。为防止内存泄漏，组件在 `onBeforeUnmount` 生命周期中已对 `setInterval` 和 ECharts 实例进行了标准的销毁处理（`dispose` / `clearInterval`），在二次开发时请务必保持此规范。
  * **视频资源加载**：因采用 Vite 构建工具，页面中的动态视频本地资源需使用 `new URL('../assets/xxx.mp4', import.meta.url).href` 进行解析加载。

## 🤝 贡献与支持

如果你在运行过程中遇到任何问题，或有新的功能建议，欢迎提交 Issue 或 Pull Request。

-----

*Powered by Vue 3 & Vuetify. Designed for Smart Traffic Management.*