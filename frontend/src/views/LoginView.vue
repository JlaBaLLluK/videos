<script setup>
import BaseAuthView from '@/views/base/BaseAuthView.vue';
import {ref} from 'vue';
import {useRouter} from 'vue-router';
import {userLogin} from '@/api/index.js';
import PasswordField from '@/components/PasswordField.vue';

const form = ref({
  username_or_email: '',
  password: '',
});
const formErrors = ref({});
const passwordShown = ref(false);

const router = useRouter();

async function submit() {
  const response = await userLogin(form.value);
  if (response.status >= 400) {
    formErrors.value = response.data;
  } else {
    await router.push({name: 'home'});
  }
}
</script>

<template>
  <base-auth-view>
    <v-form
      :class="{'mt-2': formErrors.detail, 'mt-6': !formErrors.detail}"
      @submit.prevent="submit"
    >
      <label
        v-if="formErrors.detail"
        class="wrong-cred fs-5 text-danger w-100 text-center mb-5"
      >
        {{ formErrors.detail }}
      </label>
      <v-text-field
        id="username"
        v-model="form.username_or_email"
        variant="outlined"
        density="compact"
        label="Имя пользователя или эл. почта"
        placeholder="Введите имя пользователя или эл. почту"
        :error-messages="formErrors.username_or_email"
      />
      <password-field
        v-model="form.password"
        :errors="formErrors.password"
        label="Пароль"
        placeholder="Введите пароль"
      />
      <div class="w-100 text-center">
        <v-btn variant="outlined" type="submit" class="mt-3">Войти</v-btn>
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

button {
  width: 400px;
  min-height: 45px;
}

:deep(.v-messages__message) {
  font-size: 16px;
}

</style>
