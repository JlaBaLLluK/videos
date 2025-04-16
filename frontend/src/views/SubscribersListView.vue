<script setup>
import {onMounted, ref} from 'vue';
import {getUsersList} from '@/api/index.js';
import ProgressBar from '@/components/ProgressBar.vue';
import UsersList from '@/components/UsersList.vue';

const loading = ref(true);
const items = ref([]);

async function subscribeClicked(username) {
  const item = items.value.find((item) => item.username === username);
  item.is_request_user_subscribed = !item.is_request_user_subscribed;
}

onMounted(async () => {
  const {data} = await getUsersList('core/users/subscribers/');
  items.value = data;
  loading.value = false;
});
</script>

<template>
  <progress-bar v-if="loading" />
  <div v-else class="w-75">
    <users-list
      :items="items"
      no-data-text="У вас пока нет подписчиков"
      have-data-text="Ваши подписчики:"
      @subscribe-clicked="subscribeClicked"
    />
  </div>
</template>
