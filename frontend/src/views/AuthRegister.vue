<script setup lang="ts">
import { ref } from "vue";
import { RouterLink } from "vue-router";
import { router } from "@/router";
import { appConfig } from "@/config";

const acceptedTerms = ref(false);
const username = ref("");
const password = ref("");
const showPassword = ref(false);
const submitting = ref(false);
const usernameRules = [(value: string) => !!value || "请输入用户名"];
const passwordRules = [(value: string) => !!value || "请输入密码", (value: string) => value.length <= 16 || "密码不能超过16个字符"];
const message = ref("");
const alertType = ref<"info" | "warning">("info");

async function validate() {
  if (!username.value || !password.value) {
    alertType.value = "warning";
    message.value = "请输入用户名和密码";
    return;
  }
  if (!acceptedTerms.value) {
    alertType.value = "warning";
    message.value = "请先阅读并同意使用条款";
    return;
  }
  if (!appConfig.useMockData) {
    alertType.value = "warning";
    message.value = "当前后端未开放自助注册，请联系管理员创建账号";
    return;
  }

  submitting.value = true;
  await new Promise((resolve) => window.setTimeout(resolve, 350));
  submitting.value = false;
  alertType.value = "info";
  message.value = "演示模式不会创建账号，即将返回登录页";
  window.setTimeout(() => void router.push("/login"), 1200);
}
</script>

<template>
  <v-alert class="mb-5" color="info" variant="tonal" density="compact" icon="mdi-information-outline">
    正式账号由系统管理员统一创建和授权。
  </v-alert>

  <v-form class="auth-form" @submit.prevent="validate">
    <v-text-field
      v-model="username"
      :rules="usernameRules"
      label="用户名"
      autocomplete="username"
      prepend-inner-icon="mdi-account-plus-outline"
      variant="outlined"
      density="comfortable"
      hide-details="auto"
      class="auth-input"
    />
    <v-text-field
      v-model="password"
      :rules="passwordRules"
      label="密码"
      autocomplete="new-password"
      prepend-inner-icon="mdi-lock-outline"
      :append-inner-icon="showPassword ? 'mdi-eye-off-outline' : 'mdi-eye-outline'"
      :type="showPassword ? 'text' : 'password'"
      variant="outlined"
      density="comfortable"
      hide-details="auto"
      class="auth-input"
      @click:append-inner="showPassword = !showPassword"
    />

    <v-checkbox v-model="acceptedTerms" color="primary" density="compact" hide-details>
      <template #label>
        <span class="terms-label">我已阅读并同意平台使用条款</span>
      </template>
    </v-checkbox>

    <v-alert v-if="message" :type="alertType" variant="tonal" density="compact">{{ message }}</v-alert>

    <v-btn
      color="primary"
      block
      height="50"
      variant="flat"
      size="large"
      type="submit"
      :loading="submitting"
      append-icon="mdi-arrow-right"
      class="register-button"
    >
      提交账号申请
    </v-btn>
  </v-form>

  <div class="auth-switch">
    <span>已有账号？</span>
    <RouterLink to="/login">返回登录</RouterLink>
  </div>
</template>

<style scoped lang="scss">
.auth-form { display: grid; gap: 17px; }
.auth-input :deep(.v-field) { border-radius: 14px; background: #fbfcfe; }
.auth-input :deep(.v-field__outline) { color: rgba(30, 55, 94, 0.18); }
.terms-label { color: #64748b; font-size: 13px; }
.register-button { box-shadow: 0 12px 26px rgba(49, 87, 246, 0.24); }
.auth-switch { display: flex; justify-content: center; gap: 6px; margin-top: 24px; color: #718096; font-size: 13px; }
.auth-switch a { color: #3157f6; font-weight: 700; text-decoration: none; }
</style>
