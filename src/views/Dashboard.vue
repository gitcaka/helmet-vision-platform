<template>
  <BMap
    class="bg-map"
    height="calc(100vh - 64px)"
    ak="0HKOG2X2X9rW9MOdwlO5owKFDatvEgBt"
    :center="{ lng: 106.577667, lat: 29.497096 }"
    :enable-scroll-wheel-zoom="true"
    :tilt="63"
    :zoom="21"
    :minZoom="3"
    :enablePinchToZoom="true"
    :enableTraffic="true"
  >
    <BZoom />
    <BMarker
      id="camera1"
      title="摄像头1"
      :position="{ lng: 106.57767, lat: 29.497665 }"
      :icon="{ imageUrl: 'src/assets/camera2.png', imageSize: { width: 60, height: 60 } }"
    />
    <BMarker
      id="camera2"
      title="摄像头2"
      :position="{ lng: 106.577667, lat: 29.497096 }"
      :offset="{ x: 0, y: markerY }"
      :icon="{ imageUrl: 'src/assets/camera2.png', imageSize: { width: 60, height: 60 } }"
    />
  </BMap>

  <v-navigation-drawer class="bg-transparent pointer-events-none" :width="380">
    <div class="pa-4 pointer-events-auto h-100 d-flex flex-column gap-4">
      <v-card class="glass-panel" prepend-icon="mdi-chart-donut" title="今日统计">
        <v-divider class="border-opacity-25"></v-divider>
        <v-card-text class="d-flex justify-space-around pa-2">
          <div class="chart-box">
            <div id="echart1" class="pie-chart"></div>
            <div class="text-caption text-grey-lighten-1 mt-1">非机动车流量</div>
          </div>
          <div class="chart-box">
            <div id="echart2" class="pie-chart"></div>
            <div class="text-caption text-grey-lighten-1 mt-1">未佩戴头盔</div>
          </div>
        </v-card-text>
      </v-card>

      <v-card class="glass-panel" prepend-icon="mdi-poll" title="小时数据">
        <v-divider class="border-opacity-25"></v-divider>
        <v-card-text class="pa-1">
          <apexchart
            type="bar"
            height="300"
            :options="chartOptions1"
            :series="lineChart1.series"
          />
        </v-card-text>
      </v-card>
    </div>
  </v-navigation-drawer>

  <v-navigation-drawer location="right" class="bg-transparent pointer-events-none" :width="380">
    <div class="pa-4 pointer-events-auto h-100 d-flex flex-column gap-4">
      <v-card class="glass-panel" prepend-icon="mdi-video-outline" title="实时视频">
        <v-divider class="border-opacity-25"></v-divider>
        <v-card-text class="pa-2">
          <div class="video-container rounded overflow-hidden">
            <video
              autoplay
              loop
              muted
              src="@/assets/test06.mp4"
              class="w-100 d-block"
            ></video>
          </div>
        </v-card-text>
      </v-card>

      <v-card class="glass-panel d-flex flex-column flex-grow-1" prepend-icon="mdi-camera-iris" title="实时抓拍">
        <v-divider class="border-opacity-25"></v-divider>
        <v-card-text class="pa-2 flex-grow-1 overflow-hidden">
          <v-virtual-scroll :items="logData" height="100%" class="custom-scrollbar pr-2">
            <template v-slot:default="{ item }">
              <v-card class="capture-card mb-3 pa-2 border">
                <div class="text-subtitle-2 font-weight-bold text-teal-accent-3 mb-2">
                  {{ item.title }}
                </div>
                <v-row no-gutters>
                  <v-col cols="5">
                    <v-img :src="item.img" cover class="rounded bg-grey-darken-3 h-100"></v-img>
                  </v-col>
                  <v-col cols="7" class="pl-3 text-caption d-flex flex-column justify-space-between">
                    <div>
                      <span class="text-grey-lighten-1">置信度：</span>
                      <span class="text-red-accent-2 font-weight-bold">{{ item.score }}</span>
                    </div>
                    <div>
                      <span class="text-grey-lighten-1">时间：</span>
                      <span>{{ item.time }}</span>
                    </div>
                    <div class="text-truncate" :title="'摄像头编号：' + item.cameraId">
                      <span class="text-grey-lighten-1">编号：</span>
                      <span>{{ item.cameraId }}</span>
                    </div>
                    <div class="text-truncate" :title="item.location">
                      <span class="text-grey-lighten-1">地点：</span>
                      <span style="font-size: 10px">{{ item.location }}</span>
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
import { BMap, BZoom, BMarker } from "vue3-baidu-map-gl";
import { ref, onMounted, onBeforeUnmount, computed } from "vue";
import * as echarts from "echarts";
import io from "socket.io-client";

// --- 状态与变量 ---
const markerY = ref(0);
let direction = -1;
const logData = ref([]);
const trafficData = ref([]);

// 定时器与实例引用 (必须在 setup 顶层声明，方便后续销毁)
let jumpInterval: NodeJS.Timeout;
let dataUpdateInterval: NodeJS.Timeout;
let myChart1: echarts.ECharts | null = null;
let myChart2: echarts.ECharts | null = null;
let socket: any = null;

// --- 动画逻辑 ---
const updateY = () => {
  markerY.value += direction;
  if (markerY.value <= -20 || markerY.value >= 0) {
    direction *= -1;
  }
};

// --- ECharts 基础配置 ---
const getBasePieOption = (seriesName: string, activeColor: string): echarts.EChartsOption => ({
  tooltip: { trigger: "item", backgroundColor: 'rgba(0,0,0,0.7)', textStyle: { color: '#fff' } },
  series: [
    {
      type: "pie",
      radius: ["65%", "90%"],
      label: {
        show: true,
        position: "center",
        formatter: ["{a|0}", "{b|0%}"].join("\n"),
        rich: {
          a: { color: "#08d9d6", fontSize: 24, lineHeight: 32, fontWeight: "bold" },
          b: { fontSize: 12, color: "#ccc" },
        },
      },
      data: [
        { value: 0, name: seriesName, itemStyle: { color: activeColor } },
        { value: 0, name: "其他流量", itemStyle: { color: "rgba(255, 255, 255, 0.1)" } },
      ],
    },
  ],
});

// --- ApexCharts 配置 ---
const chartOptions1 = computed(() => ({
  chart: { type: "bar", fontFamily: `inherit`, foreColor: "#cfd8dc", stacked: true, toolbar: { show: false } },
  colors: ["#3498db", "#2ecc71", "#e74c3c"],
  plotOptions: { bar: { columnWidth: "60%", borderRadius: 2 } },
  xaxis: {
    type: "category",
    categories: ["6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17"],
    axisBorder: { show: false },
    axisTicks: { show: false }
  },
  yaxis: { grid: { borderColor: 'rgba(255,255,255,0.1)' } },
  legend: { position: "bottom", markers: { radius: 12 } },
  grid: { borderColor: 'rgba(255,255,255,0.05)', strokeDashArray: 4 },
  tooltip: { theme: "dark" },
}));

const lineChart1 = {
  series: [
    { name: "总流量", data: [35, 80, 65, 45, 35, 50, 62, 20, 35, 15, 85, 75] },
    { name: "非机动车", data: [12, 30, 15, 15, 15, 20, 42, 25, 15, 15, 45, 35] },
    { name: "未佩戴头盔", data: [5, 25, 5, 15, 10, 15, 28, 10, 20, 22, 25, 10] },
  ],
};

// --- 生命周期钩子 ---
onMounted(() => {
  // 1. 初始化图表
  const chartDom1 = document.getElementById("echart1");
  const chartDom2 = document.getElementById("echart2");
  if (chartDom1) myChart1 = echarts.init(chartDom1);
  if (chartDom2) myChart2 = echarts.init(chartDom2);

  myChart1?.setOption(getBasePieOption("非机动车流量", "#00d2ff"));
  myChart2?.setOption(getBasePieOption("佩戴头盔", "#3a7bd5"));

  // 2. 地图标记动画
  jumpInterval = setInterval(updateY, 32);

  // 3. Socket 连接
  socket = io("http://localhost:5000");
  socket.on("connect", () => {
    console.log("Connected to server");
    socket.emit("get_log_data");
  });

  socket.on("data_update", (log_data_list: any, traffic_data_list: any) => {
    logData.value = log_data_list;
    trafficData.value = traffic_data_list;
  });

  // 4. 定时更新图表数据 (增加容错判断)
  dataUpdateInterval = setInterval(() => {
    if (!trafficData.value || trafficData.value.length === 0) return; // 容错：没数据时跳过更新

    const currentData: any = trafficData.value[0];
    const safeTotal = currentData.total || 1; // 防止除以0
    const safeEle = currentData.ele || 1;

    const proportion1 = ((currentData.ele / safeTotal) * 100).toFixed(0);
    const proportion2 = ((currentData.helmet / safeEle) * 100).toFixed(0);

    myChart1?.setOption({
      series: [{
        label: { formatter: `{a|${currentData.ele}}\n{b|${proportion1}%}` },
        data: [
          { value: currentData.ele, name: "非机动车流量" },
          { value: currentData.total - currentData.ele, name: "其他流量" }, // 逻辑修正：其他应该是 总数 - 非机动车
        ]
      }]
    });

    myChart2?.setOption({
      series: [{
        label: { formatter: `{a|${currentData.helmet}}\n{b|${proportion2}%}` },
        data: [
          { value: currentData.helmet, name: "佩戴头盔" },
          { value: currentData.noHelmet, name: "未佩戴头盔" },
        ]
      }]
    });
  }, 3000);
});

// --- 极其重要的清理环节 ---
onBeforeUnmount(() => {
  clearInterval(jumpInterval);
  clearInterval(dataUpdateInterval); // 防止内存泄漏
  myChart1?.dispose(); // 销毁 ECharts 实例
  myChart2?.dispose();
  if (socket) socket.disconnect(); // 断开 Socket 连接
});
</script>

<style scoped>
/* 地图底边固定 */
.bg-map {
  position: fixed;
  top: 64px;
  left: 0;
  width: 100%;
  z-index: 0;
}

/* 穿透点击：使得在空白处可以拖拽地图，而在卡片上正常操作 */
.pointer-events-none { pointer-events: none; }
.pointer-events-auto { pointer-events: auto; }
.gap-4 { gap: 1rem; }

/* 核心美化：毛玻璃质感面板 */
.glass-panel {
  background: rgba(12, 25, 56, 0.75) !important; /* 深空蓝，增加透明度 */
  backdrop-filter: blur(12px); /* 毛玻璃模糊 */
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #fff !important;
  box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
  border-radius: 12px;
}

/* 抓拍数据小卡片 */
.capture-card {
  background: rgba(255, 255, 255, 0.05) !important;
  border-color: rgba(255, 255, 255, 0.1) !important;
  transition: transform 0.2s, background 0.2s;
}
.capture-card:hover {
  background: rgba(255, 255, 255, 0.1) !important;
  transform: translateX(-4px);
}

.chart-box {
  width: 45%;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.pie-chart {
  width: 100%;
  height: 110px;
}

/* 隐藏外层抽屉滚动条，美化内部数据流滚动条 */
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: rgba(0, 210, 255, 0.4);
  border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 210, 255, 0.8);
}
</style>
