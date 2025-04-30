<script setup>
import {computed, onMounted, ref} from 'vue';
import ProgressBar from '@/components/ProgressBar.vue';
import {deletePlaylist, getPlaylists} from '@/api/playlist.js';
import PlaylistsList from '@/components/playlist/PlaylistsList.vue';

const playlists = ref([]);
const loading = ref(true);
const userPlaylistsMessage = computed(() => `Ваши плейлисты (${playlists.value.length}):`);

async function handleDelete(playlistId) {
  await deletePlaylist(playlistId);
  playlists.value = await getPlaylists('/playlist/playlists?my_playlists=1');
}

onMounted(async () => {
  playlists.value = await getPlaylists('/playlist/playlists?my_playlists=1');
  loading.value = false;
});
</script>

<template>
  <progress-bar v-if="loading" />
  <div v-else>
    <playlists-list
      v-model="playlists"
      no-data-text="Вы не создали еще ни одного плейлиста."
      :show-playlist-create="true"
      :have-data-text="userPlaylistsMessage"
      detail-route-name="playlistDetail"
    >
      <template #actions="{playlistId}">
        <v-menu>
          <template v-slot:activator="{ props }">
            <v-btn variant="plain" v-bind="props" icon>
              <v-icon>mdi-dots-vertical</v-icon>
            </v-btn>
          </template>
          <v-list>
            <v-list-item link :to="{name: 'playlistEdit', params: {id: playlistId}}">
              <div class="d-flex ga-3">
                <v-icon>mdi-pencil-outline</v-icon>
                <v-list-item-title>Редактировать</v-list-item-title>
              </div>
            </v-list-item>
            <v-list-item
              link
              class="text-danger ga-0"
              @click="handleDelete(playlistId)"
            >
              <div class="d-flex ga-3">
                <v-icon>mdi-delete-outline</v-icon>
                <v-list-item-title>Удалить</v-list-item-title>
              </div>
            </v-list-item>
          </v-list>
        </v-menu>
      </template>
    </playlists-list>
  </div>
</template>
