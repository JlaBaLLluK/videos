<script setup>
import BaseAuthView from "@/views/base/BaseAuthView.vue";
import {ref} from "vue";
import {useRouter} from "vue-router";
import {userLogin} from "@/api/index.js";

const form = ref({
  username_or_email: "",
  password: "",
});
const formErrors = ref({});
const passwordShown = ref(false);

const router = useRouter()

async function submit() {
  const response = await userLogin(form.value);
  if (response.status === 400) {
    formErrors.value = response.data;
  } else if (response.status === 401) {
    formErrors.value.wrongCredentials = "Учётная запись не найдена.";
  } else {
    await router.push({name: 'home'});
  }
}

</script>

<template>
  <BaseAuthView>
    <v-form :class="{'mt-2': formErrors.wrongCredentials, 'mt-6': !formErrors.wrongCredentials}" @submit.prevent="submit">
      <label class="wrong-cred w-100 text-center mb-5"
             v-if="formErrors.wrongCredentials">{{ formErrors.wrongCredentials }}</label>
      <v-text-field
          v-model="form.username_or_email"
          variant="outlined"
          density="compact"
          id="username"
          label="Имя пользователя или эл. почта"
          placeholder="Введите имя пользователя или эл. почту"
          :error-messages="formErrors.username_or_email"/>
      <v-text-field
          class="mt-3"
          v-model="form.password"
          variant="outlined"
          density="compact"
          id="password"
          label="Пароль"
          placeholder="Введите пароль"
          :type="passwordShown ? 'text' : 'password'"
          :append-inner-icon="passwordShown ? 'mdi-eye' : 'mdi-eye-off'"
          @click:append-inner="passwordShown = !passwordShown"
          :error-messages="formErrors.password"/>
      <div class="w-100 text-center">
        <v-btn variant="outlined" type="submit" class="mt-3">Войти</v-btn>
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

:deep(.v-messages__message) {
  font-size: 16px;
}

.wrong-cred {
  font-size: 20px;
  color: #b00020;
}

</style>