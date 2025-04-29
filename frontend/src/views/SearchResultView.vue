<script setup>
import {onMounted} from 'vue';
import {useRoute, useRouter} from 'vue-router';
import {search} from '@/api/index.js';

const route = useRoute();
const router = useRouter();

onMounted(async () => {
  const queryParams = route.query;
  if (Object.keys(queryParams).length !== 1 || !Object.keys(queryParams).includes('search_query')) {
    await router.push({name: 'notFound'});
    return;
  }

  const data = await search(queryParams.search_query);
  console.log(data);
});
</script>

<template>
  <h4>Результаты поиска по запросу:</h4>
</template>

<style scoped>

</style>
