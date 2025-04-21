<script setup>
import {onBeforeMount, ref} from 'vue';
import {useRoute, useRouter} from 'vue-router';
import baseAPI from '@/api/api.js';
import {successToast} from '@/plugins/toasts.js';

const router = useRouter();
const route = useRoute();

const form = ref({
  title: '',
  description: '',
  preview: null,
  video: null,
});
const errors = ref({});
const uploadProgress = ref(-1);

async function submit() {
  try {
    uploadProgress.value = 0;
    await baseAPI.post('video/videos/', form.value, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent) => {
        uploadProgress.value = Math.round((progressEvent.loaded * 100) / progressEvent.total);
      },
    });
    successToast('Видео загружено успешно.');
    await router.push({name: 'profile'});
  } catch (error) {
    errors.value = error.response.data;
  }
}

onBeforeMount(() => {
  if (route.params.username !== JSON.parse(localStorage.getItem('user')).username) {
    router.push({name: 'profile', params: {username: route.params.name}});
  }
});
</script>

<template>
  <div class="w-50">
    <v-form @submit.prevent="submit">
      <v-text-field
        v-model="form.title"
        variant="outlined"
        density="compact"
        label="Название видео"
        placeholder="Введите название видео"
        :error-messages="errors.title"
      />
      <v-textarea
        v-model="form.description"
        class="mt-3"
        variant="outlined"
        density="compact"
        label="Описание видео"
        placeholder="Введите описание видео"
        :error-messages="errors.description"
      />
      <v-file-input
        v-model="form.preview"
        label="Выберите превью видео"
        :error-messages="errors.preview"
      />
      <v-file-input
        v-model="form.video"
        label="Выберите видео"
        :error-messages="errors.video"
      />
      <v-progress-linear
        v-if="uploadProgress > -1"
        v-model="uploadProgress"
        height="8"
      />
      <div class="d-flex w-100 justify-center ga-3">
        <v-btn
          variant="outlined"
          type="submit"
          width="200"
          class="mt-2"
        >
          Загрузить
        </v-btn>
      </div>
    </v-form>
  </div>
</template>
