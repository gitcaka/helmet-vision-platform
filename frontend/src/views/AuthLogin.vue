<script setup lang="ts">
import { ref } from "vue";
import { RouterLink } from "vue-router";
import { Form } from "vee-validate";
import { router } from "@/router";
import { appConfig } from "@/config";
import { useAuthStore } from "@/stores/auth";

const rememberMe = ref(true);
const showPassword = ref(false);
const username = ref("");
const password = ref("");
const passwordRules = [(value: string) => !!value || "请输入密码", (value: string) => value.length <= 16 || "密码不能超过16个字符"];
const usernameRules = [(value: string) => !!value || "请输入用户名"];

async function validate(
  _values: unknown,
  { setErrors }: { setErrors: (errors: { apiError: string }) => void },
) {
  if (!username.value || !password.value) {
    setErrors({ apiError: "请输入用户名和密码" });
    return;
  }

  const authStore = useAuthStore();
  try {
    await authStore.login(username.value, password.value);
    const destination = authStore.returnUrl || "/Dashboard";
    authStore.returnUrl = null;
    await router.push(destination);
  } catch (error) {
    setErrors({ apiError: error instanceof Error ? error.message : "登录失败" });
  }
}
</script>

<template>
  <v-alert
    v-if="appConfig.useMockData"
    class="demo-alert mb-5"
    color="primary"
    variant="tonal"
    density="compact"
    icon="mdi-flask-outline"
  >
    <div class="text-caption">演示账号</div>
    <strong>admin</strong><span class="mx-2 text-medium-emphasis">/</span><strong>123456</strong>
  </v-alert>

  <Form @submit="validate" class="auth-form" v-slot="{ errors, isSubmitting }">
    <v-text-field
      v-model="username"
      :rules="usernameRules"
      label="用户名"
      autocomplete="username"
      prepend-inner-icon="mdi-account-outline"
      variant="outlined"
      density="comfortable"
      hide-details="auto"
      class="auth-input"
    />
    <v-text-field
      v-model="password"
      :rules="passwordRules"
      label="密码"
      autocomplete="current-password"
      prepend-inner-icon="mdi-lock-outline"
      :append-inner-icon="showPassword ? 'mdi-eye-off-outline' : 'mdi-eye-outline'"
      :type="showPassword ? 'text' : 'password'"
      variant="outlined"
      density="comfortable"
      hide-details="auto"
      class="auth-input"
      @click:append-inner="showPassword = !showPassword"
    />

    <div class="form-options">
      <v-checkbox v-model="rememberMe" label="记住登录状态" color="primary" density="compact" hide-details />
      <span>安全会话有效期由服务端控制</span>
    </div>

    <v-alert v-if="errors.apiError" class="mb-4" type="error" variant="tonal" density="compact">
      {{ errors.apiError }}
    </v-alert>

    <v-btn
      color="primary"
      :loading="isSubmitting"
      block
      height="50"
      variant="flat"
      size="large"
      type="submit"
      append-icon="mdi-arrow-right"
      class="login-button"
    >
      登录系统
    </v-btn>
  </Form>

  <div class="auth-switch">
    <span>还没有账号？</span>
    <RouterLink to="/register">了解账号申请</RouterLink>
  </div>
</template>

<style scoped lang="scss">
.demo-alert { border: 1px solid rgba(49, 87, 246, 0.12); border-radius: 14px; }
.auth-form { display: grid; gap: 17px; }
.auth-input :deep(.v-field) { border-radius: 14px; background: #fbfcfe; }
.auth-input :deep(.v-field__outline) { color: rgba(30, 55, 94, 0.18); }
.form-options { display: flex; align-items: center; justify-content: space-between; gap: 12px; margin-top: -5px; }
.form-options span { color: #94a3b8; font-size: 11px; text-align: right; }
.login-button { box-shadow: 0 12px 26px rgba(49, 87, 246, 0.24); }
.auth-switch { display: flex; justify-content: center; gap: 6px; margin-top: 24px; color: #718096; font-size: 13px; }
.auth-switch a { color: #3157f6; font-weight: 700; text-decoration: none; }

@media (max-width: 480px) {
  .form-options { align-items: flex-start; flex-direction: column; }
  .form-options span { margin-left: 4px; text-align: left; }
}
</style>
