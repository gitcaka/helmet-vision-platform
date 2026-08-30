const defaultApiUrl = "http://localhost:5000";

export const appConfig = {
  apiUrl: (import.meta.env.VITE_API_URL || defaultApiUrl).replace(/\/$/, ""),
  baiduMapAk: import.meta.env.VITE_BAIDU_MAP_AK || "",
  useMockData: import.meta.env.VITE_USE_MOCK_DATA !== "false",
};

export const apiAssetUrl = (path: string) => {
  if (!path || /^(?:https?:|data:|blob:)/i.test(path)) return path;
  return new URL(path.replace(/^\//, ""), `${appConfig.apiUrl}/`).href;
};

export const videoFeedUrl = `${appConfig.apiUrl}/video_feed`;
