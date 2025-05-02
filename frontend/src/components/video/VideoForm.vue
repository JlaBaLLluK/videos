<script setup>
import PhotoWithDefault from '@/components/PhotoWithDefault.vue';
import {ref, watch} from 'vue';

defineProps(['errors']);

const form = defineModel();

const videoPreview = ref(form.value.preview ? URL.createObjectURL(form.value.preview) : '');

watch(() => form.value.preview,
  (newValue) => {
    if (newValue) {
      videoPreview.value = URL.createObjectURL(newValue);
    }
  });
</script>

<template>
  <v-text-field
    v-model="form.title"
    variant="outlined"
    density="compact"
    label="Название видео"
    placeholder="Введите название видео"
    :error-messages="errors?.title"
  />
  <v-textarea
    v-model="form.description"
    class="mt-3"
    variant="outlined"
    density="compact"
    label="Описание видео"
    placeholder="Введите описание видео"
    :error-messages="errors?.description"
  />
  <slot></slot>
  <v-file-input
    v-model="form.preview"
    class="mt-3"
    label="Выберите превью видео"
    :error-messages="errors?.preview"
  />
  <div
    v-if="form.preview"
    class="d-flex flex-column align-center"
  >
    <photo-with-default class="text-center" :photo="videoPreview" :size="250" />
  </div>
</template>
