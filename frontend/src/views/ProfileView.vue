<script setup>
import {onMounted, onUnmounted, ref} from 'vue';
import {useRoute} from 'vue-router';
import {getUserData, subscribe} from '@/api/index.js';
import ProgressBar from '@/components/ProgressBar.vue';
import ProfileAvatar from '@/components/ProfileAvatar.vue';

const route = useRoute();

const user = ref({});
const username = ref(route.params.username);
const profilePhoto = ref(null);
const isChannelOwner = ref(false);
const subscribeButtonText = ref('');
const subscribersCount = ref(0);
const loading = ref(true);

function profilePhotoChanged(photo) {
  if (photo) {
    profilePhoto.value = URL.createObjectURL(photo);
  } else {
    profilePhoto.value = null;
  }
}

async function subscribeClicked() {
  const response = await subscribe(username.value);
  setSubscribeButtonText(response.data.is_subscribed);
  subscribersCount.value = response.data.subscribers_count;
}

function setSubscribeButtonText(isSubscribed) {
  if (isSubscribed) {
    subscribeButtonText.value = 'Отписаться';
  } else {
    subscribeButtonText.value = 'Подписаться';
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
  subscribersCount.value = user.value.subscribers_count;
  setSubscribeButtonText(user.value.is_subscribed);
  loading.value = false;
});

onUnmounted(() => {
  document.title = 'VidFlow';
});
</script>

<template>
  <progress-bar v-if="loading" />
  <div v-else>
    <div class="d-flex justify-start">
      <div class="d-flex justify-space-between align-center ga-5">
        <profile-avatar
          :profile-photo="profilePhoto"
          :username="username"
        />
        <div class="d-flex flex-column">
          <span class="fs-3">{{ user?.channel_name || username }}</span>
          <div>
            <span
              class="fs-5 cursor-pointer"
              @click="$router.push({name: 'profile', params: {username: username}})"
            >
              @{{ username }}
            </span>
            <span
              :class="{'cursor-pointer': isChannelOwner}"
              @click="isChannelOwner ? $router.push({name: 'subscribersList'}) : null"
            >
              · {{ subscribersCount }} подписчика(ов)
            </span>
            <span>
              · {{ user.videos_count }} видео
            </span>
          </div>
          <v-btn
            v-if="!isChannelOwner"
            variant="outlined"
            class="profile-btn mt-3 w-75"
            @click="subscribeClicked"
          >
            {{ subscribeButtonText }}
          </v-btn>
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
    </div>
    <div class="mt-5 w-100">
      <router-view @profile-photo-changed="profilePhotoChanged" />
    </div>
  </div>
</template>

<style scoped>
.profile-btn {
  border-radius: 10px;
  font-size: 14px;
}

</style>
