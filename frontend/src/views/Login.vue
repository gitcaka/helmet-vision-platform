<script setup lang="ts">
import AuthShell from "@/components/AuthShell.vue";
import AuthLogin from "@/views/AuthLogin.vue";
</script>

<template>
  <AuthShell
    eyebrow="Secure Access"
    title="欢迎回来"
    subtitle="登录后查看实时检测、告警抓拍与交通趋势。"
  >
    <AuthLogin />
  </AuthShell>
</template>
