<script setup lang="ts">
import { RouterLink } from "vue-router";

withDefaults(defineProps<{ compact?: boolean }>(), { compact: false });
</script>

<template>
  <RouterLink class="logo-link" to="/" aria-label="Helmet Vision 首页">
    <span class="logo-frame" :class="{ 'logo-frame--compact': compact }">
      <img src="@/assets/logo.png" alt="Helmet Vision" />
    </span>
  </RouterLink>
</template>

<style scoped>
.logo-link { display: inline-flex; text-decoration: none; }
.logo-frame {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 64px;
  height: 64px;
  border-radius: 18px;
  background: linear-gradient(145deg, rgba(49, 87, 246, 0.12), rgba(8, 169, 196, 0.12));
}
.logo-frame--compact { width: 42px; height: 42px; border-radius: 12px; background: rgba(255, 255, 255, 0.08); }
.logo-frame img { width: 72%; height: 72%; object-fit: contain; }
</style>
