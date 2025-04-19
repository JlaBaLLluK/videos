<script setup>
import BaseAuthView from '@/views/base/BaseAuthView.vue';
import {ref} from 'vue';
import {userRegistration} from '@/api/index.js';
import {useRouter} from 'vue-router';
import PasswordField from '@/components/PasswordField.vue';
import {infoToast} from '@/plugins/toasts.js';

const form = ref({
  username: '',
  email: '',
  password: '',
  password_confirm: ''
});
const formErrors = ref({});

const router = useRouter();

async function submit() {
  const response = await userRegistration(form.value);
  if (response.status === 400) {
    formErrors.value = response.data;
  } else {
    localStorage.setItem('registeredUserData', JSON.stringify(response.data));
    await router.push({name: 'registrationConfirm'});
    infoToast('Введите код, отправленный на указанный вами адрес электронный почты.');
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
      <password-field
        v-model="form.password"
        :errors="formErrors.password"
        placeholder="Введите пароль"
        label="Пароль"
      />
      <password-field
        v-model="form.password_confirm"
        :errors="formErrors.password_confirm"
        placeholder="Введите пароль повторно"
        label="Подтверждение пароля"
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
