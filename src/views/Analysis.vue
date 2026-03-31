<template>
  <div class="dashboard-container pa-4 bg-grey-lighten-4 min-vh-100">
    <v-row dense>
      <v-col cols="12" lg="2" md="12">
        <v-card class="h-100 d-flex flex-column" elevation="2" rounded="lg">
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
        <v-card class="h-100" elevation="2" rounded="lg">
          <v-card-title class="text-subtitle-1 font-weight-bold px-4 pt-4">
            <v-icon start color="info">mdi-chart-donut</v-icon>
            今日统计
          </v-card-title>
          <v-divider class="mx-4 mt-2"></v-divider>

          <v-card-text class="pa-2 d-flex justify-space-around align-start h-100  mt-5">
            <div class="chart-box">
              <div id="echart1" class="pie-chart"></div>
              <div class="text-caption font-weight-medium text-grey-darken-2 mt-2">非机动车流量</div>
            </div>
            <div class="chart-box">
              <div id="echart2" class="pie-chart"></div>
              <div class="text-caption font-weight-medium text-grey-darken-2 mt-2">未佩戴头盔</div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" lg="5" md="6">
        <v-card class="h-100" elevation="2" rounded="lg">
          <v-card-title class="text-subtitle-1 font-weight-bold px-4 pt-4">
            <v-icon start color="warning">mdi-trending-up</v-icon>
            未佩戴头盔趋势
          </v-card-title>
          <v-divider class="mx-4 mt-2"></v-divider>

          <v-card-text class="pa-2">
            <apexchart
              type="line"
              height="180"
              width="100%"
              :options="chartOptions1"
              :series="lineChart2.series"
            ></apexchart>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" lg="6" md="12" class="mt-2">
        <v-card class="h-100" elevation="2" rounded="lg">
          <v-card-title class="text-subtitle-1 font-weight-bold px-4 pt-4">
            <v-icon start color="primary">mdi-poll</v-icon>
            小时数据分布
          </v-card-title>
          <v-divider class="mx-4 mt-2"></v-divider>

          <v-card-text class="pa-2">
            <apexchart
              type="bar"
              height="340"
              width="100%"
              :options="chartOptions1"
              :series="lineChart1.series"
            ></apexchart>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" lg="6" md="12" class="mt-2">
        <v-card class="h-100 d-flex flex-column" elevation="2" rounded="lg">
          <v-card-title class="text-subtitle-1 font-weight-bold px-4 pt-4">
            <v-icon start color="success">mdi-map-marker-radius</v-icon>
            摄像头网点分布
          </v-card-title>
          <v-divider class="mx-4 mt-2"></v-divider>

          <v-card-text class="pa-4 flex-grow-1">
            <div class="map-container rounded-lg overflow-hidden border">
              <BMap
                height="340px"
                ak="0HKOG2X2X9rW9MOdwlO5owKFDatvEgBt"
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
                  :icon="{ imageUrl: 'src/assets/camera2.png', imageSize: { width: 50, height: 50 } }"
                />
                <BMarker
                  v-for="(item, index) in cameras"
                  :key="index"
                  :title="item.name"
                  :position="item.position"
                  :icon="{ imageUrl: 'src/assets/camera2.png', imageSize: { width: 50, height: 50 } }"
                />
              </BMap>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, onBeforeUnmount, computed } from "vue";
import * as echarts from "echarts";
import { BMap, BZoom, BMarker } from "vue3-baidu-map-gl";

// --- 数据定义 ---
const cameras = ref([
  { name: "摄像头2", position: { lng: 106.577667, lat: 29.497096 } },
  { name: "摄像头3", position: { lng: 106.577667, lat: 29.497096 } }
]);

const allCameraList = ref(["001", "002", "003", "004", "005", "006", "007", "008", "009", "010"]);
const camera1 = ref("001");

// --- 动画与实例管理 ---
let markerY = ref(0);
let direction = -1;
let jumpInterval: NodeJS.Timeout;
let myChart1: echarts.ECharts | null = null;
let myChart2: echarts.ECharts | null = null;

const updateY = () => {
  markerY.value += direction;
  if (markerY.value <= -20 || markerY.value >= 0) {
    direction *= -1;
  }
};

// --- ECharts 配置 ---
const getBasePieOption = (value: number, name: string, percent: string, color: string): echarts.EChartsOption => ({
  tooltip: { trigger: "item", backgroundColor: 'rgba(255, 255, 255, 0.9)', textStyle: { color: '#333' } },
  series: [
    {
      type: "pie",
      radius: ["55%", "85%"],
      label: {
        show: true,
        position: "center",
        formatter: [`{a|${value}}`, `{b|${percent}}`].join("\n"),
        rich: {
          a: { color: color, fontSize: 24, lineHeight: 30, fontWeight: "bold", fontFamily: 'DIN, Arial' },
          b: { fontSize: 12, color: "#666" },
        },
      },
      data: [
        { value: value, name: name, itemStyle: { color: color } },
        { value: 1000, name: "其他流量", itemStyle: { color: "#f0f2f5" } },
      ],
    },
  ],
});

// --- ApexCharts 配置 ---
const chartOptions1 = computed(() => ({
  chart: { type: "bar", fontFamily: `inherit`, foreColor: "#475569", toolbar: { show: false } },
  colors: ["#3b82f6", "#10b981", "#ef4444"], // 换成更现代明亮的蓝/绿/红色
  plotOptions: { bar: { columnWidth: "55%", borderRadius: 2 } },
  xaxis: {
    type: "category",
    categories: ["6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21"],
    axisBorder: { show: false },
    axisTicks: { show: false }
  },
  yaxis: {
    labels: { style: { colors: '#94a3b8' } }
  },
  legend: { position: "bottom", markers: { radius: 12 }, itemMargin: { horizontal: 10, vertical: 0 } },
  grid: { show: true, borderColor: '#f1f5f9', strokeDashArray: 4 },
  tooltip: { theme: "light" },
}));

const lineChart1 = {
  series: [
    { name: "总流量", data: [35, 80, 65, 45, 35, 50, 62, 20, 35, 15, 85, 75, 85, 73, 63, 52] },
    { name: "非机动车", data: [12, 30, 15, 15, 15, 20, 42, 25, 15, 15, 45, 35, 45, 29, 19, 8] },
    { name: "未佩戴头盔", data: [5, 25, 5, 15, 10, 15, 28, 10, 20, 22, 25, 10, 20, 8, 3, 1] },
  ],
};

const lineChart2 = {
  series: [{ name: "非机动车", data: [12, 30, 15, 15, 15, 20, 42, 25, 15, 15, 45, 35, 45, 29, 19, 8] }],
};

// --- 生命周期 ---
const handleResize = () => {
  myChart1?.resize();
  myChart2?.resize();
};

onMounted(() => {
  // 开启跳跃动画
  jumpInterval = setInterval(updateY, 32);

  // 初始化 ECharts
  const dom1 = document.getElementById("echart1");
  const dom2 = document.getElementById("echart2");
  if (dom1) myChart1 = echarts.init(dom1);
  if (dom2) myChart2 = echarts.init(dom2);

  // 设置清爽的配色方案
  myChart1?.setOption(getBasePieOption(148, "非机动车流量", "20%", "#0ea5e9")); // 天蓝色
  myChart2?.setOption(getBasePieOption(22, "佩戴头盔", "15%", "#10b981"));    // 翠绿色

  // 监听窗口大小变化以重绘图表
  window.addEventListener("resize", handleResize);
});

onBeforeUnmount(() => {
  // 必须清理，防止内存泄漏和路由报错
  clearInterval(jumpInterval);
  window.removeEventListener("resize", handleResize);
  myChart1?.dispose();
  myChart2?.dispose();
});
</script>

<style scoped>
/* 确保页面至少占满屏幕高度 */
.min-vh-100 {
  min-height: calc(100vh - 64px);
}

/* Flexbox 工具类间距 */
.gap-1 {
  gap: 4px;
}

/* 圆环图表容器 */
.chart-box {
  width: 45%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.pie-chart {
  width: 100%;
  height: 110px;
}

/* 地图容器：增加细边框，防止纯白背景融色 */
.map-container {
  border: 1px solid #e2e8f0;
  background-color: #f8fafc;
}

/* 重置部分 Vuetify 标题的行高 */
:deep(.v-card-title) {
  line-height: 1.5;
}
</style>
