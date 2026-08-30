<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from "vue";
import { RouterLink, useRoute } from "vue-router";
import ProfileDD from "./ProfileDD.vue";
import { appConfig } from "@/config";

const route = useRoute();
const formattedDateTime = ref("");
const profileMenuOpen = ref(false);
let updateTimeInterval: ReturnType<typeof setInterval> | undefined;

const navItems = [
  { label: "大屏首页", path: "/Dashboard", icon: "mdi-view-dashboard-outline" },
  { label: "实时监控", path: "/Monitor", icon: "mdi-cctv" },
  { label: "记录分析", path: "/Analysis", icon: "mdi-chart-timeline-variant" },
];
const activeTab = computed(() => navItems.some((item) => item.path === route.path) ? route.path : "none");

function updateTime() {
  formattedDateTime.value = new Intl.DateTimeFormat("zh-CN", {
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  }).format(new Date());
}

onMounted(() => {
  updateTime();
  updateTimeInterval = setInterval(updateTime, 1000);
});

onBeforeUnmount(() => {
  if (updateTimeInterval) clearInterval(updateTimeInterval);
});
</script>

<template>
  <v-app-bar class="app-header" :height="72" elevation="0">
    <div class="header-inner">
      <RouterLink class="header-brand" to="/Dashboard" aria-label="Helmet Vision 大屏首页">
        <span class="brand-mark"><img src="@/assets/logo.png" alt="" /></span>
        <span class="brand-copy">
          <strong>Helmet Vision</strong>
          <small>头盔佩戴智能检测平台</small>
        </span>
      </RouterLink>

      <v-tabs
        :model-value="activeTab"
        :mandatory="false"
        class="header-nav"
        height="54"
        center-active
      >
        <v-tab v-for="item in navItems" :key="item.path" :value="item.path" :to="item.path" class="nav-tab">
          <v-icon :icon="item.icon" size="20" />
          <span class="tab-label">{{ item.label }}</span>
        </v-tab>
      </v-tabs>

      <div class="header-actions">
        <div class="mode-indicator">
          <span class="mode-dot" />
          {{ appConfig.useMockData ? "演示模式" : "实时在线" }}
        </div>
        <div class="header-clock">
          <v-icon icon="mdi-clock-outline" size="16" />
          {{ formattedDateTime }}
        </div>

        <v-menu
          v-model="profileMenuOpen"
          location="bottom end"
          :offset="10"
          :close-on-content-click="false"
          eager
        >
          <template #activator="{ props }">
            <v-btn v-bind="props" icon class="profile-trigger" aria-label="用户菜单">
              <v-avatar size="36" color="rgba(103, 232, 249, 0.16)">
                <v-icon icon="mdi-account-outline" color="cyan-accent-2" size="21" />
              </v-avatar>
            </v-btn>
          </template>
          <v-sheet class="profile-sheet" rounded="xl" width="270" elevation="18">
            <ProfileDD @close-menu="profileMenuOpen = false" />
          </v-sheet>
        </v-menu>
      </div>
    </div>
  </v-app-bar>
</template>

<style scoped lang="scss">
.app-header {
  color: #f8fbff !important;
  background: linear-gradient(110deg, #0b1737 0%, #142d67 58%, #123f70 100%) !important;
  border-bottom: 1px solid rgba(148, 212, 255, 0.14) !important;
  box-shadow: 0 10px 28px rgba(9, 24, 56, 0.2) !important;
}

.header-inner {
  display: grid;
  grid-template-columns: minmax(230px, 1fr) auto minmax(230px, 1fr);
  align-items: center;
  width: 100%;
  height: 100%;
  padding: 0 clamp(16px, 2.2vw, 34px);
  gap: 18px;
}

.header-brand { display: flex; align-items: center; gap: 11px; color: inherit; text-decoration: none; min-width: 0; }
.brand-mark { display: grid; place-items: center; flex: 0 0 auto; width: 40px; height: 40px; border: 1px solid rgba(103, 232, 249, 0.2); border-radius: 12px; background: rgba(255, 255, 255, 0.06); }
.brand-mark img { width: 29px; height: 29px; object-fit: contain; }
.brand-copy { display: flex; flex-direction: column; min-width: 0; }
.brand-copy strong { font-size: 15px; line-height: 1.2; letter-spacing: 0.01em; }
.brand-copy small { margin-top: 3px; color: rgba(221, 237, 255, 0.58); font-size: 10px; letter-spacing: 0.08em; white-space: nowrap; }

.header-nav { align-self: center; }
.nav-tab { min-width: 104px !important; margin: 0 3px; border-radius: 13px !important; color: rgba(229, 240, 255, 0.7) !important; font-size: 13px; font-weight: 650; }
.nav-tab .v-icon { margin-right: 7px; }
.nav-tab.v-tab--selected { color: #fff !important; background: rgba(85, 211, 255, 0.12); box-shadow: inset 0 0 0 1px rgba(103, 232, 249, 0.15); }
.header-nav :deep(.v-tabs-slider) { height: 3px; border-radius: 4px 4px 0 0; color: #55d3ff; }

.header-actions { display: flex; align-items: center; justify-content: flex-end; gap: 12px; min-width: 0; }
.mode-indicator,
.header-clock { display: flex; align-items: center; gap: 7px; color: rgba(226, 239, 255, 0.68); font-size: 11px; white-space: nowrap; }
.mode-indicator { padding: 7px 10px; border: 1px solid rgba(103, 232, 249, 0.13); border-radius: 999px; background: rgba(255, 255, 255, 0.05); }
.mode-dot { width: 7px; height: 7px; border-radius: 50%; background: #34d399; box-shadow: 0 0 0 4px rgba(52, 211, 153, 0.12); }
.profile-trigger { border: 1px solid rgba(103, 232, 249, 0.14); background: rgba(255, 255, 255, 0.05); }
.profile-sheet { overflow: hidden; border: 1px solid rgba(30, 55, 94, 0.1); box-shadow: 0 24px 64px rgba(15, 30, 65, 0.22) !important; }

@media (max-width: 1180px) {
  .header-inner { grid-template-columns: auto 1fr auto; }
  .brand-copy small, .mode-indicator { display: none; }
  .header-nav { justify-self: center; }
}

@media (max-width: 850px) {
  .brand-copy { display: none; }
  .header-clock { display: none; }
  .nav-tab { min-width: 82px !important; }
}

@media (max-width: 620px) {
  .header-inner { padding: 0 10px; gap: 8px; }
  .brand-mark { width: 36px; height: 36px; }
  .brand-mark img { width: 25px; height: 25px; }
  .nav-tab { min-width: 54px !important; padding: 0 10px !important; }
  .nav-tab .v-icon { margin-right: 0; }
  .tab-label { display: none; }
  .header-actions { gap: 4px; }
}
</style>
