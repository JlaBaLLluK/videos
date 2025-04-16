<script setup>
import ProfileAvatar from '@/components/ProfileAvatar.vue';
import {getSubscribeButtonText} from '../utils/userUtils.js';
import {subscribe} from '@/api/index.js';

defineProps(['items', 'noDataText', 'haveDataText']);
const emits = defineEmits(['subscribeClicked']);

async function subscribeClicked(username) {
  await subscribe(username);
  emits('subscribeClicked', username);
}
</script>

<template>
  <div v-if="!items.length">
    <h4>{{ noDataText }}</h4>
  </div>
  <div v-else>
    <h4>{{ haveDataText }}</h4>
    <v-list>
      <v-list-item
        v-for="(item, index) in items"
        :key="index"
        class="border-b pa-4"
        :to="{name: 'profile', params: {'username': item.username}}"
      >
        <div class="d-flex justify-space-between">
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
          <div class="d-flex align-center">
            <v-btn
              variant="outlined"
              width="150"
              @click.prevent="subscribeClicked(item.username)"
            >
              {{ getSubscribeButtonText(item.is_subscribed) }}
            </v-btn>
          </div>
        </div>
      </v-list-item>
    </v-list>
  </div>
</template>

<style scoped>

</style>
