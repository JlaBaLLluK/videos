<script setup>
import PasswordField from '@/components/PasswordField.vue';
import {ref} from 'vue';
import {userDelete} from '@/api/index.js';
import {useRoute, useRouter} from 'vue-router';

const router = useRouter();
const route = useRoute();

const password = ref('');
const formErrors = ref({});

const model = defineModel();

async function submit() {
  const response = await userDelete(route.params.username, password.value);
  if (response.status !== 204) {
    formErrors.value = response.data;
  } else {
    localStorage.removeItem('user');
    window.dispatchEvent(new Event('user-logout'));
    await router.push({name: 'home'});
  }
}
</script>

<template>
  <v-dialog v-model="model" persistent width="500">
    <v-card>
      <v-card-title class="pl-5 d-flex justify-space-between h-100 align-center">
        <h4>Удаление аккаунта</h4>
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
            v-model="password"
            :errors="formErrors?.password"
            label="Пароль"
            placeholder="Введите пароль"
          />
          <div class="text-center mt-2">
            <v-btn type="submit" variant="outlined" style="color: red">Удалить</v-btn>
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
