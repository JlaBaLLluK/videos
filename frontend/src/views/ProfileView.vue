<script setup>
import {onMounted, onUnmounted, ref} from 'vue';
import {useRoute} from 'vue-router';
import {getUserData} from '@/api/index.js';

const route = useRoute();

const user = ref({});
const username = ref(route.params.username);
const profilePhoto = ref(null);
const isChannelOwner = ref(false);

function profilePhotoChanged(photo) {
  if (photo) {
    profilePhoto.value = URL.createObjectURL(photo);
  } else {
    profilePhoto.value = null;
  }
}

onMounted(async () => {
  document.title = username.value.toString();
  user.value = JSON.parse(localStorage.getItem('user'));
  isChannelOwner.value = user.value?.username === username.value;
  if (!isChannelOwner.value) {
    const {data} = await getUserData(username.value);
    user.value = data;
  }

  profilePhoto.value = user.value.profile_photo;
});

onUnmounted(() => {
  document.title = 'VidFlow';
});
</script>

<template>
  <div class="ma-6">
    <div class="d-flex justify-start">
      <div class="d-flex justify-space-between align-center ga-5">
        <v-avatar size="150" rounded="lg">
          <v-img v-if="profilePhoto" :src="profilePhoto" />
          <span v-else class="default-photo fs-1">{{ username[0].toUpperCase() }}</span>
        </v-avatar>
        <div class="d-flex flex-column">
          <span class="fs-3">{{ user?.channel_name || username }}</span>
          <div>
            <span
              class="fs-5 cursor-pointer"
              @click="$router.push({name: 'profile', params: {username: username}})"
            >
              @{{ username }}
            </span>
            <span>
              · 99999 подписчиков · 555 видео
            </span>
          </div>
          <v-btn v-if="!isChannelOwner" variant="outlined" class="profile-btn w-50 mt-3">Подписаться</v-btn>
        </div>
      </div>
    </div>
    <div class="w-50">
      <p class="mt-3 text-justify fs-5">{{ user?.description }}</p>
      <div v-if="isChannelOwner" class="d-flex justify-start ga-5 mt-5">
        <v-btn variant="outlined" class="profile-btn" @click="$router.push({name: 'profileUpdate'})">
          Настроить информацию
        </v-btn>
        <v-btn variant="outlined" class="profile-btn">Управление видео</v-btn>
      </div>
      <div class="mt-5">
        <router-view @profile-photo-changed="profilePhotoChanged" />
      </div>
    </div>
  </div>
</template>

<style scoped>
:deep(.v-avatar) {
  box-shadow: 0 0 10px 4px rgba(0, 0, 0, 0.15);;
}

.profile-btn {
  border-radius: 10px;
  font-size: 14px;
}

</style>
