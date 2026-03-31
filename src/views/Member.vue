<template>
  <v-container fluid class="pa-6 bg-grey-lighten-4 min-vh-100">
    <v-row>
      <v-col cols="12">
        <v-card elevation="2" rounded="lg" class="mb-4">
          <v-toolbar color="transparent" density="compact">
            <v-toolbar-title class="text-h6 font-weight-bold text-primary">
              <v-icon start color="primary">mdi-account-clock-outline</v-icon>
              管理员资格申请审批
            </v-toolbar-title>
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
                    @click="deleteItem(item)"
                  ></v-btn>
                </template>
              </v-tooltip>
            </template>
          </v-data-table>
        </v-card>
      </v-col>

      <v-col cols="12">
        <v-card elevation="2" rounded="lg">
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
        <span class="font-weight-bold text-primary px-1">{{ curdItem.name }}</span>
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
        <span class="font-weight-bold text-primary px-1">{{ curdItem.name }}</span>
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
import axios from "axios";

// --- 全局状态 ---
const snackbar = ref(false);
const snackbarText = ref("");
const snackbarColor = ref("success"); // 动态控制颜色
const isSubmitting = ref(false);      // 按钮 loading 状态，防重复提交

// --- 表格配置 ---
const headers = ref([
  { title: "ID", key: "id", width: "80px" },
  { title: "申请人", key: "name" },
  { title: "联系方式", key: "contact" },
  { title: "申请日期", key: "applyDate" },
  { title: "申请理由", key: "reason" },
  { title: "操作", key: "actions", sortable: false, align: "center" },
]);

const headers2 = ref([
  { title: "ID", key: "id", width: "80px" },
  { title: "姓名", key: "name" },
  { title: "用户名", key: "username" },
  { title: "联系方式", key: "contact" },
  { title: "申请日期", key: "applyDate" },
  { title: "申请理由", key: "reason" },
  { title: "通过日期", key: "passDate" },
]);

// --- 模拟数据 ---
const adminApplyList = ref([
  { id: 1, name: "张三", contact: "1234567890", applyDate: "2022-01-01", reason: "我是一个优秀的管理员" },
]);

const adminList = ref([
  { id: 1, name: "曹武康", username: "Kangkang", contact: "1234567890", applyDate: "2022-01-01", reason: "我是一个优秀的管理员", passDate: "2022-01-01" },
  { id: 2, name: "李四", username: "Lisi", contact: "1234567890", applyDate: "2022-01-01", reason: "我是一个优秀的管理员", passDate: "2022-01-01" },
]);

// --- 业务逻辑 ---
const dialogPass = ref(false);
const dialogDelete = ref(false);
const curdItem = ref<any>({}); // 增加 TypeScript Any 类型或自行定义 Interface

// 触发通用提示
const showMessage = (text: string, type: "success" | "error" = "success") => {
  snackbarText.value = text;
  snackbarColor.value = type;
  snackbar.value = true;
};

// 开启弹窗
const passItem = (item: any) => {
  curdItem.value = item;
  dialogPass.value = true;
};

const deleteItem = (item: any) => {
  curdItem.value = item;
  dialogDelete.value = true;
};

// 关闭弹窗
const closePass = () => {
  dialogPass.value = false;
  if (!isSubmitting.value) curdItem.value = {};
};

const closeDelete = () => {
  dialogDelete.value = false;
  if (!isSubmitting.value) curdItem.value = {};
};

// 确认拒绝 (使用 async/await 优化代码可读性)
const deleteItemConfirm = async () => {
  isSubmitting.value = true;
  try {
    await axios.post("http://localhost:5000/deleteAdminApply", { id: curdItem.value.id });
    showMessage(`已成功拒绝 ${curdItem.value.name} 的申请`);
    dialogDelete.value = false;
    // 提示：此处可追加刷新列表的逻辑，例如 adminApplyList.value = adminApplyList.value.filter(...)
  } catch (err: any) {
    showMessage(`拒绝申请失败: ${err.message || err}`, "error"); // 动态变红
  } finally {
    isSubmitting.value = false;
    curdItem.value = {};
  }
};

// 确认通过
const passConfirm = async () => {
  isSubmitting.value = true;
  try {
    await axios.post("http://localhost:5000/passAdminApply", { id: curdItem.value.id });
    showMessage(`已成功授权 ${curdItem.value.name} 为管理员`);
    dialogPass.value = false;
    // 提示：此处可追加刷新列表的逻辑
  } catch (err: any) {
    showMessage(`授权失败: ${err.message || err}`, "error"); // 动态变红
  } finally {
    isSubmitting.value = false;
    curdItem.value = {};
  }
};
</script>

<style scoped>
/* 确保全屏灰色背景，凸显白色卡片 */
.min-vh-100 {
  min-height: 100vh;
}
</style>
