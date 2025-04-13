<script setup>
import {computed, onMounted, onUnmounted, ref} from 'vue';
import {useRoute, useRouter} from 'vue-router';
import {userLogout} from '@/api/index.js';

const router = useRouter();
const route = useRoute();

const user = ref(JSON.parse(localStorage.getItem('user')));
const isAuthenticated = ref(!!user.value);
const isMenuOpened = ref(false);
const isSidebarCollapsed = ref(false);

const showSidebar = computed(() => !['registration', 'login'].includes(route.name));
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
      <v-app-bar>
        <nav class="navbar w-100 h-100">
          <div class="pl-5 h-100">
            <router-link to="/">
              <div class="d-flex h-100 align-center ga-2">
                <v-icon style="font-size: 40px;">mdi-video-outline</v-icon>
                <span>VidFlow</span>
              </div>
            </router-link>
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
      <v-navigation-drawer v-if="showSidebar" :width="250" :rail="isSidebarCollapsed">
        <v-list class="d-flex flex-column h-100">
          <v-list-item link>
            <div class="d-flex ga-3">
              <v-icon>mdi-history</v-icon>
              <v-list-item-title>История</v-list-item-title>
            </div>
          </v-list-item>
          <v-list-item link>
            <div class="d-flex ga-3">
              <v-icon>mdi-playlist-play</v-icon>
              <v-list-item-title>Плейлисты</v-list-item-title>
            </div>
          </v-list-item>
          <v-list-item link>
            <div class="d-flex ga-3">
              <v-icon>mdi-play-box-multiple-outline</v-icon>
              <v-list-item-title>Ваши видео</v-list-item-title>
            </div>
          </v-list-item>
          <v-list-item link>
            <div class="d-flex ga-3">
              <v-icon>mdi-clock-outline</v-icon>
              <v-list-item-title>Смотреть позже</v-list-item-title>
            </div>
          </v-list-item>
          <v-list-item link>
            <div class="d-flex ga-3">
              <v-icon>mdi-thumb-up-outline</v-icon>
              <v-list-item-title>Понравившиеся</v-list-item-title>
            </div>
          </v-list-item>
          <v-spacer />
          <v-list-item class="pa-0 d-flex justify-end">
            <v-btn variant="text" :icon="collapseSidebarIcon" @click.stop="isSidebarCollapsed = !isSidebarCollapsed" />
          </v-list-item>
        </v-list>
      </v-navigation-drawer>
      <v-main class="">
        <router-view :key="$route.fullPath" />
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


</style>
