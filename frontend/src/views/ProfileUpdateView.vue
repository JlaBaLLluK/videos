<script setup>
import {onMounted, ref, watch} from 'vue';
import {updateUserData} from '@/api/index.js';
import {useRouter} from 'vue-router';

const emits = defineEmits(['profilePhotoChanged']);

const router = useRouter();

const user = JSON.parse(localStorage.getItem('user'));

const form = ref({
  username: user.username,
  email: user.email,
  last_name: user.last_name,
  first_name: user.first_name,
  description: user.description,
  profile_photo: null,
});
const errors = ref({});
const profilePhotoPreview = ref(null);

async function submit() {
  const response = await updateUserData(user.username, form.value);
  if (response.status !== 200) {
    errors.value = response.data;
  } else {
    await router.push({name: 'profile', params: {username: response.data.username}});
  }
}

watch(
  () => form.value.profile_photo,
  (file) => {
    emits('profilePhotoChanged', file);
  }
);

onMounted(async () => {
  if (user.profile_photo) {
    profilePhotoPreview.value = user.profile_photo;
    const response = await fetch(user.profile_photo);
    const fileName = response.url.split('/').pop();
    const blob = await response.blob();
    form.value.profile_photo = new File([blob], fileName, { type: blob.type });
  }
});

</script>

<template>
  <div class="w-50">
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
        v-model="form.email"
        class="mt-3"
        variant="outlined"
        density="compact"
        type="email"
        label="Электронная почта"
        placeholder="Введите электронную почту"
        :error-messages="errors.email"
      />
      <v-text-field
        v-model="form.first_name"
        class="mt-3"
        variant="outlined"
        density="compact"
        type="email"
        label="Имя"
        placeholder="Введите имя"
        :error-messages="errors.first_name"
      />
      <v-text-field
        v-model="form.last_name"
        class="mt-3"
        variant="outlined"
        density="compact"
        type="text"
        label="Фамилия"
        placeholder="Введите фамилия"
        :error-messages="errors.last_name"
      />
      <v-textarea
        v-model="form.description"
        class="mt-3"
        variant="outlined"
        density="compact"
        type="text"
        label="Описание"
        placeholder="Введите описание"
        :error-messages="errors.description"
      />
      <v-file-input
        v-model="form.profile_photo"
        label="Выберите фото"
        :error-messages="errors.profile_photo"
      />
      <div class="text-center mt-3">
        <v-btn variant="outlined" type="submit" width="200">Сохранить</v-btn>
      </div>
    </v-form>
  </div>
</template>

<style scoped>
:deep(.v-label) {
  font-size: 18px;
}

:deep(.v-messages__message) {
  font-size: 16px;
}
</style>
