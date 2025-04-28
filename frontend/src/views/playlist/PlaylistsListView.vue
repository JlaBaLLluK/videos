<script setup>
import {computed, ref} from 'vue';
import ProgressBar from '@/components/ProgressBar.vue';

const playlists = ref([]);
const loading = ref(false);
const userPlaylistsMessage = computed(() => `Ваши плейлисты (${playlists.value.length}):`);

</script>

<template>
  <progress-bar v-if="loading" />
  <div v-else>
    <h4 v-if="!playlists.length">
      Вы не создали ни одного плейлиста.
      <router-link :to="{name: 'playlistCreate'}">
        Создать?
      </router-link>
    </h4>
    <div v-else>
      <h4>{{ userPlaylistsMessage }}</h4>
    </div>
  </div>
</template>

<style scoped>

</style>
