<script setup>
import {ref} from 'vue';
import PasswordField from '@/components/PasswordField.vue';
import {updateUserPassword} from '@/api/index.js';

const model = defineModel();

const form = ref({
  current_password: null,
  new_password: null,
  new_password_confirm: null,
});
const formErrors = ref({});

async function submit() {
  const response = await updateUserPassword(form.value);
  if (response.status !== 200) {
    formErrors.value = response.data;
  } else {
    model.value = false;
  }
}

</script>

<template>
  <v-dialog v-model="model" persistent width="500">
    <v-card>
      <v-card-title class="pl-5 d-flex justify-space-between h-100 align-center">
        <h4>Обновление пароля</h4>
        <v-btn
          icon
          style="border: none; box-shadow: none"
          class="pa-0 ma-0"
          @click="model = false"
        >
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>
      <v-card-text class="pt-0">
        <v-form @submit.prevent="submit">
          <password-field
            v-model="form.current_password"
            :errors="formErrors?.current_password"
            label="Текущий пароль"
            placeholder="Введите текущий пароль"
          />
          <password-field
            v-model="form.new_password"
            :errors="formErrors?.new_password"
            label="Новый пароль"
            placeholder="Введите новый пароль"
          />
          <password-field
            v-model="form.new_password_confirm"
            :errors="formErrors?.new_password_confirm"
            label="Подтвердите пароль пароль"
            placeholder="Подтвердите новый пароль"
          />
          <div class="text-center mt-2">
            <v-btn type="submit" variant="outlined">Сохранить</v-btn>
          </div>
        </v-form>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<style scoped>
:deep(.v-label) {
  font-size: 18px;
}

:deep(.v-messages__message) {
  font-size: 16px;
}
</style>
