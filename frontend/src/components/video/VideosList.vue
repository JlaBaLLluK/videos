<script setup>
import VideoPreview from '@/components/PhotoWithDefault.vue';
import PhotoWithDefault from '@/components/PhotoWithDefault.vue';

defineProps({
  haveDataText: {
    type: String,
    default: '',
  },
  noDataText: {
    type: String,
    default: '',
  },
  displayAuthor: {
    type: Boolean,
    default: false,
  },
});

const videos = defineModel();
</script>

<template>
  <div v-if="!videos || !videos.length">
    <h4>{{ noDataText }}</h4>
  </div>
  <div v-else>
    <h4>{{ haveDataText }}</h4>
    <div class="d-flex justify-start flex-wrap ga-5 mt-3">
      <v-card
        v-for="video in videos"
        :key="video.id"
        class="border-b pa-3"
        width="510"
      >
        <div class="d-flex justify-space-between align-center w-100">
          <div class="d-flex ga-3 w-100">
            <video-preview
              :text-placeholder="video.title"
              :photo="video.preview"
            />
            <div class="d-flex flex-column w-100">
              <div class="d-flex justify-space-between">
                <span class="fw-bold" style="font-size: 18px">{{ video.title }}</span>
                <slot name="actions" :videoId="video.id"></slot>
              </div>
              <span>Просмотров: {{ video.views_count }}</span>
              <span>{{ video.published_ago }}</span>
              <div class="d-flex h-100 align-end">
              </div>
            </div>
          </div>
        </div>
        <div
          v-if="displayAuthor"
          class="d-flex align-center ga-2 cursor-pointer mt-3 border-t pt-2"
          @click="$router.push({name: 'profile', params: {username: video.author_username}})"
        >
          <photo-with-default
            :text-placeholder="video.author_channel_name"
            :photo="video.author_profile_photo"
            :size="50"
          />
          <span>{{ video.author_channel_name }}</span>
        </div>
      </v-card>
    </div>
  </div>
</template>
