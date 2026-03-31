<!-- eslint-disable prettier/prettier -->
<script setup lang="ts">
import { ref } from 'vue';
import axios from 'axios';
import { router } from '@/router';

const checkbox = ref(false);
const username = ref('');
const password = ref('');
const show1 = ref(false);
const Regform = ref();
const passwordRules = ref([(v: string) => !!v || '请输入密码', (v: string) => (v && v.length <= 10) || '密码必须少于16个字符']);
const emailRules = ref([(v: string) => !!v || '请输入用户名']);
const showinfo = ref('')

function validate() {
  if(username.value === '' || password.value === ''){
    return showinfo.value = '请输入用户名或密码';
  };
  async function regist() {
    await axios.post('http://localhost:5000/regist', {'username':username.value, 'password':password.value}).then(res => {
      showinfo.value = res.data;
      setTimeout(() => {
        router.push('/auth/login')
      }, 1000);
    });
  }
  regist();
}
</script>

<template>
  <v-form ref="Regform" class="mt-7 loginForm">
    <v-text-field
      v-model="username"
      :rules="emailRules"
      label="用户名"
      class="mt-4 mb-4"
      required
      density="comfortable"
      hide-details="auto"
      variant="outlined"
      color="primary"
    ></v-text-field>
    <v-text-field
      v-model="password"
      :rules="passwordRules"
      label="密码"
      required
      density="comfortable"
      variant="outlined"
      color="primary"
      hide-details="auto"
      :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
      :type="show1 ? 'text' : 'password'"
      @click:append="show1 = !show1"
      class="pwdInput"
    ></v-text-field>

    <div class="d-sm-inline-flex align-center mt-2 mb-7 mb-sm-0 font-weight-bold">
      <v-checkbox
        v-model="checkbox"
        :rules="[(v: any) => !!v || '你必须同意继续！']"
        label="同意"
        required
        color="primary"
        class="ms-n2"
        hide-details
      ></v-checkbox>
      <a href="#" class="ml-1 text-lightText">我们的条款</a>
    </div>
    <v-btn color="secondary" block class="mt-2" variant="flat" size="large" @click="validate">注册</v-btn>
    <div v-if="showinfo" class="mt-2">
      <v-alert color="error">{{ showinfo }}</v-alert>
    </div>
  </v-form>
  <div class="mt-5 text-right">
    <v-divider />
    <v-btn variant="plain" to="/login" class="mt-2 text-capitalize mr-n2">已经有账号了?</v-btn>
  </div>
</template>
<style lang="scss">
.custom-devider {
  border-color: rgba(0, 0, 0, 0.08) !important;
}
.googleBtn {
  border-color: rgba(0, 0, 0, 0.08);
  margin: 30px 0 20px 0;
}
.outlinedInput .v-field {
  border: 1px solid rgba(0, 0, 0, 0.08);
  box-shadow: none;
}
.orbtn {
  padding: 2px 40px;
  border-color: rgba(0, 0, 0, 0.08);
  margin: 20px 15px;
}
.pwdInput {
  position: relative;
  .v-input__append {
    position: absolute;
    right: 10px;
    top: 50%;
    transform: translateY(-50%);
  }
}
</style>
