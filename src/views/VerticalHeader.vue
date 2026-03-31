<script setup lang="ts">
import { ref, onMounted, onBeforeMount } from "vue";
import ProfileDD from "./ProfileDD.vue";
import {
  BellIcon,
  SettingsIcon,
  SearchIcon,
  Menu2Icon,
} from "vue-tabler-icons";

const formattedDateTime = ref("");
let updateTimeInterval: NodeJS.Timeout;
function updateTime() {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, "0");
  const day = String(now.getDate()).padStart(2, "0");
  const hours = String(now.getHours()).padStart(2, "0");
  const minutes = String(now.getMinutes()).padStart(2, "0");
  const seconds = String(now.getSeconds()).padStart(2, "0");
  formattedDateTime.value = `${year}/${month}/${day} ${hours}:${minutes}:${seconds}`;
}

onMounted(() => {
  updateTimeInterval = setInterval(updateTime, 1000);
});
onBeforeMount(() => {
  clearInterval(updateTimeInterval);
});

const tab = ref("1");
</script>

<template>
  <v-app-bar elevation="0" height="64" color="indigo-darken-3">
    <v-tabs
      v-model="tab"
      bg-color="transparent"
      stacked
      selected-class="select"
      style="position: absolute"
    >
      <v-tab value="1" to="/Dashboard">
        <v-icon>mdi-monitor-dashboard</v-icon>
        大屏首页
      </v-tab>
      <v-tab value="2" to="/Monitor">
        <v-icon>mdi-cctv</v-icon>
        实时监控
      </v-tab>
      <v-tab value="3" to="/Analysis">
        <v-icon>mdi-google-analytics</v-icon>
        记录分析
      </v-tab>

      <!-- <v-tab value="3" to="/History">
        <v-icon>mdi-history</v-icon>
        历史记录
      </v-tab> -->
    </v-tabs>

    <v-app-bar-title class="text-center"
      >非机动车骑乘人员头盔佩戴检测Web大屏
    </v-app-bar-title>

    <div style="position: absolute; right: 5.5rem">
      {{ formattedDateTime }}
    </div>
    <!-- <v-spacer /> -->
    <!-- ---------------------------------------------- -->
    <!-- User Profile -->
    <!-- ---------------------------------------------- -->
    <v-menu :close-on-content-click="false">
      <template v-slot:activator="{ props }">
        <v-btn
          class="text-primary"
          color="lightprimary"
          variant="flat"
          rounded="pill"
          v-bind="props"
        >
          <SettingsIcon stroke-width="1.5" />
        </v-btn>
      </template>
      <v-sheet rounded="md" width="150" elevation="12">
        <ProfileDD />
      </v-sheet>
    </v-menu>
  </v-app-bar>
</template>

<style>
.select {
  background-color: #3949ab !important;
  color: #fff !important;
}
</style>
