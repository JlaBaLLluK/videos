<script setup>
import {computed, onMounted, ref} from 'vue';
import ProgressBar from '@/components/ProgressBar.vue';
import {useRoute} from 'vue-router';
import {getPlaylistDetail} from '@/api/playlist.js';
import VideosList from '@/components/video/VideosList.vue';

const route = useRoute();

const playlist = ref({});
const loading = ref(true);
const haveDataText = computed(() => `${playlist.value.name} (${playlist.value.videos.length} видео):`);

onMounted(async () => {
  playlist.value = await getPlaylistDetail(route.params.id);
  loading.value = false;
});

</script>

<template>
  <progress-bar v-if="loading" />
  <div v-else>
    <videos-list
      v-model="playlist.videos"
      no-data-text="В плейлисте еще нет видео."
      :have-data-text="haveDataText"
    />
  </div>
</template>
