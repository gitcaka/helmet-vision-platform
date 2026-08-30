<script setup lang="ts">
import { ref } from "vue";
import demoVideo from "@/assets/test06.mp4";
import { appConfig, videoFeedUrl } from "@/config";

interface MonitorItem {
  cameraId: string;
  location: string;
  zone: string;
}

const useMockData = appConfig.useMockData;
const liveVideoUrl = videoFeedUrl;
const allCameraList = ["001", "002", "003", "004", "005", "006", "007", "008", "009", "010"];
const monitorList = ref<MonitorItem[]>([
  { cameraId: "001", location: "交运实验楼东侧", zone: "教学区" },
  { cameraId: "002", location: "交运实验楼107", zone: "实验区" },
  { cameraId: "003", location: "南岸校区主干道", zone: "道路区" },
  { cameraId: "004", location: "工程结构研究所", zone: "科研区" },
  { cameraId: "005", location: "校园东门入口", zone: "出入口" },
  { cameraId: "006", location: "河海学院北侧", zone: "教学区" },
]);
</script>

<template>
  <div class="video-wall-container">
    <div class="page-heading monitor-heading">
      <div>
        <div class="page-heading__eyebrow">Live Operations</div>
        <h1 class="page-heading__title">实时监控中心</h1>
        <p class="page-heading__description">集中查看路侧摄像头画面与设备状态，切换编号即可调整当前监控点位。</p>
      </div>
      <div class="monitor-summary">
        <v-chip color="success" variant="tonal" prepend-icon="mdi-access-point" size="small">
          {{ monitorList.length }} 路在线
        </v-chip>
        <v-chip color="primary" variant="tonal" prepend-icon="mdi-database-outline" size="small">
          {{ useMockData ? "示例画面" : "实时视频流" }}
        </v-chip>
      </div>
    </div>

    <v-row class="monitor-grid" dense>
      <v-col v-for="(monitor, index) in monitorList" :key="index" cols="12" sm="6" xl="4">
        <v-card class="monitor-card surface-card" elevation="0">
          <div class="monitor-header">
            <div class="camera-title">
              <span class="live-dot" />
              <div>
                <strong>摄像头 {{ monitor.cameraId }}</strong>
                <span>{{ monitor.zone }} · 连接正常</span>
              </div>
            </div>

            <v-select
              v-model="monitor.cameraId"
              :items="allCameraList"
              variant="solo-filled"
              density="compact"
              hide-details
              class="camera-select"
              aria-label="切换摄像头"
            >
              <template #prepend-inner><v-icon icon="mdi-cctv" size="16" /></template>
            </v-select>
          </div>

          <div class="video-wrapper">
            <video v-if="useMockData" class="monitor-video" autoplay loop muted playsinline :src="demoVideo" />
            <img v-else class="monitor-video" :src="liveVideoUrl" :alt="`摄像头 ${monitor.cameraId} 实时画面`" />
            <div class="video-shade" />
            <div class="live-badge"><span /> LIVE</div>
            <div class="camera-watermark">CAM {{ monitor.cameraId }}</div>
            <div class="location-overlay">
              <v-icon icon="mdi-map-marker-outline" size="16" />
              {{ monitor.location }}
            </div>
          </div>

          <div class="monitor-footer">
            <span><v-icon icon="mdi-video-check-outline" size="16" /> 1080P</span>
            <span><v-icon icon="mdi-clock-outline" size="16" /> 延迟 42ms</span>
            <span class="online-text"><span /> 正常</span>
          </div>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<style scoped lang="scss">
.video-wall-container {
  min-height: calc(100vh - var(--app-header-height));
  padding: clamp(20px, 2.6vw, 36px);
  background:
    radial-gradient(circle at 92% 4%, rgba(8, 169, 196, 0.08), transparent 25%),
    transparent;
}

.monitor-heading { max-width: 1500px; margin-right: auto; margin-left: auto; }
.monitor-summary { display: flex; flex-wrap: wrap; justify-content: flex-end; gap: 9px; }
.monitor-grid { max-width: 1500px; margin: 0 auto; }
.monitor-card { overflow: hidden; margin: 6px; background: rgba(255, 255, 255, 0.94) !important; }
.monitor-card:hover { transform: translateY(-3px); }

.monitor-header { display: flex; align-items: center; justify-content: space-between; gap: 14px; padding: 14px 15px; }
.camera-title { display: flex; align-items: center; gap: 11px; min-width: 0; }
.camera-title > div { display: flex; min-width: 0; flex-direction: column; }
.camera-title strong { color: #162544; font-size: 13px; }
.camera-title span { margin-top: 2px; color: #94a3b8; font-size: 10px; }
.live-dot { flex: 0 0 auto; width: 9px; height: 9px; border-radius: 50%; background: #34d399; box-shadow: 0 0 0 5px rgba(52, 211, 153, 0.12); }

.camera-select { max-width: 122px; }
.camera-select :deep(.v-field) { min-height: 36px; border-radius: 10px; background: #f0f4fb; box-shadow: none; }
.camera-select :deep(.v-field__input) { min-height: 36px; padding-top: 0; padding-bottom: 0; color: #334155; font-size: 12px; font-weight: 700; }

.video-wrapper { position: relative; aspect-ratio: 16 / 9; margin: 0 10px; overflow: hidden; border-radius: 15px; background: #071126; }
.monitor-video { display: block; width: 100%; height: 100%; object-fit: cover; }
.video-shade { position: absolute; inset: 0; background: linear-gradient(180deg, rgba(3, 10, 26, 0.2), transparent 42%, rgba(3, 10, 26, 0.62)); pointer-events: none; }
.live-badge { position: absolute; top: 12px; left: 12px; display: flex; align-items: center; gap: 6px; padding: 5px 8px; border: 1px solid rgba(255, 255, 255, 0.2); border-radius: 999px; background: rgba(8, 18, 39, 0.54); color: #fff; font-size: 9px; font-weight: 800; letter-spacing: 0.12em; backdrop-filter: blur(8px); }
.live-badge span { width: 6px; height: 6px; border-radius: 50%; background: #fb7185; box-shadow: 0 0 8px #fb7185; animation: pulse 1.7s infinite; }
.camera-watermark { position: absolute; top: 13px; right: 13px; color: rgba(255, 255, 255, 0.8); font-family: Consolas, monospace; font-size: 10px; letter-spacing: 0.08em; }
.location-overlay { position: absolute; right: 13px; bottom: 12px; left: 13px; display: flex; align-items: center; gap: 6px; color: #fff; font-size: 11px; font-weight: 650; }

.monitor-footer { display: flex; align-items: center; gap: 16px; padding: 12px 15px 14px; color: #7b8ba4; font-size: 10px; }
.monitor-footer > span { display: inline-flex; align-items: center; gap: 5px; }
.online-text { margin-left: auto; color: #17a673; font-weight: 750; }
.online-text span { width: 6px; height: 6px; border-radius: 50%; background: #34d399; }

@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.45; } }

@media (max-width: 700px) {
  .video-wall-container { padding: 18px 10px 24px; }
  .monitor-summary { justify-content: flex-start; }
  .monitor-card { margin: 5px 0; }
}
</style>
