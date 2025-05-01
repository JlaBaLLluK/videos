<script setup>
import VideosList from '@/components/video/VideosList.vue';
import {computed, onMounted, ref} from 'vue';
import ProgressBar from '@/components/ProgressBar.vue';
import {addOrRemoveToWatchLater, deleteVideo, getVideos} from '@/api/video.js';
import {useRoute} from 'vue-router';
import {infoToast} from '@/plugins/toasts.js';
import WatchLaterMenu from '@/components/video/menu/WatchLaterMenu.vue';
import DeleteEditMenu from '@/components/video/menu/DeleteEditMenu.vue';
import RemoveFromHistoryMenu from '@/components/video/menu/RemoveFromHistoryMenu.vue';
import baseAPI from '@/api/api.js';

const route = useRoute();

const loading = ref(true);
const videos = ref([]);
const noDataText = ref('');
const endpoint = ref('video/videos');
const watchLaterMenuText = ref('');

const haveDataText = computed(() => `Видео (${videos.value.length}):`);

async function watchLater(videoId) {
  const data = await addOrRemoveToWatchLater(videoId);
  infoToast(data.message);
  videos.value = await getVideos(endpoint.value);
}

async function handleDelete(videoId) {
  await deleteVideo(videoId);
  videos.value = await getVideos(endpoint.value);
}

async function removeFromHistory(videoId) {
  await baseAPI.put(`video/videos/${videoId}/remove-from-history/`);
  videos.value = await getVideos(endpoint.value);
}

onMounted(async () => {
  if (route.name === 'myVideos') {
    endpoint.value += '?my-published=1';
    noDataText.value = 'Вы пока не опубликовали ни одного видео.';
  } else if (route.name === 'watchLater') {
    endpoint.value += '/watch-later/';
    noDataText.value = 'Вы еще не добавили сюда ни одного видео.';
    watchLaterMenuText.value = 'Убрать из плейлиста';
  } else if (route.name === 'userVideos') {
    endpoint.value += `?by_username=${route.params.username}`;
    noDataText.value = 'Пользователь пока не опубликовал ни одного видео.';
    watchLaterMenuText.value = 'Смотреть позже';
  } else if (route.name === 'likesHistory') {
    endpoint.value += '?likes_history=1';
    noDataText.value = 'Вы не отметили ни одно видео как понравившееся.';
  } else if (route.name === 'viewsHistory') {
    endpoint.value += '?views_history=1';
    noDataText.value = 'Вы не посмотрели ни одно видео';
  }

  videos.value = await getVideos(endpoint.value);
  loading.value = false;
});
</script>

<template>
  <progress-bar v-if="loading" />
  <div v-else>
    <videos-list
      v-model="videos"
      :no-data-text="noDataText"
      :have-data-text="haveDataText"
    >
      <template #actions="{videoId}">
        <delete-edit-menu
          v-if="route.name === 'myVideos'"
          @delete-clicked="handleDelete(videoId)"
          @edit-clicked="$router.push({name: 'videoEdit', params: {id: videoId}})"
        />
        <watch-later-menu
          v-else-if="['watchLater', 'userVideos'].includes(route.name)"
          :text="watchLaterMenuText"
          @watch-later-clicked="watchLater(videoId)"
        />
        <remove-from-history-menu
          v-else-if="route.name === 'viewsHistory'"
          @remove-from-history-clicked="removeFromHistory(videoId)"
        />
      </template>
    </videos-list>
  </div>
</template>
