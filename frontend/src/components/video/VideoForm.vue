<script setup>
defineProps(['errors']);

const form = defineModel();
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
  <v-file-input
    v-model="form.preview"
    label="Выберите превью видео"
    :error-messages="errors?.preview"
  />
  <v-file-input
    v-model="form.video"
    label="Выберите видео"
    :error-messages="errors?.video"
  />
  <slot name="uploadProgress"></slot>
</template>
