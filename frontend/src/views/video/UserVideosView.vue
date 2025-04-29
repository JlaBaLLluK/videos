<script setup>
import VideosList from '@/components/video/VideosList.vue';
import {computed, onMounted, ref} from 'vue';
import ProgressBar from '@/components/ProgressBar.vue';
import {getVideos} from '@/api/video.js';
import {useRoute} from 'vue-router';

const route = useRoute();

const loading = ref(true);
const videos = ref([]);
const haveVideosText = computed(() => `Видео (${videos.value.length}):`);

onMounted(async () => {
  const response = await getVideos(`video/videos?by_username=${route.params.username}`);
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
      no-data-text="Пользователь пока не опубликовал видео."
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
            <v-list-item @click="watchLater(videoId)">
              Смотреть позже
            </v-list-item>
          </v-list>
        </v-menu>
      </template>
    </videos-list>
  </div>
</template>
