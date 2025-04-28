<script setup>
import {onMounted, ref} from 'vue';
import {getVideos} from '@/api/video.js';
import VideosList from '@/components/video/VideosList.vue';

const videos = ref([]);

async function watchLater(videoId) {

}

onMounted(async () => {
  const response = await getVideos('video/videos/');
  if (response.status === 200) {
    videos.value = response.data;
  }
});
</script>

<template>
  <videos-list v-model="videos" :display-author="true" no-data-text="Ещё нет видео">
    <template #actions="{videoId}">
      <v-menu>
        <template v-slot:activator="{ props }">
          <v-btn icon v-bind="props" variant="plain">
            <v-icon>mdi-dots-vertical</v-icon>
          </v-btn>
        </template>
        <v-list>
          <v-list-item @click="watchLater(videoId)">
            Смотреть позже
          </v-list-item>
        </v-list>
      </v-menu>
    </template>
  </videos-list>
</template>

<style scoped>

</style>
