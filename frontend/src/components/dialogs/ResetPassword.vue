<script setup>
import {ref} from 'vue';
import {resetPassword, sendResetPasswordCode} from '@/api/index.js';
import {infoToast} from '@/plugins/toasts.js';

const model = defineModel();

const username = ref('');
const confirmationCode = ref('');
const usernameErrors = ref({});
const codeError = ref('');
const displayCodeField = ref(false);
const submitButtonText = ref('Отправить код на почту');
const correctCode = ref('');

async function submit() {
  if (!displayCodeField.value) {
    const response = await sendResetPasswordCode(username.value);
    if (response.status !== 200) {
      usernameErrors.value = response.data;
      return;
    }

    displayCodeField.value = true;
    submitButtonText.value = 'Сбросить пароль';
    correctCode.value = response.data.code;
    return;
  }

  if (confirmationCode.value !== correctCode.value) {
    codeError.value = 'Неверный код.';
    return;
  }

  await resetPassword(username.value);
  infoToast('Новый пароль отправлен на почту. Вы сможете изменить его в своём профиле.');
  model.value = false;
}

</script>

<template>
  <v-dialog v-model="model" width="500" persistent>
    <v-card>
      <v-card-title class="pl-5 d-flex justify-space-between h-100 align-center">
        <h4>Сброс пароля</h4>
        <v-btn
          icon
          style="border: none; box-shadow: none"
          class="pa-0 ma-0"
          @click="model = false"
        >
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>
      <v-card-text>
        <v-form @submit.prevent="submit">
          <v-text-field
            id="username"
            v-model="username"
            variant="outlined"
            density="compact"
            label="Имя пользователя"
            placeholder="Введите имя пользователя"
            :error-messages="usernameErrors.username"
          />
          <v-text-field
            v-if="displayCodeField"
            v-model="confirmationCode"
            class="mt-3"
            variant="outlined"
            label="Код подтверждения"
            placeholder="Введите код подтверждения"
            :error-messages="codeError"
            density="compact"
          />
          <v-btn
            type="submit"
            variant="outlined"
            :text="submitButtonText"
            class="w-100 mt-2"
          />
        </v-form>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>
