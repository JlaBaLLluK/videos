<script setup>
import BaseAuthView from '@/views/base/BaseAuthView.vue';
import {ref} from 'vue';
import {userRegistration} from '@/api/index.js';
import {useRouter} from 'vue-router';

const form = ref({
  username: '',
  email: '',
  password: '',
  password_confirm: ''
});
const formErrors = ref({});
const passwordShown = ref(false);
const confirmPasswordShow = ref(false);

const router = useRouter();

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
  <base-auth-view>
    <v-form class="mt-6" @submit.prevent="submit">
      <v-text-field
        v-model="form.username"
        variant="outlined"
        density="compact"
        label="Имя пользователя"
        placeholder="Введите имя пользователя"
        :error-messages="formErrors.username"
      />
      <v-text-field
        v-model="form.email"
        class="mt-3"
        variant="outlined"
        density="compact"
        type="email"
        label="Электронная почта"
        placeholder="Введите электронную почту"
        :error-messages="formErrors.email"
      />
      <v-text-field
        v-model="form.password"
        class="mt-3"
        variant="outlined"
        density="compact"
        label="Пароль"
        placeholder="Введите пароль"
        :type="passwordShown ? 'text' : 'password'"
        :append-inner-icon="passwordShown ? 'mdi-eye' : 'mdi-eye-off'"
        :error-messages="formErrors.password"
        @click:append-inner="passwordShown = !passwordShown"
      />
      <v-text-field
        v-model="form.password_confirm"
        class="mt-3"
        variant="outlined"
        density="compact"
        label="Подтверждение пароля"
        placeholder="Введите пароль повторно"
        :type="confirmPasswordShow ? 'text' : 'password'"
        :append-inner-icon="confirmPasswordShow ? 'mdi-eye' : 'mdi-eye-off'"
        :error-messages="formErrors.password_confirm"
        @click:append-inner="confirmPasswordShow = !confirmPasswordShow"
      />
      <div class="w-100 text-center mt-3">
        <v-btn variant="outlined" type="submit">Зарегистрироваться</v-btn>
      </div>
    </v-form>
  </base-auth-view>
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
