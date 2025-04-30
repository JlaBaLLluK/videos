<script setup>
import VideoForm from '@/components/video/VideoForm.vue';
import {onMounted, ref} from 'vue';
import ProgressBar from '@/components/ProgressBar.vue';
import baseAPI from '@/api/api.js';
import {useRoute, useRouter} from 'vue-router';
import {getFileFromUrl} from '@/utils/imageUtils.js';
import SubmitButton from '@/components/buttons/SubmitButton.vue';
import {editVideo} from '@/api/video.js';
import ResetButton from '@/components/buttons/ResetButton.vue';

const router = useRouter();
const route = useRoute();

const form = ref({
  title: '',
  description: '',
  preview: {},
  video: {}
});
const errors = ref({});
const loading = ref(true);
const initial = ref({});

async function getInitial() {
  const response = await baseAPI.get(`video/videos/${route.params.id}/`, {params: {isInitialReceive: true}});
  initial.value = response.data;
}

async function submit() {
  errors.value = {};
  const response = await editVideo(route.params.id, form.value);
  if (response.status !== 200) {
    errors.value = response.data;
  } else {
    await router.push({name: 'myVideos'});
  }
}

onMounted(async () => {
  await getInitial();
  form.value = {...initial.value};
  if (form.value.preview) {
    const file = await getFileFromUrl(`http://${import.meta.env.VITE_API_URL}${initial.value.preview}`);
    form.value.preview = file;
    initial.value.preview = file;
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
        <video-form v-model="form" :errors="errors" />
        <div class="d-flex justify-center w-100 ga-3 mt-2">
          <reset-button v-model="form" :initial="initial" />
          <submit-button text="Сохранить" />
        </div>
      </v-form>
    </div>
  </div>
</template>
