<script setup>
import VideoForm from '@/components/video/VideoForm.vue';
import {onMounted, ref} from 'vue';
import VideoUploadProgress from '@/components/video/VideoUploadProgress.vue';
import ProgressBar from '@/components/ProgressBar.vue';
import baseAPI from '@/api/api.js';
import {useRoute, useRouter} from 'vue-router';
import {getFileFromUrl} from '@/utils/imageUtils.js';
import SubmitButton from '@/components/buttons/SubmitButton.vue';
import {editVideo} from '@/api/video.js';

const router = useRouter();
const route = useRoute();

const form = ref({
  title: '',
  description: '',
  preview: {},
  video: {}
});
const errors = ref({});
const uploadProgress = ref(0);
const loading = ref(true);

async function getInitial() {
  const response = await baseAPI.get(`video/videos/${route.params.id}/`, {params: {isInitialReceive: true}});
  return response.data;
}

async function submit() {
  errors.value = {};
  const response = await editVideo(route.params.id, form.value);
  if (response.status !== 200) {
    errors.value = response.data;
  } else {
    await router.push({name: 'publishedVideos'});
  }
}

onMounted(async () => {
  const initial = await getInitial();
  form.value = {...initial};
  if (form.value.preview) {
    form.value.preview = await getFileFromUrl(`http://${import.meta.env.VITE_API_URL}${initial.preview}`);
  }

  loading.value = false;
});
</script>

<template>
  <progress-bar v-if="loading" />
  <div v-else class="w-50">
    <h4>Редактирование видео</h4>
    <div class="mt-5">
      <v-form @submit.prevent="submit">
        <video-form v-model="form" :errors="errors">
          <video-upload-progress v-if="!errors" v-model="uploadProgress" />
          <div class="d-flex justify-center w-100 ga-3">
            <submit-button text="Сохранить" />
          </div>
        </video-form>
      </v-form>
    </div>
  </div>
</template>
