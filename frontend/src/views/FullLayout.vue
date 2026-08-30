<script lang="ts" setup>
import { RouterView } from "vue-router";
import VerticalHeaderVue from "./VerticalHeader.vue";
</script>

<template>
  <v-locale-provider>
    <v-app>
      <VerticalHeaderVue />
      <v-main>
        <v-container fluid class="page-wrapper">
          <RouterView />
        </v-container>
      </v-main>
    </v-app>
  </v-locale-provider>
</template>

<style>
.page-wrapper {
  min-height: calc(100vh - var(--app-header-height));
  background: transparent;
  padding: 0;
}
</style>
