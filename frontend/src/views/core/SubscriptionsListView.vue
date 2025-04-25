<script setup>
import {computed, onMounted, ref} from 'vue';
import {getUsersList} from '@/api/index.js';
import ProgressBar from '@/components/ProgressBar.vue';
import UsersList from '@/components/UsersList.vue';

const loading = ref(true);
const items = ref([]);
const haveDataText = computed(() => `Ваши подписки (${items.value.length}):`);

function subscribeClicked(username) {
  const itemIndex = items.value.indexOf(items.value.find((item) => item.username === username));
  items.value.splice(itemIndex, 1);
}

onMounted(async () => {
  const {data} = await getUsersList('core/users/subscriptions/');
  items.value = data;
  loading.value = false;
});
</script>

<template>
  <progress-bar v-if="loading" />
  <div v-else class="w-75">
    <users-list
      :items="items"
      no-data-text="У вас пока нет подписок"
      :have-data-text="haveDataText"
      :need-remove-element="true"
      @subscribe-clicked="subscribeClicked"
    />
  </div>
</template>
