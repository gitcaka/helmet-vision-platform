<template>
  <div class="dashboard-container">
    <div class="page-heading">
      <div>
        <div class="page-heading__eyebrow">Analytics workspace</div>
        <h1 class="page-heading__title">记录分析</h1>
        <p class="page-heading__description">
          聚合设备流量、头盔佩戴情况与时段趋势，快速发现高风险区域和异常时段。
        </p>
      </div>
      <div class="heading-actions">
        <v-chip color="primary" variant="tonal" prepend-icon="mdi-calendar-today">今日数据</v-chip>
        <v-chip color="secondary" variant="tonal" prepend-icon="mdi-cctv">设备 {{ camera1 }}</v-chip>
      </div>
    </div>

    <v-row dense>
      <v-col cols="12" lg="2" md="12">
        <v-card class="surface-card analysis-card h-100 d-flex flex-column">
          <v-card-title class="text-subtitle-1 font-weight-bold px-4 pt-4">
            <v-icon start color="primary">mdi-crosshairs-gps</v-icon>
            数据选点
          </v-card-title>
          <v-divider class="mx-4 mt-2 mb-4"></v-divider>

          <v-card-text class="flex-grow-1 px-4">
            <v-select
              v-model="camera1"
              :items="allCameraList"
              label="当前设备"
              variant="outlined"
              density="compact"
              hide-details
              prepend-inner-icon="mdi-cctv"
              class="mb-6"
            ></v-select>

            <div class="mb-4 d-flex flex-column gap-1">
              <span class="text-caption text-grey-darken-1">监控地点</span>
              <span class="text-body-2 font-weight-medium text-grey-darken-3">
                重庆交通大学交运实验楼107
              </span>
            </div>

            <div class="d-flex align-center justify-space-between mt-auto pt-4">
              <span class="text-caption text-grey-darken-1">设备状态</span>
              <v-chip color="success" size="small" variant="flat" class="font-weight-bold">
                <v-icon start size="14">mdi-check-circle</v-icon>
                良好
              </v-chip>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" lg="5" md="6">
        <v-card class="surface-card analysis-card h-100">
          <v-card-title class="text-subtitle-1 font-weight-bold px-4 pt-4">
            <v-icon start color="info">mdi-chart-donut</v-icon>
            今日统计
          </v-card-title>
          <v-divider class="mx-4 mt-2"></v-divider>

          <v-card-text class="stats-chart-content">
            <div class="chart-box">
              <div ref="pieChartOne" class="pie-chart"></div>
              <div class="chart-caption">
                <span>非机动车流量</span>
                <small>占总流量 52%</small>
              </div>
            </div>
            <div class="chart-box">
              <div ref="pieChartTwo" class="pie-chart"></div>
              <div class="chart-caption">
                <span>未佩戴头盔</span>
                <small>占非机动车 15%</small>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" lg="5" md="6">
        <v-card class="surface-card analysis-card h-100">
          <v-card-title class="text-subtitle-1 font-weight-bold px-4 pt-4">
            <v-icon start color="warning">mdi-trending-up</v-icon>
            未佩戴头盔趋势
          </v-card-title>
          <v-divider class="mx-4 mt-2"></v-divider>

          <v-card-text class="chart-card-body">
            <div ref="trendChartElement" class="trend-chart" />
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" lg="6" md="12" class="mt-2">
        <v-card class="surface-card analysis-card h-100">
          <v-card-title class="text-subtitle-1 font-weight-bold px-4 pt-4">
            <v-icon start color="primary">mdi-poll</v-icon>
            小时数据分布
          </v-card-title>
          <v-divider class="mx-4 mt-2"></v-divider>

          <v-card-text class="chart-card-body chart-card-body--large">
            <div ref="hourlyChartElement" class="analysis-hourly-chart" />
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" lg="6" md="12" class="mt-2">
        <v-card class="surface-card analysis-card h-100 d-flex flex-column">
          <v-card-title class="text-subtitle-1 font-weight-bold px-4 pt-4">
            <v-icon start color="success">mdi-map-marker-radius</v-icon>
            摄像头网点分布
          </v-card-title>
          <v-divider class="mx-4 mt-2"></v-divider>

          <v-card-text class="pa-4 flex-grow-1">
            <div class="map-container rounded-lg overflow-hidden border">
              <BMap
                v-if="mapAk"
                height="340px"
                :ak="mapAk"
                :center="{ lng: 106.577667, lat: 29.497096 }"
                :enable-scroll-wheel-zoom="true"
                :tilt="63"
                :zoom="13"
                :minZoom="3"
              >
                <BZoom />
                <BMarker
                  title="摄像头1"
                  :position="{ lng: 106.577667, lat: 29.497096 }"
                  :offset="{ x: 0, y: markerY }"
                  :icon="markerIcon"
                />
                <BMarker
                  v-for="(item, index) in cameras"
                  :key="index"
                  :title="item.name"
                  :position="item.position"
                  :icon="markerIcon"
                />
              </BMap>
              <div v-else class="map-placeholder d-flex align-center justify-center pa-6 text-center">
                请在 .env.local 中配置百度地图 AK
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts" setup>
import { ref, nextTick, onMounted, onBeforeUnmount } from "vue";
import { init as initChart, type ECharts, type EChartsCoreOption } from "@/plugins/echarts";
import { BMap, BZoom, BMarker } from "vue3-baidu-map-gl";
import cameraMarker from "@/assets/camera2.png";
import { appConfig } from "@/config";

const mapAk = appConfig.baiduMapAk;
const markerIcon = { imageUrl: cameraMarker, imageSize: { width: 50, height: 50 } };

// --- 数据定义 ---
const cameras = ref([
  { name: "摄像头2", position: { lng: 106.577667, lat: 29.497096 } },
  { name: "摄像头3", position: { lng: 106.577667, lat: 29.497096 } }
]);

const allCameraList = ref(["001", "002", "003", "004", "005", "006", "007", "008", "009", "010"]);
const camera1 = ref("001");

// --- 动画与实例管理 ---
const markerY = ref(0);
let direction = -1;
let jumpInterval: ReturnType<typeof setInterval> | undefined;
let myChart1: ECharts | null = null;
let myChart2: ECharts | null = null;
let trendChart: ECharts | null = null;
let hourlyChart: ECharts | null = null;
let chartResizeObserver: ResizeObserver | null = null;
const pieChartOne = ref<HTMLElement | null>(null);
const pieChartTwo = ref<HTMLElement | null>(null);
const trendChartElement = ref<HTMLElement | null>(null);
const hourlyChartElement = ref<HTMLElement | null>(null);

const updateY = () => {
  markerY.value += direction;
  if (markerY.value <= -20 || markerY.value >= 0) {
    direction *= -1;
  }
};

// --- ECharts 配置 ---
const getBasePieOption = (value: number, total: number, name: string, color: string): EChartsCoreOption => ({
  animationDuration: 650,
  tooltip: {
    trigger: "item",
    formatter: "{b}<br/>{c} ({d}%)",
    backgroundColor: "rgba(255, 255, 255, 0.96)",
    borderColor: "#dbe5f3",
    textStyle: { color: "#1c2b4a" },
  },
  series: [
    {
      type: "pie",
      center: ["50%", "49%"],
      radius: ["58%", "78%"],
      startAngle: 90,
      label: { show: false },
      labelLine: { show: false },
      emphasis: { scale: false },
      itemStyle: { borderColor: "#ffffff", borderWidth: 3, borderRadius: 8 },
      data: [
        {
          value,
          name,
          itemStyle: { color },
          label: {
            show: true,
            position: "center",
            formatter: [`{value|${value}}`, `{percent|${total ? Math.round((value / total) * 100) : 0}%}`].join("\n"),
            rich: {
              value: { color, fontSize: 27, lineHeight: 32, fontWeight: 800, fontFamily: "Arial" },
              percent: { color: "#718096", fontSize: 12, lineHeight: 20 },
            },
          },
        },
        {
          value: Math.max(total - value, 0),
          name: "其他流量",
          itemStyle: { color: "#edf2f8" },
          label: { show: false },
        },
      ],
    },
  ],
});

const chartHours = ["6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21"];
const trendOption: EChartsCoreOption = {
  color: ["#ef4444"],
  tooltip: { trigger: "axis" },
  grid: { left: 42, right: 18, top: 18, bottom: 32 },
  xAxis: { type: "category", data: chartHours, axisLine: { lineStyle: { color: "#cbd5e1" } } },
  yAxis: { type: "value", splitLine: { lineStyle: { color: "#f1f5f9" } } },
  series: [{ type: "line", name: "未佩戴头盔", smooth: true, areaStyle: { opacity: 0.12 }, data: [5, 25, 5, 15, 10, 15, 28, 10, 20, 22, 25, 10, 20, 8, 3, 1] }],
};
const hourlyOption: EChartsCoreOption = {
  color: ["#3b82f6", "#10b981", "#ef4444"],
  tooltip: { trigger: "axis", axisPointer: { type: "shadow" } },
  legend: { top: 8, left: "center", itemWidth: 12, itemHeight: 8 },
  grid: { left: 18, right: 18, top: 54, bottom: 18, containLabel: true },
  xAxis: {
    type: "category",
    data: chartHours,
    axisTick: { show: false },
    axisLabel: { color: "#718096", fontSize: 11, interval: 0 },
    axisLine: { lineStyle: { color: "#dbe3ee" } },
  },
  yAxis: {
    type: "value",
    minInterval: 1,
    axisLabel: { color: "#718096" },
    splitLine: { lineStyle: { color: "#edf2f7", type: "dashed" } },
  },
  series: [
    {
      type: "bar",
      name: "总流量",
      barMaxWidth: 15,
      itemStyle: { borderRadius: [5, 5, 0, 0] },
      data: [35, 80, 65, 45, 35, 50, 62, 20, 35, 15, 85, 75, 85, 73, 63, 52],
    },
    {
      type: "bar",
      name: "非机动车",
      barMaxWidth: 15,
      itemStyle: { borderRadius: [5, 5, 0, 0] },
      data: [12, 30, 15, 15, 15, 20, 42, 25, 15, 15, 45, 35, 45, 29, 19, 8],
    },
    {
      type: "bar",
      name: "未佩戴头盔",
      barMaxWidth: 15,
      itemStyle: { borderRadius: [5, 5, 0, 0] },
      data: [5, 25, 5, 15, 10, 15, 28, 10, 20, 22, 25, 10, 20, 8, 3, 1],
    },
  ],
};

// --- 生命周期 ---
const handleResize = () => {
  myChart1?.resize();
  myChart2?.resize();
  trendChart?.resize();
  hourlyChart?.resize();
};

onMounted(async () => {
  // 开启跳跃动画
  jumpInterval = setInterval(updateY, 32);

  await nextTick();

  // 初始化 ECharts
  const dom1 = pieChartOne.value;
  const dom2 = pieChartTwo.value;
  const trendDom = trendChartElement.value;
  const hourlyDom = hourlyChartElement.value;
  if (dom1) myChart1 = initChart(dom1);
  if (dom2) myChart2 = initChart(dom2);
  if (trendDom) trendChart = initChart(trendDom);
  if (hourlyDom) hourlyChart = initChart(hourlyDom);

  // 设置清爽的配色方案
  myChart1?.setOption(getBasePieOption(148, 286, "非机动车流量", "#0ea5e9"));
  myChart2?.setOption(getBasePieOption(22, 148, "未佩戴头盔", "#ef4444"));
  trendChart?.setOption(trendOption);
  hourlyChart?.setOption(hourlyOption);

  const chartElements = [dom1, dom2, trendDom, hourlyDom].filter(
    (element): element is HTMLElement => element !== null,
  );
  chartResizeObserver = new ResizeObserver(() => {
    window.requestAnimationFrame(handleResize);
  });
  chartElements.forEach((element) => chartResizeObserver?.observe(element));
  window.requestAnimationFrame(handleResize);

  // 监听窗口大小变化以重绘图表
  window.addEventListener("resize", handleResize);
});

onBeforeUnmount(() => {
  // 必须清理，防止内存泄漏和路由报错
  if (jumpInterval) clearInterval(jumpInterval);
  window.removeEventListener("resize", handleResize);
  chartResizeObserver?.disconnect();
  myChart1?.dispose();
  myChart2?.dispose();
  trendChart?.dispose();
  hourlyChart?.dispose();
});
</script>

<style scoped>
.dashboard-container {
  min-height: calc(100vh - var(--app-header-height));
  padding: 28px;
  background:
    radial-gradient(circle at 90% 0%, rgba(8, 169, 196, 0.07), transparent 26%),
    transparent;
}

.heading-actions {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 10px;
}

.analysis-card {
  overflow: hidden;
  background: rgba(255, 255, 255, 0.94);
}

.analysis-card :deep(.v-card-title) {
  color: #1c2b4a;
  font-size: 15px !important;
  letter-spacing: -0.01em;
}

.analysis-card :deep(.v-card-title .v-icon) {
  width: 34px;
  height: 34px;
  margin-inline-end: 9px !important;
  border-radius: 10px;
  background: rgba(49, 87, 246, 0.08);
}

.analysis-card :deep(.v-divider) {
  opacity: 0.55;
}

/* Flexbox 工具类间距 */
.gap-1 {
  gap: 4px;
}

/* 圆环图表容器 */
.chart-box {
  min-width: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.stats-chart-content {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  align-items: center;
  min-height: 205px;
  padding: 12px 18px 18px !important;
  gap: 8px;
}

.pie-chart {
  width: 100%;
  height: 150px;
}

.chart-caption {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: -2px;
  color: #33415c;
  font-size: 13px;
  font-weight: 700;
  line-height: 1.5;
}

.chart-caption small {
  color: #8a96aa;
  font-size: 10px;
  font-weight: 500;
}

.chart-card-body {
  min-height: 205px;
  padding: 8px 12px 12px !important;
}

.chart-card-body--large {
  min-height: 360px;
}

/* 地图容器：增加细边框，防止纯白背景融色 */
.map-container {
  border: 1px solid #e2e8f0;
  background-color: #f8fafc;
  border-radius: 16px !important;
  box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.7);
}

.trend-chart { width: 100%; height: 185px; }
.analysis-hourly-chart { width: 100%; height: 350px; }

.map-placeholder {
  height: 340px;
  color: #64748b;
  background: linear-gradient(135deg, #eff6ff, #f8fafc);
}

/* 重置部分 Vuetify 标题的行高 */
:deep(.v-card-title) {
  line-height: 1.5;
}

@media (max-width: 960px) {
  .dashboard-container {
    padding: 22px 18px;
  }
}

@media (max-width: 600px) {
  .dashboard-container {
    padding: 18px 12px;
  }

  .heading-actions {
    justify-content: flex-start;
  }

  .chart-box {
    width: auto;
  }

  .pie-chart {
    height: 140px;
  }

  .stats-chart-content {
    min-height: 196px;
    padding-inline: 6px !important;
  }
}
</style>
