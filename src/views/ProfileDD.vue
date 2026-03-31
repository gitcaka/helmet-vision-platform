<script setup lang="ts">
import { ref } from "vue";
import { SettingsIcon, LogoutIcon, UserIcon } from "vue-tabler-icons";
import { useAuthStore } from "@/stores/auth";
import axios from "axios";

const authStore = useAuthStore();
const dialog = ref(false);
const step = ref(1);

const snackbar = ref(false);
const snackbarText = ref("");

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
}

function nextButton() {
  if (step.value == 2) {
    if (
      applyInput.value.name == "" ||
      applyInput.value.contact == "" ||
      applyInput.value.reason == ""
    ) {
      snackbarText.value = "请填写完整信息";
      snackbar.value = true;
      return;
    }
  }
  if (step.value < 3) {
    step.value += 1;
  } else {
    axios
      .post("http://localhost:5000/addExamine", {
        dog2adopt: dog2adopt.value,
        adopter: adopterInput.value,
      })
      .then((res) => {
        snackbarText.value = "申请成功";
        snackbar.value = true;
        dialog.value = false;
        clearAdoptInfo();
      })
      .catch((err) => {
        snackbarText.value = "提交失败" + err;
        snackbar.value = true;
      });
  }
}
</script>

<template>
  <!-- ---------------------------------------------- -->
  <!-- profile DD -->
  <!-- ---------------------------------------------- -->
  <div class="pa-4">
    <h4 class="mb-n1">早上好, <span class="font-weight-regular">康康</span></h4>
    <span class="text-subtitle-2 text-medium-emphasis">游客</span>

    <v-divider></v-divider>
    <perfect-scrollbar>
      <v-divider></v-divider>

      <v-list class="mt-3 pa-0">
        <v-list-item color="secondary" rounded="md">
          <template v-slot:prepend>
            <SettingsIcon size="20" class="mr-2" />
          </template>

          <v-list-item-title class="text-subtitle-2"
            >账户设置</v-list-item-title
          >
        </v-list-item>

        <v-list-item @click="dialog = true" color="secondary" rounded="md">
          <template v-slot:prepend>
            <UserIcon size="20" class="mr-2" />
          </template>

          <v-list-item-title class="text-subtitle-2"
            >成为管理</v-list-item-title
          >
        </v-list-item>

        <v-list-item color="secondary" rounded="md" to="/Member">
          <template v-slot:prepend>
            <UserIcon size="20" class="mr-2" />
          </template>

          <v-list-item-title class="text-subtitle-2"
            >成员管理</v-list-item-title
          >
        </v-list-item>

        <v-list-item @click="authStore.logout()" color="secondary" rounded="md">
          <template v-slot:prepend>
            <LogoutIcon size="20" class="mr-2" />
          </template>

          <v-list-item-title class="text-subtitle-2"
            >退出登录</v-list-item-title
          >
        </v-list-item>
      </v-list>
    </perfect-scrollbar>
  </div>

  <v-dialog
    v-model="dialog"
    max-width="800"
    persistent
    transition="dialog-bottom-transition"
  >
    <v-card>
      <v-card-title class="d-flex justify-space-between align-center">
        <div>
          <v-icon icon="mdi-account-cog-outline" class="mr-2"></v-icon
          >申请成为管理员
        </div>
        <v-btn icon="mdi-close" variant="text" @click="dialog = false"></v-btn>
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
        <v-btn class="ma-2" variant="tonal" @click="nextButton">
          {{ step == 1 ? "我同意" : step == 3 ? "提交审核" : "下一步" }}
        </v-btn>
      </template>
    </v-card>
  </v-dialog>

  <v-snackbar v-model="snackbar" :timeout="2000" color="success">{{
    snackbarText
  }}</v-snackbar>
</template>

<style lang="scss">
.v-field--variant-outlined {
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
</style>
