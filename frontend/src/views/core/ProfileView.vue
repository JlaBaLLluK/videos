<script setup>
import {onMounted, onUnmounted, ref} from 'vue';
import {useRoute} from 'vue-router';
import {getUserData} from '@/api/index.js';
import ProgressBar from '@/components/ProgressBar.vue';
import ProfileAvatar from '@/components/PhotoWithDefault.vue';
import SubscribeButton from '@/components/SubscribeButton.vue';
import UserDetail from '@/components/dialogs/UserDetail.vue';

const route = useRoute();

const user = ref({});
const username = ref(route.params.username);
const profilePhoto = ref(null);
const isChannelOwner = ref(false);
const detailDialogOpen = ref(false);

const subscribersCount = ref(0);
const loading = ref(true);

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
  subscribersCount.value = user.value.subscribers_count;
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
          :photo="profilePhoto"
          :text-placeholder="username"
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
          </div>
          <subscribe-button
            v-if="!isChannelOwner && user"
            :user="user"
            @update-subscribers-count="(newSubscribersCount) => subscribersCount = newSubscribersCount"
          />
        </div>
      </div>
    </div>
    <div class="w-50">
      <p class="mt-3 text-justify fs-5">
        {{ user?.description_preview }}
      </p>
      <div v-if="!['profileUpdate', 'videoUpload'].includes($route.name)" class="mt-n5">
        <b class="cursor-pointer" @click="detailDialogOpen=true">Ещё</b>
      </div>
      <div v-if="isChannelOwner" class="d-flex justify-start ga-5 mt-5">
        <v-btn variant="outlined" @click="$router.push({name: 'profileUpdate'})">
          Настроить информацию
        </v-btn>
        <v-btn variant="outlined" @click="$router.push({name: 'videoUpload'})">Загрузить видео</v-btn>
      </div>
    </div>
    <div class="mt-5 w-100">
      <router-view @profile-photo-changed="profilePhotoChanged" />
    </div>
  </div>
  <user-detail
    v-if="user"
    v-model="detailDialogOpen"
    :user="user"
  />
</template>
