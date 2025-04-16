<script setup>
import ProfileAvatar from '@/components/ProfileAvatar.vue';
import SubscribeButton from '@/components/SubscribeButton.vue';

defineProps({
  noDataText: {
    type: String
  },
  haveDataText: {
    type: String
  },
  needRemoveElement: {
    type: Boolean,
    default: false
  }
});

const items = defineModel('items');

function removeElement(username) {
  const removeIndex = items.value.indexOf(items.value.find((item) => item.username === username));
  items.value.splice(removeIndex, 1);
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
      >
        <div class="d-flex justify-space-between">
          <div
            class="d-flex ga-3 cursor-pointer"
            @click="$router.push({name: 'profile', params: {'username': item.username}})"
          >
            <profile-avatar
              :size="65"
              :username="item.username"
              :profile-photo="item.profile_photo"
            />
            <div class="d-flex flex-column">
              <span style="font-size: 1.1rem">{{ item?.channel_name || username }}</span>
              <span>{{ item.description_preview }}</span>
            </div>
          </div>
          <div class="d-flex align-center">
            <subscribe-button
              :user="item"
              :need-remove-element="needRemoveElement"
              @remove-element="removeElement"
            />
          </div>
        </div>
      </v-list-item>
    </v-list>
  </div>
</template>
