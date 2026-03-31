import { defineStore } from "pinia";
import { router } from "@/router";
import axios from "axios";

// 💡 核心开关：是否启用真实后端/数据库
// true = 请求 localhost:5000； false = 使用本地模拟数据直接登录
const ENABLE_BACKEND = false;

export const useAuthStore = defineStore({
  id: "auth",
  state: () => ({
    // 从本地存储初始化状态，使用户能够保持登录状态
    /* eslint-disable-next-line @typescript-eslint/ban-ts-comment */
    // @ts-ignore
    user: JSON.parse(localStorage.getItem("user")),
    returnUrl: null,
  }),
  actions: {
    async login(username: string, password: string) {
      let userData;

      if (ENABLE_BACKEND) {
        // ==========================================
        // 模式 1：开启后端（真实请求）
        // ==========================================
        try {
          const response = await axios.post("http://localhost:5000/login", {
            username,
            password,
          });
          // 注意：axios 的返回值包了一层，通常后端实际返回的数据在 response.data 中
          userData = response.data;
        } catch (error) {
          console.error("后端登录请求失败:", error);
          throw error; // 抛出错误让页面捕获并提示
        }
      } else {
        // ==========================================
        // 模式 2：关闭后端（模拟登录，方便前端纯 UI 调试）
        // ==========================================
        console.log("当前为模拟登录模式，未连接后端/数据库！");

        // 模拟网络延迟 500ms
        await new Promise((resolve) => setTimeout(resolve, 500));

        // 随便写一个模拟的校验逻辑
        if (username === "admin" && password === "123456") {
          userData = {
            id: 1,
            username: "admin",
            token: "mock-jwt-token-123456",
            role: "admin"
          };
        } else {
          throw new Error("模拟登录失败：请输入账号 admin，密码 123456");
        }
      }

      // ==========================================
      // 公共逻辑：更新状态与跳转
      // ==========================================

      // 更新pinia状态
      this.user = userData;
      // 将用户详细信息和jwt存储在本地存储中，以便在页面刷新之间保持用户登录
      localStorage.setItem("user", JSON.stringify(userData));
      // 重定向到以前的url或默认重定向到主页
      router.push(this.returnUrl || "/main");
    },

    logout() {
      this.user = null;
      localStorage.removeItem("user");
      router.push("/login");
    },
  },
});
