<script setup lang="ts">
import { computed, ref } from "vue";
import { useAuthStore } from "@/stores/auth";
import { router } from "@/router";
import { appConfig } from "@/config";

const authStore = useAuthStore();
const emit = defineEmits<{ "close-menu": [] }>();
const dialog = ref(false);
const accountDialog = ref(false);
const step = ref(1);

const snackbar = ref(false);
const snackbarText = ref("");
const snackbarColor = ref<"success" | "warning">("success");
const displayName = computed(() => authStore.user?.username || "用户");
const userInitial = computed(() => displayName.value.slice(0, 1).toUpperCase());
const isAdmin = computed(() => authStore.user?.role === "admin");
const roleLabel = computed(() => isAdmin.value ? "系统管理员" : "普通用户");
const accountStatus = computed(() => authStore.user ? "在线" : "未登录");
const dataMode = computed(() => appConfig.useMockData ? "示例数据" : "实时服务");
const accountDetails = computed(() => [
  { icon: "mdi-identifier", label: "账户 ID", value: `UID-${String(authStore.user?.id ?? 0).padStart(4, "0")}` },
  { icon: "mdi-account-badge-outline", label: "账户名称", value: displayName.value },
  { icon: "mdi-shield-key-outline", label: "权限角色", value: roleLabel.value },
  { icon: "mdi-database-sync-outline", label: "数据来源", value: dataMode.value },
]);
const greeting = computed(() => {
  const hour = new Date().getHours();
  if (hour < 6) return "夜深了";
  if (hour < 12) return "早上好";
  if (hour < 18) return "下午好";
  return "晚上好";
});

const applyInput = ref({
  name: "",
  contact: "",
  reason: "",
});

function prevButton() {
  step.value -= 1;
}

function clearAdoptInfo() {
  step.value = 1;
  applyInput.value = { name: "", contact: "", reason: "" };
}

function openAccountOverview() {
  accountDialog.value = true;
}

function openAdminApplication() {
  step.value = 1;
  dialog.value = true;
}

function closeAdminApplication() {
  dialog.value = false;
  emit("close-menu");
}

function closeAccountOverview() {
  accountDialog.value = false;
  emit("close-menu");
}

function startAdminApplicationFromOverview() {
  accountDialog.value = false;
  openAdminApplication();
}

async function goToMemberManagement() {
  accountDialog.value = false;
  emit("close-menu");
  await router.push("/Member");
}

async function nextButton() {
  if (step.value == 2) {
    if (
      applyInput.value.name == "" ||
      applyInput.value.contact == "" ||
      applyInput.value.reason == ""
    ) {
      snackbarText.value = "请填写完整信息";
      snackbarColor.value = "warning";
      snackbar.value = true;
      return;
    }
  }
  if (step.value < 3) {
    step.value += 1;
  } else {
    await new Promise((resolve) => window.setTimeout(resolve, 350));
    snackbarText.value = "申请已提交（示例数据）";
    snackbarColor.value = "success";
    snackbar.value = true;
    dialog.value = false;
    emit("close-menu");
    clearAdoptInfo();
  }
}

async function logout() {
  emit("close-menu");
  await authStore.logout();
  await router.push("/login");
}
</script>

<template>
  <!-- ---------------------------------------------- -->
  <!-- profile DD -->
  <!-- ---------------------------------------------- -->
  <div class="profile-panel">
    <div class="profile-summary">
      <v-avatar size="46" color="primary" class="profile-avatar">{{ userInitial }}</v-avatar>
      <div>
        <div class="profile-greeting">{{ greeting }}</div>
        <div class="profile-name">{{ displayName }}</div>
        <v-chip size="x-small" color="primary" variant="tonal" class="mt-1">
          {{ authStore.user?.role === 'admin' ? '系统管理员' : '普通用户' }}
        </v-chip>
      </div>
    </div>

    <v-divider class="my-3" />
    <div class="profile-menu-scroll">
      <v-list class="pa-0" density="comfortable">
        <v-list-item color="primary" rounded="lg" @click.stop="openAccountOverview">
          <template v-slot:prepend>
            <v-icon icon="mdi-account-circle-outline" size="20" class="mr-3" />
          </template>
          <v-list-item-title class="text-subtitle-2">账户概览</v-list-item-title>
          <v-list-item-subtitle>当前登录身份</v-list-item-subtitle>
        </v-list-item>

        <v-list-item @click.stop="openAdminApplication" color="primary" rounded="lg">
          <template v-slot:prepend>
            <v-icon icon="mdi-shield-account-outline" size="20" class="mr-3" />
          </template>
          <v-list-item-title class="text-subtitle-2">申请管理员</v-list-item-title>
          <v-list-item-subtitle>提交权限申请</v-list-item-subtitle>
        </v-list-item>

        <v-list-item color="primary" rounded="lg" @click="goToMemberManagement">
          <template v-slot:prepend>
            <v-icon icon="mdi-account-group-outline" size="20" class="mr-3" />
          </template>
          <v-list-item-title class="text-subtitle-2">成员管理</v-list-item-title>
          <v-list-item-subtitle>审批与人员列表</v-list-item-subtitle>
        </v-list-item>

        <v-list-item @click="logout" color="error" rounded="lg" aria-label="退出登录">
          <template v-slot:prepend>
            <v-icon icon="mdi-logout-variant" size="20" class="mr-3" />
          </template>
          <v-list-item-title class="text-subtitle-2">退出登录</v-list-item-title>
        </v-list-item>
      </v-list>
    </div>
  </div>

  <v-dialog v-model="accountDialog" max-width="620" persistent transition="dialog-bottom-transition">
    <v-card class="account-overview" rounded="xl">
      <div class="account-hero">
        <div class="account-hero__glow" />
        <div class="account-hero__content">
          <v-avatar size="68" color="rgba(255,255,255,.16)" class="account-hero__avatar">
            {{ userInitial }}
          </v-avatar>
          <div>
            <div class="account-hero__eyebrow">Account overview</div>
            <div class="account-hero__name">{{ displayName }}</div>
            <div class="account-hero__meta">
              <span><i class="status-dot" />{{ accountStatus }}</span>
              <span>{{ roleLabel }}</span>
            </div>
          </div>
          <v-btn
            class="account-close"
            icon="mdi-close"
            variant="text"
            aria-label="关闭账户概览"
            @click="closeAccountOverview"
          />
        </div>
      </div>

      <v-card-text class="account-body">
        <div class="account-section-title">基本信息</div>
        <div class="account-detail-grid">
          <div v-for="item in accountDetails" :key="item.label" class="account-detail-item">
            <span class="account-detail-icon"><v-icon :icon="item.icon" size="20" /></span>
            <span>
              <small>{{ item.label }}</small>
              <strong>{{ item.value }}</strong>
            </span>
          </div>
        </div>

        <div class="account-permission-card">
          <div>
            <div class="account-section-title mb-1">当前权限</div>
            <div class="text-body-2 text-medium-emphasis">
              {{ isAdmin ? '可访问检测大屏、实时监控、记录分析和成员管理。' : '可访问检测大屏、实时监控和记录分析。' }}
            </div>
          </div>
          <v-chip color="success" variant="tonal" prepend-icon="mdi-shield-check-outline">权限正常</v-chip>
        </div>
      </v-card-text>

      <v-card-actions class="account-actions">
        <v-btn
          v-if="isAdmin"
          variant="tonal"
          prepend-icon="mdi-account-group-outline"
          @click="goToMemberManagement"
        >
          成员管理
        </v-btn>
        <v-btn
          v-else
          variant="tonal"
          prepend-icon="mdi-shield-account-outline"
          @click="startAdminApplicationFromOverview"
        >
          申请管理员
        </v-btn>
        <v-spacer />
        <v-btn color="primary" variant="flat" @click="closeAccountOverview">完成</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <v-dialog
    v-model="dialog"
    max-width="800"
    persistent
    transition="dialog-bottom-transition"
  >
    <v-card class="admin-application" rounded="xl">
      <v-card-title class="admin-dialog-title d-flex justify-space-between align-center">
        <div>
          <v-icon icon="mdi-account-cog-outline" class="mr-2"></v-icon
          >申请成为管理员
        </div>
        <v-btn icon="mdi-close" variant="text" aria-label="关闭申请弹窗" @click="closeAdminApplication"></v-btn>
      </v-card-title>
      <v-stepper
        v-model="step"
        :items="['同意协议', '填写信息', '提交审核']"
        hide-actions
        flat
      >
        <template v-slot:item.1>
          <v-card title="管理员协议" flat>
            <v-card-text>
              &nbsp;&nbsp;&nbsp;&nbsp;1.
              本协议旨在明确用户申请成为非机动车骑行人员头盔佩戴检测Web应用管理员的条款和条件。<br />
              &nbsp;&nbsp;&nbsp;&nbsp;2.
              提交的申请将由现有管理员团队进行审核，审核过程包括背景调查和面试。审核结果将在提交申请后的14个工作日内通知申请人<br />
              &nbsp;&nbsp;&nbsp;&nbsp;3.
              管理员必须对在系统中获取的所有敏感信息保密，不得泄露给第三方。<br />
              &nbsp;&nbsp;&nbsp;&nbsp;4.
              系统管理员团队保留随时修改本协议的权利。用户若违反协议，管理员权限将被立即终止。<br />
              &nbsp;&nbsp;&nbsp;&nbsp;5.
              通过提交申请，用户表明已阅读、理解并同意遵守本协议的所有条款。<br />
            </v-card-text>
          </v-card>
        </template>
        <template v-slot:item.2>
          <v-card title="填写信息" flat>
            <v-row dense justify="center">
              <v-col cols="12" md="6" sm="6">
                <v-text-field
                  label="姓名"
                  prepend-icon="mdi-account"
                  :rounded="false"
                  variant="outlined"
                  v-model="applyInput.name"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6" sm="6">
                <v-text-field
                  label="联系方式"
                  prepend-icon="mdi-phone"
                  :rounded="false"
                  variant="outlined"
                  v-model="applyInput.contact"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="12" sm="6">
                <v-textarea
                  label="申请理由"
                  prepend-icon="mdi-lead-pencil"
                  variant="outlined"
                  counter
                  v-model="applyInput.reason"
                ></v-textarea>
              </v-col>
            </v-row>
          </v-card>
        </template>
        <template v-slot:item.3>
          <v-card title="提交审核？" flat>
            <v-card-text>
              请检查所有信息<span style="font-weight: bold; color: red"
                >无误</span
              >后再提交审核。
            </v-card-text>
            <v-row class="border-primary">
              <v-col cols="12" sm="12" class="py-0 my-0"
                >申请人：{{ applyInput.name }}</v-col
              >
              <v-col cols="12" sm="12" class="py-0 my-0"
                >联系方式：{{ applyInput.contact }}</v-col
              >
              <v-col cols="12" sm="12" class="py-0 my-0 mb-3"
                >申请理由：{{ applyInput.reason }}</v-col
              >
            </v-row>
          </v-card>
        </template>
      </v-stepper>
      <template v-slot:actions>
        <v-btn
          class="ma-2"
          variant="tonal"
          @click="prevButton"
          :disabled="step == 1 ? true : false"
        >
          上一步
        </v-btn>
        <v-spacer></v-spacer>
        <v-btn class="ma-2" color="primary" variant="flat" @click="nextButton">
          {{ step == 1 ? "我同意" : step == 3 ? "提交审核" : "下一步" }}
        </v-btn>
      </template>
    </v-card>
  </v-dialog>

  <v-snackbar v-model="snackbar" :timeout="2000" :color="snackbarColor">{{
    snackbarText
  }}</v-snackbar>
</template>

<style scoped lang="scss">
.profile-panel { padding: 18px; }
.profile-summary { display: flex; align-items: center; gap: 13px; }
.profile-avatar { color: #fff; font-weight: 800; box-shadow: 0 10px 22px rgba(49, 87, 246, 0.22); }
.profile-greeting { color: #94a3b8; font-size: 11px; }
.profile-name { margin-top: 1px; color: #12213f; font-size: 15px; font-weight: 800; }
.profile-menu-scroll :deep(.v-list-item) { margin-bottom: 3px; }
.profile-menu-scroll :deep(.v-list-item-subtitle) { margin-top: 2px; font-size: 10px; }
.profile-menu-scroll :deep(.v-list-item) { cursor: pointer; }

.account-overview,
.admin-application {
  overflow: hidden;
  border: 1px solid rgba(30, 55, 94, 0.1);
  box-shadow: 0 28px 80px rgba(14, 31, 65, 0.25) !important;
}

.account-hero {
  position: relative;
  overflow: hidden;
  padding: 28px;
  color: #fff;
  background: linear-gradient(125deg, #0c1b3e 0%, #183b7c 62%, #087f9b 130%);
}

.account-hero__glow {
  position: absolute;
  top: -90px;
  right: -55px;
  width: 230px;
  height: 230px;
  border-radius: 50%;
  background: rgba(55, 217, 242, 0.16);
  filter: blur(2px);
}

.account-hero__content {
  position: relative;
  display: flex;
  align-items: center;
  gap: 18px;
}

.account-hero__avatar {
  flex: 0 0 auto;
  border: 1px solid rgba(255, 255, 255, 0.22);
  font-size: 26px;
  font-weight: 800;
  box-shadow: 0 12px 28px rgba(5, 18, 45, 0.25);
}

.account-hero__eyebrow {
  color: rgba(218, 240, 255, 0.65);
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.14em;
  text-transform: uppercase;
}

.account-hero__name {
  margin-top: 3px;
  font-size: 24px;
  font-weight: 800;
  line-height: 1.2;
}

.account-hero__meta {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 8px;
  color: rgba(231, 244, 255, 0.78);
  font-size: 12px;
}

.account-hero__meta span {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.status-dot {
  display: inline-block;
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #4ade80;
  box-shadow: 0 0 0 4px rgba(74, 222, 128, 0.13);
}

.account-close {
  position: absolute;
  top: -12px;
  right: -12px;
  color: rgba(255, 255, 255, 0.82);
}

.account-body {
  padding: 24px 26px 12px !important;
}

.account-section-title {
  color: #263754;
  font-size: 13px;
  font-weight: 800;
}

.account-detail-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
  margin-top: 11px;
}

.account-detail-item {
  display: flex;
  align-items: center;
  gap: 11px;
  min-width: 0;
  padding: 13px;
  border: 1px solid #e6ecf5;
  border-radius: 14px;
  background: #f8faff;
}

.account-detail-icon {
  display: grid;
  width: 38px;
  height: 38px;
  flex: 0 0 auto;
  place-items: center;
  color: #3157f6;
  border-radius: 11px;
  background: rgba(49, 87, 246, 0.08);
}

.account-detail-item span:last-child {
  display: flex;
  min-width: 0;
  flex-direction: column;
}

.account-detail-item small {
  color: #8a96aa;
  font-size: 10px;
}

.account-detail-item strong {
  overflow: hidden;
  margin-top: 2px;
  color: #24324b;
  font-size: 13px;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.account-permission-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-top: 14px;
  padding: 16px;
  border: 1px solid rgba(16, 185, 129, 0.14);
  border-radius: 15px;
  background: rgba(16, 185, 129, 0.045);
}

.account-actions {
  padding: 12px 26px 24px;
}

.admin-dialog-title {
  padding: 20px 22px;
  color: #1f2e4b;
  border-bottom: 1px solid #e8edf5;
  background: linear-gradient(135deg, #f7f9ff, #f4fbfd);
  font-size: 18px;
  font-weight: 800;
}

:deep(.v-field--variant-outlined) {
  background-color: rgba(0, 0, 0, 0.025);
  border-radius: 12px !important;
}

.bg-lightwarning {
  background-color: #fff8e1;
}

.circle {
  position: relative;
  overflow: hidden;
  &.sm-circle {
    &::before {
      content: "";
      position: absolute;
      width: 200px;
      height: 200px;
      border: 3px solid rgb(var(--v-theme-warning));
      border-radius: 50%;
      top: 125px;
      right: -70px;
    }
  }

  &.lg-circle {
    &::after {
      content: "";
      position: absolute;
      width: 200px;
      height: 200px;
      border: 19px solid rgb(var(--v-theme-warning));
      border-radius: 50%;
      top: 65px;
      right: -150px;
    }
  }
}

.bg-lightprimary {
  background-color: #eef2f6;
}

.profile-menu-scroll {
  max-height: 420px;
  overflow-y: auto;
}

@media (max-width: 600px) {
  .account-hero {
    padding: 22px 18px;
  }

  .account-hero__avatar {
    width: 56px !important;
    height: 56px !important;
  }

  .account-hero__name {
    font-size: 20px;
  }

  .account-body {
    padding: 20px 16px 10px !important;
  }

  .account-detail-grid {
    grid-template-columns: 1fr;
  }

  .account-permission-card {
    align-items: flex-start;
    flex-direction: column;
  }

  .account-actions {
    padding: 10px 16px 18px;
  }
}
</style>
