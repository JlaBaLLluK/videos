<script setup>
import BaseAuthView from "@/views/base/BaseAuthView.vue";
import {ref} from "vue";

const form = ref({
  username_or_email: "",
  password: "",
})

const passwordShown = ref(false);

</script>

<template>
  <BaseAuthView>
    <v-form enctype="multipart/form-data">
      <v-text-field
          v-model="form.username_or_email"
          variant="outlined"
          density="compact"
          id="username"
          label="Имя пользователя или эл. почта"
          placeholder="Введите имя пользователя или эл. почту"/>
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
      <div class="w-100 text-center">
        <v-btn variant="outlined">Войти</v-btn>
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