import { defineStore } from "pinia";
import { io, type Socket } from "socket.io-client";
import noHelmetImage from "@/assets/NoHelmet1.png";
import { apiAssetUrl, appConfig } from "@/config";
import { getErrorMessage, http } from "@/services/http";

export interface CaptureLog {
  id: number;
  event_id?: string;
  type: string;
  time: string;
  camera: string;
  score: string;
  title: string;
  location: string;
  img: string;
}

export interface TrafficData {
  id: number;
  date: string;
  total: number;
  ele: number;
  helmet: number;
  noHelmet: number;
}

interface DataResponse {
  ok: boolean;
  logs: CaptureLog[];
  traffic: TrafficData[];
}

let socket: Socket | null = null;
let demoTimer: number | undefined;

const formatTime = () => new Date().toLocaleString("zh-CN", { hour12: false });

const sampleLogs: CaptureLog[] = [
  {
    id: 1,
    event_id: "demo-001",
    type: "no_helmet",
    time: "2026/08/30 09:42:18",
    camera: "CAM-001",
    score: "96.8%",
    title: "检测到未佩戴头盔",
    location: "重庆交通大学交运实验楼107",
    img: noHelmetImage,
  },
  {
    id: 2,
    event_id: "demo-002",
    type: "no_helmet",
    time: "2026/08/30 09:38:06",
    camera: "CAM-002",
    score: "93.5%",
    title: "检测到未佩戴头盔",
    location: "重庆交通大学交运实验楼东侧",
    img: noHelmetImage,
  },
  {
    id: 3,
    event_id: "demo-003",
    type: "helmet",
    time: "2026/08/30 09:31:42",
    camera: "CAM-001",
    score: "98.1%",
    title: "头盔佩戴正常",
    location: "重庆交通大学交运实验楼107",
    img: noHelmetImage,
  },
];

const sampleTraffic: TrafficData = {
  id: 1,
  date: "2026-08-30",
  total: 286,
  ele: 168,
  helmet: 132,
  noHelmet: 36,
};

const normalizeLog = (item: CaptureLog): CaptureLog => ({
  ...item,
  img: item.img ? apiAssetUrl(item.img) : noHelmetImage,
});

export const useDashboardStore = defineStore("dashboard", {
  state: () => ({
    logs: [] as CaptureLog[],
    traffic: [] as TrafficData[],
    connected: false,
    loading: false,
    error: "",
  }),
  actions: {
    async start() {
      this.stop();
      this.loading = true;
      this.error = "";

      if (appConfig.useMockData) {
        this.logs = sampleLogs.map((item) => ({ ...item }));
        this.traffic = [{ ...sampleTraffic }];
        this.connected = true;
        this.loading = false;
        demoTimer = window.setInterval(() => {
          const current = this.traffic[0];
          if (!current) return;
          const helmetDetected = Math.random() > 0.22;
          current.total += 1;
          current.ele += 1;
          if (helmetDetected) current.helmet += 1;
          else current.noHelmet += 1;

          if (!helmetDetected) {
            this.logs.unshift({
              ...sampleLogs[0],
              id: Date.now(),
              event_id: `demo-${Date.now()}`,
              time: formatTime(),
              score: `${(92 + Math.random() * 7).toFixed(1)}%`,
            });
            this.logs = this.logs.slice(0, 20);
          }
        }, 5_000);
        return;
      }

      try {
        const response = await http.get<DataResponse>("/api/data");
        this.logs = response.data.logs.map(normalizeLog);
        this.traffic = response.data.traffic;
      } catch (error) {
        this.error = getErrorMessage(error, "实时数据加载失败");
      } finally {
        this.loading = false;
      }

      socket = io(appConfig.apiUrl, { withCredentials: true });
      socket.on("connect", () => {
        this.connected = true;
        this.error = "";
      });
      socket.on("disconnect", () => {
        this.connected = false;
      });
      socket.on("connect_error", (error) => {
        this.connected = false;
        this.error = `实时连接失败：${error.message}`;
      });
      socket.on("data_update", (logs: CaptureLog[], traffic: TrafficData[]) => {
        this.logs = logs.map(normalizeLog);
        this.traffic = traffic;
      });
      socket.on("log_created", (log: CaptureLog) => {
        this.logs = [normalizeLog(log), ...this.logs].slice(0, 50);
      });
      socket.on("traffic_updated", (traffic: TrafficData) => {
        const existingIndex = this.traffic.findIndex((item) => item.date === traffic.date);
        if (existingIndex >= 0) this.traffic[existingIndex] = traffic;
        else this.traffic.unshift(traffic);
      });
    },

    stop() {
      if (demoTimer !== undefined) {
        window.clearInterval(demoTimer);
        demoTimer = undefined;
      }
      socket?.disconnect();
      socket = null;
      this.connected = false;
    },
  },
});
