<script setup>
import BaseAuthView from "@/views/base/BaseAuthView.vue";
import {ref} from "vue";

const form = ref({
  username: "",
  email: "",
  password: "",
  password_confirm: ""
})

const passwordShown = ref(false);
const confirmPasswordShow = ref(false);

</script>

<template>
  <BaseAuthView>
    <v-form v-model="form">
      <v-text-field
          v-model="form.username"
          variant="outlined"
          density="compact"
          id="username"
          label="Имя пользователя"
          placeholder="Введите имя пользователя"/>
      <v-text-field
          v-model="form.email"
          variant="outlined"
          density="compact"
          id="email"
          type="email"
          label="Электронная почта"
          placeholder="Введите электронную почту"/>
      <v-text-field
          v-model="form.password"
          variant="outlined"
          density="compact"
          id="password"
          label="Пароль"
          placeholder="Введите пароль"
          :type="passwordShown ? 'text' : 'password'"
          :append-inner-icon="passwordShown ? 'mdi-eye' : 'mdi-eye-off'"
          @click:append-inner="passwordShown = !passwordShown"/>
      <v-text-field
          v-model="form.password_confirm"
          variant="outlined"
          density="compact" id="password_confirm"
          label="Подтверждение пароля"
          placeholder="Введите пароль повторно"
          :type="confirmPasswordShow ? 'text' : 'password'"
          :append-inner-icon="confirmPasswordShow ? 'mdi-eye' : 'mdi-eye-off'"
          @click:append-inner="confirmPasswordShow = !confirmPasswordShow"/>
      <div class="w-100 text-center">
        <v-btn variant="outlined">Зарегистрироваться</v-btn>
      </div>
    </v-form>
  </BaseAuthView>
</template>

<style scoped>
:deep(form) {
  min-width: 400px;
}

:deep(.v-label) {
  font-size: 18px;
}

button {
  width: 400px;
  min-height: 45px;
}

</style>