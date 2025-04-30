<script setup>
import {computed, onMounted, ref} from 'vue';
import ProgressBar from '@/components/ProgressBar.vue';
import {deletePlaylist, getPlaylists} from '@/api/playlist.js';
import PlaylistsList from '@/components/playlist/PlaylistsList.vue';
import {useRoute} from 'vue-router';

const route = useRoute();

const playlists = ref([]);
const loading = ref(true);

const isOwnPlaylists = computed(() => route.name === 'myPlaylistsList');
const noDataText = computed(() => isOwnPlaylists.value ? 'Вы не создали ни одного плейлиста.' : 'Пользователь не создал ни одного плейлиста.');
const userPlaylistsMessage = computed(() => isOwnPlaylists.value ? 'Ваши плейлисты ' : 'Плейлисты ');
const playlistsAmount = computed(() => `(${playlists.value.length}):`);

async function handleDelete(playlistId) {
  await deletePlaylist(playlistId);
  playlists.value = await getPlaylists('/playlist/playlists?my_playlists=1');
}

onMounted(async () => {
  let endpoint = '/playlist/playlists';
  if (isOwnPlaylists.value) {
    endpoint += '?my_playlists=1';
  } else {
    endpoint += `?by_username=${route.params.username}`;
  }

  playlists.value = await getPlaylists(endpoint);
  loading.value = false;
});
</script>

<template>
  <progress-bar v-if="loading" />
  <div v-else>
    <playlists-list
      v-model="playlists"
      :no-data-text="noDataText"
      :show-playlist-create="isOwnPlaylists"
      :have-data-text="userPlaylistsMessage + playlistsAmount"
      detail-route-name="playlistDetail"
    >
      <template v-if="isOwnPlaylists" #actions="{playlistId}">
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
