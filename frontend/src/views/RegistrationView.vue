<script setup>
import BaseAuthView from "@/views/base/BaseAuthView.vue";
import {ref} from "vue";
import {userRegistration} from "@/api/index.js";
import {useRouter} from "vue-router";

const form = ref({
  username: "",
  email: "",
  password: "",
  password_confirm: ""
});
const formErrors = ref({});
const passwordShown = ref(false);
const confirmPasswordShow = ref(false);

const router = useRouter()

async function submit() {
  const response = await userRegistration(form.value);
  if (response.status === 400) {
    formErrors.value = response.data;
  } else {
    await router.push({name: 'login'});
  }
}

</script>

<template>
  <BaseAuthView>
    <v-form class="mt-6" @submit.prevent="submit">
      <v-text-field
          v-model="form.username"
          variant="outlined"
          density="compact"
          label="Имя пользователя"
          placeholder="Введите имя пользователя"
          :error-messages="formErrors.username"/>
      <v-text-field
          class="mt-3"
          v-model="form.email"
          variant="outlined"
          density="compact"
          type="email"
          label="Электронная почта"
          placeholder="Введите электронную почту"
          :error-messages="formErrors.email"/>
      <v-text-field
          class="mt-3"
          v-model="form.password"
          variant="outlined"
          density="compact"
          label="Пароль"
          placeholder="Введите пароль"
          :type="passwordShown ? 'text' : 'password'"
          :append-inner-icon="passwordShown ? 'mdi-eye' : 'mdi-eye-off'"
          @click:append-inner="passwordShown = !passwordShown"
          :error-messages="formErrors.password"/>
      <v-text-field
          class="mt-3"
          v-model="form.password_confirm"
          variant="outlined"
          density="compact"
          label="Подтверждение пароля"
          placeholder="Введите пароль повторно"
          :type="confirmPasswordShow ? 'text' : 'password'"
          :append-inner-icon="confirmPasswordShow ? 'mdi-eye' : 'mdi-eye-off'"
          @click:append-inner="confirmPasswordShow = !confirmPasswordShow"
          :error-messages="formErrors.password_confirm"/>
      <div class="w-100 text-center mt-3">
        <v-btn variant="outlined" type="submit">Зарегистрироваться</v-btn>
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

:deep(.v-messages__message) {
  font-size: 16px;
}

button {
  width: 400px;
  min-height: 45px;
}

</style>
