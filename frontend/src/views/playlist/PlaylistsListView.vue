<script setup>
import {computed, onMounted, ref} from 'vue';
import ProgressBar from '@/components/ProgressBar.vue';
import {deletePlaylist, getPlaylists} from '@/api/playlist.js';
import PhotoWithDefault from '@/components/PhotoWithDefault.vue';

const playlists = ref([]);
const loading = ref(true);
const userPlaylistsMessage = computed(() => `Ваши плейлисты (${playlists.value.length}):`);

async function handleDelete(playlistId) {
  await deletePlaylist(playlistId);
  playlists.value = await getPlaylists();
}

onMounted(async () => {
  playlists.value = await getPlaylists();
  loading.value = false;
});
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
      <div class="d-flex justify-space-between">
        <h4>{{ userPlaylistsMessage }}</h4>
        <v-btn :to="{name: 'playlistCreate'}">Создать</v-btn>
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
              <v-menu>
                <template v-slot:activator="{ props }">
                  <v-btn variant="plain" v-bind="props" icon>
                    <v-icon>mdi-dots-vertical</v-icon>
                  </v-btn>
                </template>
                <v-list>
                  <v-list-item link :to="{name: 'playlistEdit', params: {id: item.id}}">
                    <div class="d-flex ga-3">
                      <v-icon>mdi-pencil-outline</v-icon>
                      <v-list-item-title>Редактировать</v-list-item-title>
                    </div>
                  </v-list-item>
                  <v-list-item
                    link
                    class="text-danger ga-0"
                    @click="handleDelete(item.id)"
                  >
                    <div class="d-flex ga-3">
                      <v-icon>mdi-delete-outline</v-icon>
                      <v-list-item-title>Удалить</v-list-item-title>
                    </div>
                  </v-list-item>
                </v-list>
              </v-menu>
            </div>
          </div>
        </v-list-item>
      </v-list>
    </div>
  </div>
</template>

<style scoped>

</style>
