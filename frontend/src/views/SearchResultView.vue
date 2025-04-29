<script setup>
import {onMounted, ref, watch} from 'vue';
import {useRoute, useRouter} from 'vue-router';
import {search} from '@/api/index.js';
import ProgressBar from '@/components/ProgressBar.vue';
import FiltersRadioGroup from '@/components/core/FiltersRadioGroup.vue';

const route = useRoute();
const router = useRouter();

const displayFilterBlock = ref(false);
const contentType = ref();
const sorting = ref();
const data = ref({});
const loading = ref(true);

const CONTENT_TYPE_RADIOS = [
  {
    label: 'Видео',
    value: 'videos'
  },
  {
    label: 'Каналы',
    value: 'channels'
  },
  {
    label: 'Плейлисты',
    value: 'playlists'
  }
];
const VIDEOS_SORT_RADIOS = [
  {
    label: 'Сначала новые',
    value: 'newest'
  },
  {
    label: 'Сначала старые',
    value: 'oldest'
  },
  {
    label: 'Сначала популярные',
    value: 'popular'
  }
];
const CHANNELS_SORT_RADIOS = [
  {
    label: 'Недавняя активность',
    value: 'activity'
  },
  {
    label: 'По числу подписчиков',
    value: 'subscribers'
  }
];
const PLAYLISTS_SORT_RADIOS = [
  {
    label: 'По числу видео',
    value: 'videos'
  },
  {
    label: 'Недавнее обновление',
    value: 'recently_updated'
  }
];

watch(() => contentType.value,
  async (newValue) => {
    loading.value = true;
    data.value = await search({search_query: route.query.search_query, content_type: newValue});

    loading.value = false;
  });

onMounted(async () => {
  const queryParams = route.query;
  if (Object.keys(queryParams).length !== 1 || !Object.keys(queryParams).includes('search_query')) {
    await router.push({name: 'notFound'});
    return;
  }

  data.value = await search({search_query: queryParams.search_query});
  loading.value = false;
});
</script>

<template>
  <progress-bar v-if="loading" />
  <div>
    <v-btn
      prepend-icon="mdi-filter"
      text="Фильтр"
      variant="plain"
      class="fs-6 pa-0"
      @click="displayFilterBlock = !displayFilterBlock"
    />
    <div v-if="displayFilterBlock" class="d-flex ga-10">
      <div class="d-flex flex-column" style="width: 160px">
        <span class="fw-bold fs-5">Тип</span>
        <filters-radio-group v-model="contentType" :items="CONTENT_TYPE_RADIOS" />
      </div>
      <div v-if="contentType" style="width: 245px">
        <span class="fw-bold fs-5">Упорядочить</span>
        <filters-radio-group v-if="contentType === 'videos'" v-model="sorting" :items="VIDEOS_SORT_RADIOS" />
        <filters-radio-group v-else-if="contentType === 'channels'" v-model="sorting" :items="CHANNELS_SORT_RADIOS" />
        <filters-radio-group v-else-if="contentType === 'playlists'" v-model="sorting" :items="PLAYLISTS_SORT_RADIOS" />
      </div>
    </div>
    <h4 class="mt-2">Результаты поиска по запросу:</h4>
    <pre>{{ data }}</pre>
  </div>
</template>

<style scoped>

</style>
