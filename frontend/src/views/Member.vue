<template>
  <v-container fluid class="member-page">
    <div class="page-heading">
      <div>
        <div class="page-heading__eyebrow">Team governance</div>
        <h1 class="page-heading__title">成员管理</h1>
        <p class="page-heading__description">
          集中处理管理员申请与权限状态。当前操作使用示例数据，可安全体验审批流程。
        </p>
      </div>
      <v-chip color="warning" variant="tonal" prepend-icon="mdi-database-outline">示例数据模式</v-chip>
    </div>

    <v-row class="metric-grid" dense>
      <v-col cols="12" sm="4">
        <v-card class="surface-card metric-card" color="primary">
          <div class="metric-icon"><v-icon>mdi-account-clock-outline</v-icon></div>
          <div>
            <div class="metric-label">待审批申请</div>
            <div class="metric-value">{{ adminApplyList.length }}</div>
          </div>
        </v-card>
      </v-col>
      <v-col cols="12" sm="4">
        <v-card class="surface-card metric-card" color="secondary">
          <div class="metric-icon"><v-icon>mdi-shield-account-outline</v-icon></div>
          <div>
            <div class="metric-label">在职管理员</div>
            <div class="metric-value">{{ adminList.length }}</div>
          </div>
        </v-card>
      </v-col>
      <v-col cols="12" sm="4">
        <v-card class="surface-card metric-card metric-card--neutral">
          <div class="metric-icon"><v-icon>mdi-lock-check-outline</v-icon></div>
          <div>
            <div class="metric-label">当前权限组</div>
            <div class="metric-value metric-value--text">管理员</div>
          </div>
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12">
        <v-card class="surface-card member-table-card mb-4">
          <v-toolbar color="transparent" density="compact">
            <v-toolbar-title class="text-h6 font-weight-bold text-primary">
              <v-icon start color="primary">mdi-account-clock-outline</v-icon>
              管理员资格申请审批
            </v-toolbar-title>
            <v-chip class="mr-4" size="small" color="primary" variant="tonal">示例数据</v-chip>
          </v-toolbar>
          <v-divider></v-divider>

          <v-data-table
            :headers="headers"
            :items="adminApplyList"
            show-expand
            hover
            items-per-page-text="每页记录："
            no-data-text="暂时没有待审批的申请~"
          >
            <template v-slot:expanded-row="{ columns, item }">
              <tr class="bg-grey-lighten-5">
                <td :colspan="columns.length" class="pa-4">
                  <div class="d-flex align-center">
                    <v-icon color="info" class="me-2">mdi-information-outline</v-icon>
                    <strong>详细申请理由：</strong>
                    <span class="text-grey-darken-2 ms-2">{{ item.reason || '未填写' }}</span>
                  </div>
                </td>
              </tr>
            </template>

            <template v-slot:item.actions="{ item }">
              <v-tooltip text="同意申请" location="top">
                <template v-slot:activator="{ props }">
                  <v-btn
                    v-bind="props"
                    icon="mdi-check"
                    color="success"
                    variant="text"
                    size="small"
                    aria-label="同意申请"
                    @click="passItem(item)"
                  ></v-btn>
                </template>
              </v-tooltip>

              <v-tooltip text="拒绝申请" location="top">
                <template v-slot:activator="{ props }">
                  <v-btn
                    v-bind="props"
                    icon="mdi-close"
                    color="error"
                    variant="text"
                    size="small"
                    aria-label="拒绝申请"
                    @click="deleteItem(item)"
                  ></v-btn>
                </template>
              </v-tooltip>
            </template>
          </v-data-table>
        </v-card>
      </v-col>

      <v-col cols="12">
        <v-card class="surface-card member-table-card">
          <v-toolbar color="transparent" density="compact">
            <v-toolbar-title class="text-h6 font-weight-bold text-success">
              <v-icon start color="success">mdi-shield-account-outline</v-icon>
              在职管理员信息
            </v-toolbar-title>
          </v-toolbar>
          <v-divider></v-divider>

          <v-data-table
            :headers="headers2"
            :items="adminList"
            show-expand
            hover
            items-per-page-text="每页记录："
            no-data-text="暂无管理员数据~"
          >
            <template v-slot:expanded-row="{ columns, item }">
              <tr class="bg-grey-lighten-5">
                <td :colspan="columns.length" class="pa-4">
                  <div class="d-flex align-center">
                    <v-icon color="info" class="me-2">mdi-text-box-outline</v-icon>
                    <strong>历史申请理由：</strong>
                    <span class="text-grey-darken-2 ms-2">{{ item.reason || '无记录' }}</span>
                  </div>
                </td>
              </tr>
            </template>
            </v-data-table>
        </v-card>
      </v-col>
    </v-row>
  </v-container>

  <v-dialog v-model="dialogDelete" max-width="450px" persistent>
    <v-card rounded="lg">
      <v-card-title class="text-h6 pt-6 px-6 d-flex align-center">
        <v-icon color="error" class="me-2">mdi-alert-circle</v-icon>
        拒绝申请确认
      </v-card-title>
      <v-card-text class="px-6 py-4 text-body-1">
        确定要 <strong class="text-error">拒绝</strong>
        <span class="font-weight-bold text-primary px-1">{{ curdItem?.name }}</span>
        的管理员申请吗？此操作无法撤销。
      </v-card-text>
      <v-card-actions class="px-6 pb-6">
        <v-spacer></v-spacer>
        <v-btn variant="plain" :disabled="isSubmitting" @click="closeDelete">取消</v-btn>
        <v-btn color="error" variant="flat" :loading="isSubmitting" @click="deleteItemConfirm">
          确认拒绝
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <v-dialog v-model="dialogPass" max-width="450px" persistent>
    <v-card rounded="lg">
      <v-card-title class="text-h6 pt-6 px-6 d-flex align-center">
        <v-icon color="success" class="me-2">mdi-check-circle</v-icon>
        同意申请确认
      </v-card-title>
      <v-card-text class="px-6 py-4 text-body-1">
        确定要 <strong class="text-success">同意</strong>
        <span class="font-weight-bold text-primary px-1">{{ curdItem?.name }}</span>
        的管理员申请吗？他将获得系统管理权限。
      </v-card-text>
      <v-card-actions class="px-6 pb-6">
        <v-spacer></v-spacer>
        <v-btn variant="plain" :disabled="isSubmitting" @click="closePass">取消</v-btn>
        <v-btn color="success" variant="flat" :loading="isSubmitting" @click="passConfirm">
          确认授权
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <v-snackbar v-model="snackbar" :timeout="3000" :color="snackbarColor" location="top">
    <div class="d-flex align-center">
      <v-icon start>{{ snackbarColor === 'success' ? 'mdi-check-circle' : 'mdi-alert-circle' }}</v-icon>
      {{ snackbarText }}
    </div>
  </v-snackbar>
</template>

<script lang="ts" setup>
import { ref } from "vue";

interface AdminApplication {
  id: number;
  name: string;
  contact: string;
  applyDate: string;
  reason: string;
}

interface Administrator extends AdminApplication {
  username: string;
  passDate: string;
}

// --- 全局状态 ---
const snackbar = ref(false);
const snackbarText = ref("");
const snackbarColor = ref("success"); // 动态控制颜色
const isSubmitting = ref(false);      // 按钮 loading 状态，防重复提交

// --- 表格配置 ---
const headers = [
  { title: "ID", key: "id", width: "80px" },
  { title: "申请人", key: "name" },
  { title: "联系方式", key: "contact" },
  { title: "申请日期", key: "applyDate" },
  { title: "申请理由", key: "reason" },
  { title: "操作", key: "actions", sortable: false, align: "center" as const },
];

const headers2 = [
  { title: "ID", key: "id", width: "80px" },
  { title: "姓名", key: "name" },
  { title: "用户名", key: "username" },
  { title: "联系方式", key: "contact" },
  { title: "申请日期", key: "applyDate" },
  { title: "申请理由", key: "reason" },
  { title: "通过日期", key: "passDate" },
];

// --- 模拟数据 ---
const adminApplyList = ref<AdminApplication[]>([
  { id: 1, name: "张三", contact: "1234567890", applyDate: "2022-01-01", reason: "我是一个优秀的管理员" },
]);

const adminList = ref<Administrator[]>([
  { id: 1, name: "曹武康", username: "Kangkang", contact: "1234567890", applyDate: "2022-01-01", reason: "我是一个优秀的管理员", passDate: "2022-01-01" },
  { id: 2, name: "李四", username: "Lisi", contact: "1234567890", applyDate: "2022-01-01", reason: "我是一个优秀的管理员", passDate: "2022-01-01" },
]);

// --- 业务逻辑 ---
const dialogPass = ref(false);
const dialogDelete = ref(false);
const curdItem = ref<AdminApplication | null>(null);

// 触发通用提示
const showMessage = (text: string, type: "success" | "error" = "success") => {
  snackbarText.value = text;
  snackbarColor.value = type;
  snackbar.value = true;
};

// 开启弹窗
const passItem = (item: AdminApplication) => {
  curdItem.value = item;
  dialogPass.value = true;
};

const deleteItem = (item: AdminApplication) => {
  curdItem.value = item;
  dialogDelete.value = true;
};

// 关闭弹窗
const closePass = () => {
  dialogPass.value = false;
  if (!isSubmitting.value) curdItem.value = null;
};

const closeDelete = () => {
  dialogDelete.value = false;
  if (!isSubmitting.value) curdItem.value = null;
};

// 确认拒绝 (使用 async/await 优化代码可读性)
const deleteItemConfirm = async () => {
  const item = curdItem.value;
  if (!item) return;
  isSubmitting.value = true;
  try {
    await new Promise((resolve) => window.setTimeout(resolve, 300));
    adminApplyList.value = adminApplyList.value.filter((application) => application.id !== item.id);
    showMessage(`已拒绝 ${item.name} 的申请（示例数据）`);
    dialogDelete.value = false;
  } finally {
    isSubmitting.value = false;
    curdItem.value = null;
  }
};

// 确认通过
const passConfirm = async () => {
  const item = curdItem.value;
  if (!item) return;
  isSubmitting.value = true;
  try {
    await new Promise((resolve) => window.setTimeout(resolve, 300));
    adminApplyList.value = adminApplyList.value.filter((application) => application.id !== item.id);
    adminList.value.unshift({
      ...item,
      id: Math.max(0, ...adminList.value.map((admin) => admin.id)) + 1,
      username: `admin_${item.id}`,
      passDate: new Date().toISOString().slice(0, 10),
    });
    showMessage(`已授权 ${item.name} 为管理员（示例数据）`);
    dialogPass.value = false;
  } finally {
    isSubmitting.value = false;
    curdItem.value = null;
  }
};
</script>

<style scoped>
.member-page {
  min-height: calc(100vh - var(--app-header-height));
  padding: 28px !important;
  background:
    radial-gradient(circle at 88% 4%, rgba(49, 87, 246, 0.06), transparent 25%),
    transparent;
}

.metric-grid {
  margin-bottom: 10px;
}

.metric-card {
  display: flex;
  align-items: center;
  gap: 16px;
  min-height: 116px;
  padding: 22px;
  color: white;
  background: linear-gradient(135deg, #3157f6, #5272f7) !important;
}

.metric-grid .v-col:nth-child(2) .metric-card {
  background: linear-gradient(135deg, #078ea6, #08b9cd) !important;
}

.metric-card--neutral {
  color: #1c2b4a;
  background: linear-gradient(135deg, #ffffff, #f5f8ff) !important;
}

.metric-icon {
  display: grid;
  width: 48px;
  height: 48px;
  flex: 0 0 auto;
  place-items: center;
  border: 1px solid rgba(255, 255, 255, 0.24);
  border-radius: 15px;
  background: rgba(255, 255, 255, 0.16);
  font-size: 24px;
}

.metric-card--neutral .metric-icon {
  color: #3157f6;
  border-color: rgba(49, 87, 246, 0.12);
  background: rgba(49, 87, 246, 0.08);
}

.metric-label {
  margin-bottom: 2px;
  font-size: 13px;
  font-weight: 600;
  opacity: 0.82;
}

.metric-value {
  font-size: 30px;
  font-weight: 800;
  line-height: 1.1;
}

.metric-value--text {
  font-size: 22px;
}

.member-table-card {
  overflow: hidden;
  background: rgba(255, 255, 255, 0.95);
}

.member-table-card :deep(.v-toolbar) {
  min-height: 64px;
  padding: 6px 8px;
}

.member-table-card :deep(.v-toolbar-title) {
  color: #1c2b4a !important;
  font-size: 17px !important;
}

.member-table-card :deep(thead th) {
  color: #5e6d88;
  font-size: 12px;
  font-weight: 800 !important;
  letter-spacing: 0.03em;
  background: #f8faff;
}

.member-table-card :deep(tbody tr) {
  transition: background-color 160ms ease;
}

.member-table-card :deep(tbody tr:hover) {
  background: rgba(49, 87, 246, 0.035) !important;
}

@media (max-width: 960px) {
  .member-page {
    padding: 22px 18px !important;
  }
}

@media (max-width: 600px) {
  .member-page {
    padding: 18px 12px !important;
  }

  .metric-card {
    min-height: 98px;
    padding: 18px;
  }

  .member-table-card :deep(.v-toolbar-title) {
    font-size: 15px !important;
  }
}
</style>
