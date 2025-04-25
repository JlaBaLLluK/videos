<script setup>
import VideoPreview from '@/components/PhotoWithDefault.vue';

defineProps({
  displayActions: {
    type: Boolean,
    default: false
  },
  haveDataText: {
    type: String,
    default: '',
  },
  noDataText: {
    type: String,
    default: '',
  }
});

const videos = defineModel();
</script>

<template>
  <div v-if="!videos.length">
    <h4>{{ noDataText }}</h4>
  </div>
  <div v-else>
    <h4>{{ haveDataText }}</h4>
    <v-list>
      <v-list-item v-for="video in videos" :key="video.id" class="border-b pa-3">
        <div class="d-flex justify-space-between align-center">
          <div class="d-flex ga-3 cursor-pointer">
            <video-preview
              :size="65"
              :text-placeholder="video.title"
              :photo="video.preview"
            />
            <div class="d-flex flex-column">
              <span>{{ video.title }}</span>
              <span>Просмотров: {{ video.views_count }}</span>
            </div>
          </div>
          <slot name="actions" :videoId="video.id"></slot>
        </div>
      </v-list-item>
    </v-list>
  </div>
</template>
