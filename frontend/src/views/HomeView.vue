<script setup>
import {onMounted, ref} from 'vue';
import {getVideos} from '@/api/video.js';
import PhotoWithDefault from '@/components/PhotoWithDefault.vue';

const videos = ref([]);

onMounted(async () => {
  const response = await getVideos('video/videos/');
  if (response.status === 200) {
    videos.value = response.data;
  }
});
</script>

<template>
  <div class="d-flex justify-center flex-wrap ga-10">
    <div v-for="video in videos" :key="video.id">
      <v-card width="350" height="480">
        <div class="d-flex flex-column h-100">
          <photo-with-default
            :size="350"
            :photo="video.preview"
          />
          <div class="d-flex ga-3 pt-3">
            <div class="cursor-pointer">
              <photo-with-default
                :text-placeholder="video.author_channel_name"
                :photo="video.author_profile_photo"
                :size="50"
                @click="$router.push({name: 'profile', params: {username: video.author_username}})"
              />
            </div>
            <div class="d-flex flex-column">
              <span style="font-size: 1.2em; font-weight: 600" class="cursor-pointer">{{ video.title }}</span>
              <span
                style="font-size: 1.05em"
                class="cursor-pointer"
                @click="$router.push({name: 'profile', params: {username: video.author_username}})"
              >
                {{ video.author_channel_name }}
              </span>
            </div>
          </div>
          <div class="d-flex h-100 align-end">
            <span>
              Просмотров: {{ video.views_count }} · {{ video.published_ago }}
            </span>
          </div>
        </div>
      </v-card>
    </div>
  </div>
</template>

<style scoped>

</style>
