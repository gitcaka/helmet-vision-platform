import { defineStore } from "pinia";
import { appConfig } from "@/config";
import { getErrorMessage, http } from "@/services/http";

export interface AuthUser {
  id: number;
  username: string;
  role?: string;
}

interface AuthResponse {
  ok: boolean;
  text: AuthUser;
}

const storageKey = "helmet-user";

const readMockUser = (): AuthUser | null => {
  try {
    const value = localStorage.getItem(storageKey);
    return value ? (JSON.parse(value) as AuthUser) : null;
  } catch {
    localStorage.removeItem(storageKey);
    return null;
  }
};

export const useAuthStore = defineStore({
  id: "auth",
  state: () => ({
    user: null as AuthUser | null,
    returnUrl: null as string | null,
    initialized: false,
  }),
  actions: {
    async initialize() {
      if (this.initialized) return;

      if (appConfig.useMockData) {
        this.user = readMockUser();
      } else {
        try {
          const response = await http.get<AuthResponse>("/api/me");
          this.user = response.data.text;
        } catch {
          this.user = null;
        }
      }
      this.initialized = true;
    },

    async login(username: string, password: string) {
      let userData: AuthUser;

      if (appConfig.useMockData) {
        await new Promise((resolve) => window.setTimeout(resolve, 350));
        if (username !== "admin" || password !== "123456") {
          throw new Error("示例登录失败：请输入账号 admin，密码 123456");
        }
        userData = { id: 1, username: "admin", role: "admin" };
        localStorage.setItem(storageKey, JSON.stringify(userData));
      } else {
        try {
          const response = await http.post<AuthResponse>("/login", { username, password });
          userData = response.data.text;
        } catch (error) {
          throw new Error(getErrorMessage(error, "登录失败"));
        }
      }

      this.user = userData;
      this.initialized = true;
      return userData;
    },

    async logout() {
      if (!appConfig.useMockData) {
        try {
          await http.post("/logout");
        } catch {
          // 即使服务不可用，也要清理本地登录态。
        }
      }
      this.user = null;
      localStorage.removeItem(storageKey);
    },
  },
});
