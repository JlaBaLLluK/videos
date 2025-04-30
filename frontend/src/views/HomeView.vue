<script setup>
import {onMounted, ref} from 'vue';
import {addOrRemoveToWatchLater, getVideos} from '@/api/video.js';
import VideosList from '@/components/video/VideosList.vue';
import {infoToast} from '@/plugins/toasts.js';
import ProgressBar from '@/components/ProgressBar.vue';
import WatchLaterMenu from '@/components/video/menu/WatchLaterMenu.vue';

const videos = ref([]);
const loading = ref(true);

async function watchLater(videoId) {
  const data = await addOrRemoveToWatchLater(videoId);
  infoToast(data.message);
}

onMounted(async () => {
  videos.value = await getVideos('video/videos/');
  loading.value = false;
});
</script>

<template>
  <progress-bar v-if="loading" />
  <videos-list
    v-else
    v-model="videos"
    :display-author="true"
    no-data-text="Ещё нет видео"
  >
    <template #actions="{videoId}">
      <watch-later-menu text="Смотреть позже" @watch-later-clicked="watchLater(videoId)" />
    </template>
  </videos-list>
</template>
