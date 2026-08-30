import axios, { AxiosError } from "axios";
import { appConfig } from "@/config";

interface ApiErrorBody {
  text?: string;
  message?: string;
}

export const http = axios.create({
  baseURL: appConfig.apiUrl,
  timeout: 10_000,
  withCredentials: true,
});

export const getErrorMessage = (error: unknown, fallback = "请求失败，请稍后重试") => {
  if (error instanceof AxiosError) {
    const data = error.response?.data as ApiErrorBody | undefined;
    return data?.text || data?.message || error.message || fallback;
  }
  if (error instanceof Error) return error.message;
  return fallback;
};
