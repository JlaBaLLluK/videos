<script setup>
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
  showPlaylistCreate: {
    type: Boolean,
    default: false
  }
});

const playlists = defineModel();
</script>

<template>
  <h4 v-if="!playlists.length">
    {{ noDataText }}
    <router-link v-if="showPlaylistCreate" :to="{name: 'playlistCreate'}">
      Создать?
    </router-link>
  </h4>
  <div v-else>
    <div class="d-flex justify-space-between mt-10">
      <h4>{{ haveDataText }}</h4>
      <v-btn v-if="showPlaylistCreate" :to="{name: 'playlistCreate'}">Создать</v-btn>
    </div>
    <v-list>
      <v-list-item v-for="item in playlists" :key="item.id" class="mb-3 border-b">
        <div class="d-flex justify-space-between">
          <div class="d-flex ga-3">
            <photo-with-default :size="85" :photo="item.playlist_preview" :text-placeholder="item.name" />
            <div>
              <span class="fs-5 fw-bold">{{ item.name }}</span><br>
              <span style="font-size: 1.2em">{{ item.videos_count }} видео</span>
            </div>
          </div>
          <div class="d-flex align-center">
            <slot name="actions" :playlistId="item.id"></slot>
          </div>
        </div>
      </v-list-item>
    </v-list>
  </div>
</template>
