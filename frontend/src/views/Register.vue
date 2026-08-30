<script setup lang="ts">
import AuthShell from "@/components/AuthShell.vue";
import AuthRegister from "@/views/AuthRegister.vue";
</script>

<template>
  <AuthShell
    eyebrow="Create Account"
    title="创建账号"
    subtitle="当前示例模式不会保存新账号，正式账号请由系统管理员创建。"
  >
    <AuthRegister />
  </AuthShell>
</template>
