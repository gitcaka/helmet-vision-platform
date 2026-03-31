<script setup lang="ts">
import Logo from "@/views/logo.vue";
import AuthLogin from "@/views/AuthLogin.vue";
</script>

<template>
  <div class="d-flex align-center justify-center h-screen sophisticated-bg px-4 py-8">

    <v-card
      elevation="16"
      class="login-card pa-10 pa-sm-12"
      rounded="xl"
    >
      <v-card-text class="pa-0">
        <div class="text-center mb-10">
          <Logo class="mb-6" />

          <h1 class="text-h5 text-sm-h4 font-weight-bold text-grey-darken-3 mb-3">
            非机动车骑乘人员<br class="d-sm-none" />头盔佩戴检测系统
          </h1>

          <p class="text-subtitle-1 text-grey-lighten-1 font-weight-regular">
            请登录后继续
          </p>
        </div>

        <AuthLogin />
      </v-card-text>
    </v-card>
  </div>
</template>

<style lang="scss">
/* 全局通用美化样式
*/

// 高级光影渐变背景
.sophisticated-bg {
  background: linear-gradient(135deg, #f0f3f8 0%, #fdfdff 100%);
}

// 登录卡片控制
.login-card {
  width: 100%;
  max-width: 500px;
  // 可以选择性地添加微妙的边框，在某些光线下会更有质感
  border: 1px solid rgba(0, 0, 0, 0.03);
}

/* 以下为您原有配合 AuthLogin.vue 组件内部使用的样式，已整理和优化
  建议：如果条件允许，请将它们移动到 AuthLogin.vue 的 <style scoped> 中。
*/
.loginForm {
  .v-field--outlined .v-field__outline {
    border-color: rgba(0, 0, 0, 0.08);
  }

  .v-field--active input {
    font-weight: 500;
  }
}

.custom-devider {
  border-color: rgba(0, 0, 0, 0.06) !important;
}

.orbtn {
  padding: 2px 30px;
  border-color: rgba(0, 0, 0, 0.08);
  margin: 20px 15px;
  color: #757575; // 优化“或”字的颜色
}

.pwdInput {
  position: relative;
  .v-input__append {
    position: absolute;
    right: 12px;
    top: 50%;
    transform: translateY(-50%);
  }
}

// 您原有的 googleBtn 和 outlinedInput 在此页面未直接用到，暂时保留以供组件内部使用
.googleBtn {
  border-color: rgba(0, 0, 0, 0.08);
  margin: 30px 0 20px 0;
}

.outlinedInput .v-field {
  border: 1px solid rgba(0, 0, 0, 0.08);
  box-shadow: none;
}
</style>
