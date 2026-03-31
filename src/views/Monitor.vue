<template>
  <div class="video-wall-container pa-4">
    <v-row class="ma-0">
      <v-col
        v-for="(monitor, index) in monitorList"
        :key="index"
        cols="12"
        sm="6"
        lg="4"
        class="pa-2"
      >
        <v-card class="monitor-card" elevation="2" rounded="lg" color="white">

          <div class="monitor-header d-flex align-center justify-space-between px-3 py-2 border-bottom">
            <div class="d-flex align-center">
              <span class="live-dot mr-2"></span>
              <span class="text-caption font-weight-bold text-red tracking-wide">
                LIVE
              </span>
            </div>

            <div class="select-wrapper">
              <v-select
                v-model="monitor.cameraId"
                :items="allCameraList"
                variant="solo-filled"
                density="compact"
                hide-details
                bg-color="rgba(100, 181, 246, 0.1)"
                class="camera-select"
              >
                <template v-slot:prepend-inner>
                  <v-icon size="small" color="grey">mdi-cctv</v-icon>
                </template>
              </v-select>
            </div>
          </div>

          <div class="video-container pa-2">
            <div class="video-wrapper border rounded">
              <video
                class="monitor-video"
                autoplay
                loop
                muted
                :src="monitor.videoSrc"
              ></video>

              <div class="camera-watermark">
                CAM - {{ monitor.cameraId }}
              </div>
            </div>
          </div>

        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

// 摄像头列表
const allCameraList = ref([
  "001", "002", "003", "004", "005", "006", "007", "008", "009", "010"
]);

/* Vite 动态资源加载处理 */
const getAssetVideo = (name: string) => {
  return new URL(`../assets/${name}.mp4`, import.meta.url).href;
};

// 数据驱动：监控机位列表
const monitorList = ref([
  { cameraId: "001", videoSrc: getAssetVideo("test06") },
  { cameraId: "002", videoSrc: getAssetVideo("test04") },
  { cameraId: "003", videoSrc: getAssetVideo("test07") },
  { cameraId: "004", videoSrc: getAssetVideo("record1") },
  { cameraId: "005", videoSrc: getAssetVideo("test08") },
  { cameraId: "006", videoSrc: getAssetVideo("test09") },
]);
</script>

<style scoped lang="scss">
/* 全局背景：干净的浅灰蓝色 */
.video-wall-container {
  background-color: #f0f4f8; /* 白色风格背景色 */
  min-height: calc(100vh - 64px);
}

/* 监控卡片样式 */
.monitor-card {
  // 增加一点点极细的、颜色极浅的边框，在某些纯白模式下能更好区分
  border: 1px solid rgba(0, 0, 0, 0.03);
}

/* 头部状态栏：改为浅灰色背景 */
.monitor-header {
  background-color: #f8fafc; /* Slate 50 */

  .tracking-wide {
    letter-spacing: 0.1em;
  }
}

// 细分割线
.border-bottom {
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

/* LIVE 呼吸红灯 (在白色背景下依旧使用红色，非常显眼) */
.live-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #ff1744; /* 红色稍微调亮 */
  box-shadow: 0 0 6px #ff1744;
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0% { opacity: 1; box-shadow: 0 0 6px #ff1744; }
  50% { opacity: 0.5; box-shadow: 0 0 2px #ff1744; }
  100% { opacity: 1; box-shadow: 0 0 6px #ff1744; }
}

/* 选择框样式定制 (白色风格) */
.select-wrapper {
  width: 140px;

  :deep(.v-field__input) {
    min-height: 32px !important;
    padding-top: 0;
    padding-bottom: 0;
    font-size: 14px;
    color: #334155; /* 深蓝灰色文字 */
  }

  :deep(.v-field) {
    border-radius: 6px;
    box-shadow: none !important; // 去除solo默认阴影
  }
}

/* 视频容器与比例 */
.video-wrapper {
  position: relative;
  width: 100%;
  aspect-ratio: 16 / 9;
  background-color: #000;
  overflow: hidden; // 保证视频圆角

  // 极浅的视频外框线
  &.border {
    border: 1px solid rgba(0, 0, 0, 0.08) !important;
  }

  .monitor-video {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
  }
}

/* 白色风格水印：改为深色半透明文字，加白阴影 */
.camera-watermark {
  position: absolute;
  bottom: 8px; /* 稍微向上移一点 */
  right: 12px;
  font-family: "Courier New", Courier, monospace;
  font-size: 13px;
  font-weight: bold;
  color: rgba(0, 0, 0, 0.6); // 黑色半透明
  text-shadow: 1px 1px 0px rgba(255, 255, 255, 0.8); // 白色文字阴影
  pointer-events: none;
}
</style>
