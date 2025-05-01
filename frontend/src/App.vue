<script setup>
import {computed, onMounted, onUnmounted, ref, watch} from 'vue';
import {useRoute, useRouter} from 'vue-router';
import {userLogout} from '@/api/index.js';

const router = useRouter();
const route = useRoute();

const user = ref(JSON.parse(localStorage.getItem('user')));
const isAuthenticated = ref(!!user.value);
const isMenuOpened = ref(false);
const isSidebarCollapsed = ref(false);
const searchQuery = ref('');

const showSidebar = computed(() => !['registration', 'login', 'registrationConfirm'].includes(route.name));
const collapseSidebarIcon = computed(() => isSidebarCollapsed.value ? 'mdi-arrow-right' : 'mdi-arrow-left');

function userLoginEventHandler() {
  user.value = JSON.parse(localStorage.getItem('user'));
  isAuthenticated.value = true;
}

function userLogoutEventHandler() {
  isAuthenticated.value = false;
}

function toggleMenu() {
  if (!isAuthenticated.value) {
    isMenuOpened.value = false;
    router.push({name: 'login'});
  } else {
    isMenuOpened.value = true;
  }
}

async function logout() {
  isMenuOpened.value = false;
  await userLogout();
  await router.push({name: 'home'});
}


watch(() => route.name, (newValue) => {
  if (newValue === 'searchResult') {
    searchQuery.value = route.query.search_query;
  } else {
    searchQuery.value = '';
  }
});

onMounted(() => {
  window.addEventListener('user-login', userLoginEventHandler);
  window.addEventListener('user-logout', userLogoutEventHandler);
});

onUnmounted(() => {
  window.removeEventListener('user-login', userLoginEventHandler);
  window.removeEventListener('user-logout', userLogoutEventHandler);
});

</script>

<template>
  <v-app>
    <div class="site-container d-flex vh-100">
      <v-app-bar class="position-fixed pa-0">
        <nav class="navbar w-100 h-100">
          <div class="pl-5 h-100">
            <router-link to="/">
              <div class="d-flex h-100 align-center ga-2">
                <v-icon style="font-size: 40px;">mdi-video-outline</v-icon>
                <span>VidFlow</span>
              </div>
            </router-link>
          </div>
          <div class="w-25 h-100 d-flex">
            <v-text-field
              v-model="searchQuery"
              class="pl-3 search-field"
              placeholder="Введите запрос"
              clearable
              style="box-shadow: 0 0 8px rgba(0, 0, 0, 0.4); border-radius: 15px;"
              variant="plain"
              hide-details
              density="comfortable"
            />
            <v-btn icon @click="router.push({name: 'searchResult', query: {search_query: searchQuery}})">
              <v-icon>mdi-magnify</v-icon>
            </v-btn>
          </div>
          <div class="pr-5">
            <v-menu v-model="isMenuOpened">
              <template v-slot:activator="{ props }">
                <v-btn
                  v-bind="props"
                  icon
                  style="font-size: 24px;"
                  @click="toggleMenu"
                >
                  <v-icon>mdi-account</v-icon>
                </v-btn>
              </template>
              <v-list>
                <v-list-item :to="{name: 'profile', params: {username: user.username}}">
                  <v-list-item-title>Профиль</v-list-item-title>
                </v-list-item>
                <v-list-item @click="logout">
                  <v-list-item-title>Выход</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
          </div>
        </nav>
      </v-app-bar>
      <v-navigation-drawer v-if="showSidebar" :width="260" :rail="isSidebarCollapsed">
        <v-list class="d-flex flex-column h-100">
          <v-list-item link :to="{name: 'subscriptionsList'}">
            <div class="d-flex ga-3">
              <v-icon>mdi-account-group-outline</v-icon>
              <v-list-item-title>Подписки</v-list-item-title>
            </div>
          </v-list-item>
          <v-list-item link :to="{name: 'myVideos'}">
            <div class="d-flex ga-3">
              <v-icon>mdi-play-box-multiple-outline</v-icon>
              <v-list-item-title>Ваши видео</v-list-item-title>
            </div>
          </v-list-item>
          <v-list-item link :to="{name: 'myPlaylistsList'}">
            <div class="d-flex ga-3">
              <v-icon>mdi-playlist-play</v-icon>
              <v-list-item-title>Ваши плейлисты</v-list-item-title>
            </div>
          </v-list-item>
          <v-list-item link :to="{name: 'likesHistory'}">
            <div class="d-flex ga-3">
              <v-icon>mdi-thumb-up-outline</v-icon>
              <v-list-item-title>Понравившиеся</v-list-item-title>
            </div>
          </v-list-item>
          <v-list-item link :to="{name: 'watchLater'}">
            <div class="d-flex ga-3">
              <v-icon>mdi-clock-outline</v-icon>
              <v-list-item-title>Смотреть позже</v-list-item-title>
            </div>
          </v-list-item>
          <v-list-item link :to="{name: 'viewsHistory'}">
            <div class="d-flex ga-3">
              <v-icon>mdi-history</v-icon>
              <v-list-item-title>История просмотров</v-list-item-title>
            </div>
          </v-list-item>
          <v-spacer />
          <v-list-item class="pa-0 d-flex justify-end">
            <v-btn variant="text" :icon="collapseSidebarIcon" @click.stop="isSidebarCollapsed = !isSidebarCollapsed" />
          </v-list-item>
        </v-list>
      </v-navigation-drawer>
      <v-main>
        <div class="ma-6 h-100">
          <router-view :key="$route.fullPath" />
        </div>
      </v-main>
    </div>
  </v-app>
</template>

<style scoped>
header {
  background-color: #f1efef !important;
  height: 60px;
  position: fixed;
}

header a {
  text-decoration: none;
  font-size: 26px;
  color: black;
}

:deep(.v-navigation-drawer) {
  border: none;
  box-shadow: 4px 0 8px rgba(0, 0, 0, 0.15);
}

:deep(.v-list-item-title) {
  font-size: 18px;
}

:deep(.search-field .v-field__input) {
  margin: 0 !important;
  padding: 0 !important;
  display: flex;
  height: 100% !important;
  align-items: center;
}
</style>
