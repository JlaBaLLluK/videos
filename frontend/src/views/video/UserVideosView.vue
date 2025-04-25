<script setup>
import VideosList from '@/components/video/VideosList.vue';
import {computed, onMounted, ref} from 'vue';
import ProgressBar from '@/components/ProgressBar.vue';
import {deleteVideo, getVideos} from '@/api/video.js';

const loading = ref(true);
const videos = ref([]);
const haveVideosText = computed(() => `Ваши видео (${videos.value.length}):`);

async function handleDelete(videoId) {
  await deleteVideo(videoId);
  const indexToDelete = videos.value.indexOf(videos.value.find((video) => video.id === videoId));
  videos.value.splice(indexToDelete, 1);
}

onMounted(async () => {
  const response = await getVideos('video/videos/my-published/');
  videos.value = response.data;
  loading.value = false;
});
</script>

<template>
  <progress-bar v-if="loading" />
  <div v-else>
    <videos-list
      v-model="videos"
      :display-actions="true"
      no-data-text="Вы пока не опубликовали ни одного видео."
      :have-data-text="haveVideosText"
    >
      <template #actions="{videoId}">
        <v-menu>
          <template v-slot:activator="{ props }">
            <v-btn icon v-bind="props" variant="plain">
              <v-icon>mdi-dots-vertical</v-icon>
            </v-btn>
          </template>
          <v-list>
            <v-list-item link :to="{name: 'videoEdit', params: {id: videoId}}">
              <div class="d-flex ga-3">
                <v-icon>mdi-pencil-outline</v-icon>
                <v-list-item-title>Редактировать</v-list-item-title>
              </div>
            </v-list-item>
            <v-list-item
              link
              class="text-danger ga-0"
              @click="handleDelete(videoId)"
            >
              <div class="d-flex ga-3">
                <v-icon>mdi-delete-outline</v-icon>
                <v-list-item-title>Удалить</v-list-item-title>
              </div>
            </v-list-item>
          </v-list>
        </v-menu>
      </template>
    </videos-list>
  </div>
</template>
