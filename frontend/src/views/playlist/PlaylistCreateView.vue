<script setup>
import {ref} from 'vue';
import SubmitButton from '@/components/buttons/SubmitButton.vue';
import {createPlaylist} from '@/api/playlist.js';
import {useRouter} from 'vue-router';

const router = useRouter();

const form = ref({
  name: ''
});
const errors = ref({});

async function submit() {
  const response = await createPlaylist(form.value);
  if (response.status !== 201) {
    errors.value = response.data;
  } else {
    await router.push({name: 'myPlaylistsList'});
  }
}
</script>

<template>
  <h3>Создание плейлиста</h3>
  <v-form class="w-25 mt-4" @submit.prevent="submit">
    <v-text-field
      v-model="form.name"
      variant="outlined"
      density="compact"
      label="Название плейлиста"
      placeholder="Введите название плейлиста"
      :error-messages="errors.name"
    />
    <div class="w-100 d-flex justify-center">
      <submit-button text="Создать" />
    </div>
  </v-form>
</template>

<style scoped>

</style>
