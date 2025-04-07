<script setup>
import {ref} from "vue";
import {updateUserData} from "@/api/index.js";
import {useRouter} from "vue-router";

const emits = defineEmits(["updateDone"])

const router = useRouter();

const user = JSON.parse(localStorage.getItem('user'));

const form = ref({
  username: user.username,
  email: user.email,
  last_name: user.last_name,
  first_name: user.first_name,
  // profile_photo: "",
});
const errors = ref({});

async function submit() {
  const response = await updateUserData(user.username, form.value);
  if (response.status !== 200) {
    errors.value = response.data;
  } else {
    emits('updateDone');
    await router.push({name: 'profile', params: {username: response.data.username}});
  }
}
</script>

<template>
  <v-form @submit.prevent="submit">
    <v-text-field
        v-model="form.username"
        variant="outlined"
        density="compact"
        label="Имя пользователя"
        placeholder="Введите имя пользователя"
        :error-messages="errors.username"
    />
    <v-text-field
        class="mt-3"
        v-model="form.email"
        variant="outlined"
        density="compact"
        type="email"
        label="Электронная почта"
        placeholder="Введите электронную почту"
        :error-messages="errors.email"
    />
    <v-text-field
        class="mt-3"
        v-model="form.first_name"
        variant="outlined"
        density="compact"
        type="email"
        label="Имя"
        placeholder="Введите имя"
        :error-messages="errors.first_name"
    />
    <v-text-field
        class="mt-3"
        v-model="form.last_name"
        variant="outlined"
        density="compact"
        type="text"
        label="Фамилия"
        placeholder="Введите фамилия"
        :error-messages="errors.last_name"
    />
    <div class="w-100 text-center mt-3">
      <v-btn variant="outlined" type="submit">Сохранить</v-btn>
    </div>
  </v-form>
</template>

<style scoped>
:deep(.v-label) {
  font-size: 18px;
}

:deep(.v-messages__message) {
  font-size: 16px;
}
</style>
