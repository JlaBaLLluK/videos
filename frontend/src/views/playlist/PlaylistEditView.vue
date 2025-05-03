<script setup>
import SubmitButton from '@/components/buttons/SubmitButton.vue';
import {onMounted, ref} from 'vue';
import ResetButton from '@/components/buttons/ResetButton.vue';
import baseAPI from '@/api/api.js';
import {useRoute, useRouter} from 'vue-router';
import VideosList from '@/components/video/VideosList.vue';
import ProgressBar from '@/components/ProgressBar.vue';
import {editPlaylist} from '@/api/playlist.js';

const router = useRouter();
const route = useRoute();

const initial = ref({});
const form = ref({});
const errors = ref({});
const loading = ref(true);

function moveVideo(videoId, source, destination) {
  const elem = source.find((item) => item.id === videoId);
  destination.push(elem);
  const index = source.indexOf(elem);
  source.splice(index, 1);
}

function addToPlaylist(videoId) {
  moveVideo(videoId, form.value.videos_outside_playlist, form.value.videos_in_playlist);
}

function removeFromPlaylist(videoId) {
  moveVideo(videoId, form.value.videos_in_playlist, form.value.videos_outside_playlist);
}

async function submit() {
  const response = await editPlaylist(route.params.id, form.value);
  if (response.status !== 200) {
    errors.value = response.data;
  } else {
    await router.push({name: 'myPlaylistsList'});
  }
}

onMounted(async () => {
  const response = await baseAPI.get(`playlist/playlists/${route.params.id}/initial/`);
  initial.value = response.data;
  form.value = JSON.parse(JSON.stringify(initial.value));
  loading.value = false;
});

</script>

<template>
  <progress-bar v-if="loading" />
  <div v-else>
    <h4>Редактирование плейлиста</h4>
    <v-form class="w-100 mt-4" @submit.prevent="submit">
      <v-text-field
        v-model="form.name"
        class="w-33"
        variant="outlined"
        density="compact"
        label="Название плейлиста"
        placeholder="Введите название плейлиста"
        :error-messages="errors.name"
      />
      <div class="d-flex">
        <div class="w-50">
          <span class="fs-5">Видео вне плейлиста:</span>
          <videos-list v-model="form.videos_outside_playlist" no-data-text="нет видео">
            <template #actions="{ videoId }">
              <v-tooltip text="Добавить в плейлист" location="bottom">
                <template v-slot:activator="{props}">
                  <v-btn
                    v-bind="props"
                    icon
                    variant="plain"
                    @click="addToPlaylist(videoId)"
                  >
                    <v-icon>mdi-plus</v-icon>
                  </v-btn>
                </template>
              </v-tooltip>
            </template>
          </videos-list>
        </div>
        <div class="w-50">
          <span class="fs-5">Видео в плейлисте:</span>
          <videos-list v-model="form.videos_in_playlist" no-data-text="нет видео">
            <template #actions="{ videoId }">
              <v-tooltip text="Убрать из плейлиста" location="bottom">
                <template v-slot:activator="{props}">
                  <v-btn
                    v-bind="props"
                    icon
                    variant="plain"
                    @click="removeFromPlaylist(videoId)"
                  >
                    <v-icon>mdi-minus</v-icon>
                  </v-btn>
                </template>
              </v-tooltip>
            </template>
          </videos-list>
        </div>
      </div>
      <div class="d-flex ga-5 mt-3">
        <reset-button v-model="form" :initial="initial" :init-with-json="true" />
        <submit-button text="Сохранить" />
      </div>
    </v-form>
  </div>
</template>
