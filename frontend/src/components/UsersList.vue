<script setup>
import ProfileAvatar from '@/components/ProfileAvatar.vue';

defineProps(['items', 'noDataText', 'haveDataText']);
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
</template>

<style scoped>

</style>
