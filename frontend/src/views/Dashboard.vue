<template>
  <BMap
    v-if="mapAk"
    class="bg-map"
    height="calc(100vh - var(--app-header-height))"
    :ak="mapAk"
    :center="{ lng: 106.577667, lat: 29.497096 }"
    :enable-scroll-wheel-zoom="true"
    :tilt="63"
    :zoom="21"
    :minZoom="3"
    :enable-pinch-to-zoom="true"
    :enable-traffic="true"
  >
    <BZoom />
    <BMarker
      title="摄像头1"
      :position="{ lng: 106.57767, lat: 29.497665 }"
      :icon="markerIcon"
    />
    <BMarker
      title="摄像头2"
      :position="{ lng: 106.577667, lat: 29.497096 }"
      :offset="{ x: 0, y: markerY }"
      :icon="markerIcon"
    />
  </BMap>
  <div v-else class="bg-map map-fallback d-flex align-center justify-center">
    <v-alert type="info" variant="tonal">请在 .env.local 中配置 VITE_BAIDU_MAP_AK</v-alert>
  </div>

  <v-navigation-drawer class="bg-transparent pointer-events-none" :width="380">
    <div class="pa-4 pointer-events-auto h-100 d-flex flex-column gap-4">
      <v-card class="glass-panel" prepend-icon="mdi-chart-donut">
        <template #title>
          <div class="d-flex align-center justify-space-between">
            <span>今日统计</span>
            <v-chip :color="connected ? 'success' : 'warning'" size="x-small" variant="flat">
              {{ modeLabel }}
            </v-chip>
          </div>
        </template>
        <v-divider class="border-opacity-25" />
        <v-card-text class="dashboard-stat-charts">
          <div class="chart-box">
            <div ref="trafficChartElement" class="pie-chart" />
            <div class="chart-caption">
              <span>非机动车流量</span>
              <small>占今日总流量</small>
            </div>
          </div>
          <div class="chart-box">
            <div ref="helmetChartElement" class="pie-chart" />
            <div class="chart-caption">
              <span>未佩戴头盔</span>
              <small>占非机动车流量</small>
            </div>
          </div>
        </v-card-text>
        <v-alert v-if="error" density="compact" type="warning" variant="tonal" class="ma-2">
          {{ error }}
        </v-alert>
      </v-card>

      <v-card class="glass-panel" prepend-icon="mdi-poll" title="小时数据（示例）">
        <v-divider class="border-opacity-25" />
        <v-card-text class="hourly-chart-body">
          <div ref="hourlyChartElement" class="hourly-chart" />
        </v-card-text>
      </v-card>
    </div>
  </v-navigation-drawer>

  <v-navigation-drawer location="right" class="bg-transparent pointer-events-none" :width="380">
    <div class="pa-4 pointer-events-auto h-100 d-flex flex-column gap-4">
      <v-card class="glass-panel" prepend-icon="mdi-video-outline" title="实时视频">
        <v-divider class="border-opacity-25" />
        <v-card-text class="pa-2">
          <div class="video-container rounded overflow-hidden">
            <video v-if="useMockData" autoplay loop muted :src="demoVideo" class="w-100 d-block" />
            <img v-else :src="liveVideoUrl" alt="实时检测视频" class="w-100 d-block" />
          </div>
        </v-card-text>
      </v-card>

      <v-card class="glass-panel d-flex flex-column flex-grow-1" prepend-icon="mdi-camera-iris" title="实时抓拍">
        <v-divider class="border-opacity-25" />
        <v-card-text class="pa-2 flex-grow-1 overflow-hidden">
          <v-skeleton-loader v-if="loading" type="list-item-avatar-three-line@3" />
          <v-virtual-scroll v-else :items="logs" height="100%" class="custom-scrollbar pr-2">
            <template #default="{ item }">
              <v-card class="capture-card mb-3 pa-2 border">
                <div class="text-subtitle-2 font-weight-bold text-teal-accent-3 mb-2">
                  {{ item.title || item.type }}
                </div>
                <v-row no-gutters>
                  <v-col cols="5">
                    <v-img :src="item.img" cover class="rounded bg-grey-darken-3 h-100" />
                  </v-col>
                  <v-col cols="7" class="pl-3 text-caption d-flex flex-column justify-space-between">
                    <div><span class="text-grey-lighten-1">置信度：</span><span class="text-red-accent-2 font-weight-bold">{{ item.score || '-' }}</span></div>
                    <div><span class="text-grey-lighten-1">时间：</span><span>{{ item.time }}</span></div>
                    <div class="text-truncate" :title="`摄像头编号：${item.camera}`">
                      <span class="text-grey-lighten-1">编号：</span><span>{{ item.camera || '-' }}</span>
                    </div>
                    <div class="text-truncate" :title="item.location">
                      <span class="text-grey-lighten-1">地点：</span><span class="location-text">{{ item.location || '-' }}</span>
                    </div>
                  </v-col>
                </v-row>
              </v-card>
            </template>
          </v-virtual-scroll>
        </v-card-text>
      </v-card>
    </div>
  </v-navigation-drawer>
</template>

<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from "vue";
import { storeToRefs } from "pinia";
import { init as initChart, type ECharts, type EChartsCoreOption } from "@/plugins/echarts";
import { BMap, BMarker, BZoom } from "vue3-baidu-map-gl";
import cameraMarker from "@/assets/camera2.png";
import demoVideo from "@/assets/test06.mp4";
import { appConfig, videoFeedUrl } from "@/config";
import { useDashboardStore } from "@/stores/dashboard";

const dashboardStore = useDashboardStore();
const { connected, error, loading, logs, traffic } = storeToRefs(dashboardStore);
const mapAk = appConfig.baiduMapAk;
const useMockData = appConfig.useMockData;
const liveVideoUrl = videoFeedUrl;
const modeLabel = computed(() => (useMockData ? "示例数据" : connected.value ? "实时在线" : "连接中"));
const markerIcon = { imageUrl: cameraMarker, imageSize: { width: 60, height: 60 } };

const markerY = ref(0);
let markerDirection = -1;
let jumpInterval: ReturnType<typeof setInterval> | undefined;
let trafficChart: ECharts | null = null;
let helmetChart: ECharts | null = null;
let hourlyChart: ECharts | null = null;
let chartResizeObserver: ResizeObserver | null = null;
const trafficChartElement = ref<HTMLElement | null>(null);
const helmetChartElement = ref<HTMLElement | null>(null);
const hourlyChartElement = ref<HTMLElement | null>(null);

const updateMarker = () => {
  markerY.value += markerDirection;
  if (markerY.value <= -20 || markerY.value >= 0) markerDirection *= -1;
};

const basePieOption = (
  name: string,
  activeColor: string,
  value = 0,
  total = 1,
): EChartsCoreOption => ({
  animationDuration: 650,
  tooltip: {
    trigger: "item",
    formatter: "{b}<br/>{c} ({d}%)",
    backgroundColor: "rgba(4, 13, 31, 0.92)",
    borderColor: "rgba(103, 232, 249, 0.2)",
    textStyle: { color: "#fff" },
  },
  series: [{
    type: "pie",
    center: ["50%", "49%"],
    radius: ["58%", "78%"],
    startAngle: 90,
    label: { show: false },
    labelLine: { show: false },
    emphasis: { scale: false },
    itemStyle: { borderColor: "rgba(10, 25, 58, 0.88)", borderWidth: 3, borderRadius: 7 },
    data: [
      {
        value,
        name,
        itemStyle: { color: activeColor },
        label: {
          show: true,
          position: "center",
          formatter: [`{value|${value}}`, `{percent|${total ? Math.round((value / total) * 100) : 0}%}`].join("\n"),
          rich: {
            value: { color: activeColor, fontSize: 25, lineHeight: 31, fontWeight: 800, fontFamily: "Arial" },
            percent: { color: "#c9d5e7", fontSize: 11, lineHeight: 18 },
          },
        },
      },
      {
        value: Math.max(total - value, 0),
        name: "其他",
        itemStyle: { color: "rgba(255,255,255,0.1)" },
        label: { show: false },
      },
    ],
  }],
});

const updatePieCharts = () => {
  const current = traffic.value[0];
  if (!current) return;

  trafficChart?.setOption(basePieOption("非机动车", "#00d2ff", current.ele, current.total), true);
  helmetChart?.setOption(basePieOption("未佩戴头盔", "#ff616f", current.noHelmet, current.ele), true);
};

const resizeCharts = () => {
  trafficChart?.resize();
  helmetChart?.resize();
  hourlyChart?.resize();
};

const hourlyOption: EChartsCoreOption = {
  color: ["#67b7ff", "#27d6b2", "#ff616f"],
  tooltip: { trigger: "axis", axisPointer: { type: "shadow" } },
  legend: {
    top: 7,
    left: "center",
    itemWidth: 11,
    itemHeight: 7,
    itemGap: 10,
    textStyle: { color: "#cfd8dc", fontSize: 10 },
  },
  grid: { left: 10, right: 12, top: 52, bottom: 12, containLabel: true },
  xAxis: {
    type: "category",
    data: ["6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17"],
    axisTick: { show: false },
    axisLabel: { color: "#cfd8dc", fontSize: 10, interval: 0 },
    axisLine: { lineStyle: { color: "rgba(255,255,255,0.25)" } },
  },
  yAxis: {
    type: "value",
    minInterval: 1,
    axisLabel: { color: "#cfd8dc", fontSize: 10 },
    splitLine: { lineStyle: { color: "rgba(255,255,255,0.08)", type: "dashed" } },
  },
  series: [
    {
      type: "line",
      name: "总流量",
      smooth: true,
      symbol: "none",
      lineStyle: { width: 2 },
      areaStyle: { opacity: 0.08 },
      data: [35, 80, 65, 45, 35, 50, 62, 20, 35, 15, 85, 75],
    },
    {
      type: "bar",
      name: "非机动车",
      barMaxWidth: 12,
      itemStyle: { borderRadius: [4, 4, 0, 0] },
      data: [12, 30, 15, 15, 15, 20, 42, 25, 15, 15, 45, 35],
    },
    {
      type: "bar",
      name: "未佩戴头盔",
      barMaxWidth: 12,
      itemStyle: { borderRadius: [4, 4, 0, 0] },
      data: [5, 25, 5, 15, 10, 15, 28, 10, 20, 22, 25, 10],
    },
  ],
};

watch(traffic, updatePieCharts, { deep: true });

onMounted(async () => {
  await nextTick();
  const trafficDom = trafficChartElement.value;
  const helmetDom = helmetChartElement.value;
  const hourlyDom = hourlyChartElement.value;
  if (trafficDom) trafficChart = initChart(trafficDom);
  if (helmetDom) helmetChart = initChart(helmetDom);
  if (hourlyDom) hourlyChart = initChart(hourlyDom);
  trafficChart?.setOption(basePieOption("非机动车", "#00d2ff"));
  helmetChart?.setOption(basePieOption("未佩戴头盔", "#ff616f"));
  hourlyChart?.setOption(hourlyOption);
  const chartElements = [trafficDom, helmetDom, hourlyDom].filter(
    (element): element is HTMLElement => element !== null,
  );
  chartResizeObserver = new ResizeObserver(() => {
    window.requestAnimationFrame(resizeCharts);
  });
  chartElements.forEach((element) => chartResizeObserver?.observe(element));
  window.requestAnimationFrame(resizeCharts);
  jumpInterval = setInterval(updateMarker, 32);
  window.addEventListener("resize", resizeCharts);
  void dashboardStore.start().then(updatePieCharts);
});

onBeforeUnmount(() => {
  if (jumpInterval) clearInterval(jumpInterval);
  window.removeEventListener("resize", resizeCharts);
  chartResizeObserver?.disconnect();
  trafficChart?.dispose();
  helmetChart?.dispose();
  hourlyChart?.dispose();
  dashboardStore.stop();
});
</script>

<style scoped>
.bg-map { position: fixed; top: var(--app-header-height); left: 0; width: 100%; z-index: 0; }
.map-fallback { height: calc(100vh - var(--app-header-height)); background: linear-gradient(135deg, #dbeafe, #eff6ff); }
.pointer-events-none { pointer-events: none; }
.pointer-events-auto { pointer-events: auto; }
.gap-4 { gap: 1rem; }
.glass-panel {
  overflow: hidden;
  background: linear-gradient(145deg, rgba(10, 25, 58, 0.88), rgba(19, 43, 86, 0.8)) !important;
  backdrop-filter: blur(16px) saturate(125%);
  -webkit-backdrop-filter: blur(16px) saturate(125%);
  border: 1px solid rgba(134, 214, 255, 0.14) !important;
  color: #fff !important;
  box-shadow: 0 18px 48px rgba(7, 19, 44, 0.28) !important;
  border-radius: 18px !important;
}
.glass-panel :deep(.v-card-title) { font-size: 15px; font-weight: 750; letter-spacing: -0.01em; }
.glass-panel :deep(.v-card-item__prepend) { color: #67e8f9; }
.capture-card { background: rgba(255, 255, 255, 0.055) !important; border-color: rgba(255, 255, 255, 0.09) !important; border-radius: 13px !important; transition: transform 0.2s, background 0.2s; }
.capture-card:hover { background: rgba(255, 255, 255, 0.1) !important; transform: translateX(-4px); }
.dashboard-stat-charts {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  align-items: center;
  min-height: 190px;
  padding: 8px 10px 14px !important;
  gap: 4px;
}
.chart-box { min-width: 0; display: flex; flex-direction: column; align-items: center; }
.pie-chart { width: 100%; height: 138px; }
.chart-caption { display: flex; flex-direction: column; align-items: center; margin-top: -2px; color: #e8f2ff; font-size: 11px; font-weight: 700; line-height: 1.45; }
.chart-caption small { color: rgba(211, 227, 245, 0.54); font-size: 9px; font-weight: 500; }
.hourly-chart-body { min-height: 296px; padding: 2px 7px 8px !important; }
.hourly-chart { width: 100%; height: 286px; }
.location-text { font-size: 10px; }
.video-container { min-height: 178px; aspect-ratio: 16 / 9; border: 1px solid rgba(134, 214, 255, 0.12); border-radius: 13px !important; background: #020617; }
.video-container video, .video-container img { width: 100%; height: 100%; object-fit: cover; }
.custom-scrollbar::-webkit-scrollbar { width: 6px; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(0, 210, 255, 0.4); border-radius: 10px; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: rgba(0, 210, 255, 0.8); }

@media (max-width: 700px) {
  .glass-panel { border-radius: 15px !important; }
}
</style>
