<script setup>
import {computed, onMounted, ref} from 'vue';
import ProgressBar from '@/components/ProgressBar.vue';
import {getPlaylists} from '@/api/playlist.js';
import PlaylistsList from '@/components/playlist/PlaylistsList.vue';
import {useRoute} from 'vue-router';

const route = useRoute();

const playlists = ref([]);
const loading = ref(true);
const userPlaylistsMessage = computed(() => `Плейлисты (${playlists.value.length}):`);

onMounted(async () => {
  playlists.value = await getPlaylists(`playlist/playlists?by_username=${route.params.username}`);
  loading.value = false;
});
</script>

<template>
  <progress-bar v-if="loading" />
  <div v-else>
    <playlists-list
      v-model="playlists"
      no-data-text="Пользователь пока не создал ни одного плейлиста."
      :have-data-text="userPlaylistsMessage"
      detail-route-name="userPlaylistDetail"
    />
  </div>
</template>
