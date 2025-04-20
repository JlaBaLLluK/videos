<script setup>
import BaseAuthView from '@/views/base/BaseAuthView.vue';
import {ref} from 'vue';
import {userRegistrationConfirmation} from '@/api/index.js';
import {useRouter} from 'vue-router';
import {successToast} from '@/plugins/toasts.js';

const router = useRouter();

const confirmationCode = ref('');
const error = ref();

async function submit() {
  const registeredUserData = JSON.parse(localStorage.getItem('registeredUserData'));
  if (registeredUserData.confirmation_code !== confirmationCode.value) {
    error.value = 'Неверный код подтверждения.';
    return;
  }

  error.value = '';
  const message = await userRegistrationConfirmation(registeredUserData.username);
  localStorage.removeItem('registeredUserData');
  successToast(message);
  await router.push({name: 'login'});
}

</script>

<template>
  <base-auth-view>
    <v-form @submit.prevent="submit">
      <v-text-field
        v-model="confirmationCode"
        label="Код подтверждения"
        placeholder="Введите код подтверждения"
        class="mt-5"
        :error-messages="error"
        variant="outlined"
        density="compact"
      />
      <v-btn
        variant="outlined"
        type="submit"
        text="Подтвердить"
        class="w-100 mt-2"
      />
    </v-form>
  </base-auth-view>
</template>

<style scoped>
:deep(form) {
  min-width: 300px;
}

:deep(.v-label) {
  font-size: 18px;
}

:deep(.v-messages__message) {
  font-size: 16px;
}

</style>
