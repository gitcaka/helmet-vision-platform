import type { ThemeDefinition } from "vuetify";

export const helmetLightTheme: ThemeDefinition = {
  dark: false,
  colors: {
    background: "#F3F6FB",
    surface: "#FFFFFF",
    primary: "#3157F6",
    secondary: "#08A9C4",
    success: "#17A673",
    info: "#1487E3",
    warning: "#E99A24",
    error: "#E84C5B",
    lightprimary: "#EEF3FF",
    lightsecondary: "#E9FAFD",
    darkText: "#12213F",
    lightText: "#64748B",
    borderLight: "#E2E8F0",
    containerBg: "#F3F6FB",
  },
  variables: {
    "border-color": "30, 55, 94",
    "border-opacity": 0.1,
    "high-emphasis-opacity": 0.92,
    "medium-emphasis-opacity": 0.68,
  },
};
