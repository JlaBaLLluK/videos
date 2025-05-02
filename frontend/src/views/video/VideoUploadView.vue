<script setup>
import {onBeforeMount, ref} from 'vue';
import {useRoute, useRouter} from 'vue-router';
import baseAPI from '@/api/api.js';
import {successToast} from '@/plugins/toasts.js';
import {getMe} from '@/api/index.js';
import VideoForm from '@/components/video/VideoForm.vue';
import VideoUploadProgress from '@/components/video/VideoUploadProgress.vue';
import SubmitButton from '@/components/buttons/SubmitButton.vue';

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
    errors.value = null;
    await baseAPI.post('video/videos/', form.value, {
      timeout: 300000,
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent) => {
        uploadProgress.value = Math.round((progressEvent.loaded * 100) / progressEvent.total);
      },
    });
    successToast('Видео загружено успешно.');
    await getMe();
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
      <video-form v-model="form" :errors="errors">
        <v-file-input
          v-model="form.video"
          class="mt-3"
          label="Выберите видео"
          :error-messages="errors?.video"
        />
        <video-upload-progress v-if="!errors && uploadProgress > -1" v-model="uploadProgress" />
      </video-form>
      <div class="d-flex w-100 justify-center ga-3 mt-2">
        <submit-button text="Загрузить" />
      </div>
    </v-form>
  </div>
</template>
