<script setup>
import {onMounted, ref} from 'vue';
import {getSubscribersList} from '@/api/index.js';
import ProgressBar from '@/components/ProgressBar.vue';
import ProfileAvatar from '@/components/ProfileAvatar.vue';

const loading = ref(true);
const items = ref([]);

onMounted(async () => {
  const {data} = await getSubscribersList();
  items.value = data;
  loading.value = false;
});
</script>

<template>
  <progress-bar v-if="loading" />
  <div v-else class="w-75">
    <div v-if="!items">
      <h4>У вас пока нет подписчиков</h4>
    </div>
    <div v-else>
      <h4>Ваши подписчики:</h4>
      <v-list style="background: none !important; box-shadow: none !important;">
        <v-list-item
          v-for="(item, index) in items"
          :key="index"
          class="border-b pa-4"
          style="overflow: visible !important; background: none !important; box-shadow: none !important;"
          :to="{name: 'profile', params: {'username': item.username}}"
        >
          <div class="d-flex ga-3">
            <profile-avatar
              :size="65"
              :username="item.username"
              :profile-photo="item.profile_photo"
            />
            <div class="d-flex flex-column">
              <span style="font-size: 1.1rem">{{ item?.channel_name || username }}</span>
              <span>{{ item.description }}</span>
            </div>
          </div>
        </v-list-item>
      </v-list>
    </div>
  </div>
</template>
