<script setup>
import {computed, onMounted, ref} from 'vue';
import {addOrRemoveToWatchLater, watchLaterVideos} from '@/api/video.js';
import VideosList from '@/components/video/VideosList.vue';
import {infoToast} from '@/plugins/toasts.js';
import ProgressBar from '@/components/ProgressBar.vue';

const videos = ref([]);
const loading = ref(true);
const haveDataText = computed(() => `Видео для просмотра позже (${videos.value.length}):`);

async function removeFromWatchLater(videoId) {
  const data = await addOrRemoveToWatchLater(videoId);
  infoToast(data.message);
  const indexToRemove = videos.value.indexOf(videos.value.find((video) => video.id === videoId));
  videos.value.splice(indexToRemove, 1);
}

onMounted(async () => {
  videos.value = await watchLaterVideos();
  loading.value = false;
});
</script>

<template>
  <progress-bar v-if="loading" />
  <videos-list
    v-else
    v-model="videos"
    :display-author="true"
    no-data-text="Тут еще ничего нет."
    :have-data-text="haveDataText"
  >
    <template #actions="{videoId}">
      <v-menu>
        <template v-slot:activator="{ props }">
          <v-btn icon v-bind="props" variant="plain">
            <v-icon>mdi-dots-vertical</v-icon>
          </v-btn>
        </template>
        <v-list>
          <v-list-item @click="removeFromWatchLater(videoId)">
            Убрать из плейлиста
          </v-list-item>
        </v-list>
      </v-menu>
    </template>
  </videos-list>
</template>
