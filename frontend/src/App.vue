<script setup>
import {computed, onMounted, onUnmounted, ref, watch} from "vue";
import {useRoute, useRouter} from "vue-router";
import {userLogout} from "@/api/index.js";

const router = useRouter()
const route = useRoute();

const user = ref(JSON.parse(localStorage.getItem('user')));
const isAuthenticated = ref(!!user.value);
const isMenuOpened = ref(false);
const showSidebar = computed(() => !["registration", "login"].includes(route.name));

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
  window.addEventListener("user-login", userLoginEventHandler);
  window.addEventListener("user-logout", userLogoutEventHandler);
});

onUnmounted(() => {
  window.removeEventListener("user-login", userLoginEventHandler);
  window.removeEventListener("user-logout", userLogoutEventHandler);
});

</script>

<template>
  <v-app>
    <div class="site-container d-flex vh-100">
      <header class="w-100">
        <nav class="navbar w-100 h-100">
          <div class="pl-5 h-100">
            <router-link to="/">
              <div class="d-flex h-100 align-center">
                <v-icon style="font-size: 40px;">mdi-video-outline</v-icon>
                <span>VidFlow</span>
              </div>
            </router-link>
          </div>
          <div class="pr-5">
            <v-menu v-model="isMenuOpened">
              <template v-slot:activator="{ props }">
                <v-btn v-bind="props" icon style="font-size: 24px;" @click="toggleMenu">
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
      </header>
      <v-navigation-drawer v-if="showSidebar">
        <v-list-item link title="List Item 1" class="pl-5"></v-list-item>
        <v-list-item link title="List Item 2" class="pl-5"></v-list-item>
        <v-list-item link title="List Item 3" class="pl-5"></v-list-item>
      </v-navigation-drawer>
      <div class="d-flex justify-center w-100">
        <router-view/>
      </div>
    </div>
  </v-app>
</template>

<style scoped>
header {
  background-color: #dddddd;
  height: 60px;
  position: fixed;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  z-index: 2 !important;
}

header a {
  text-decoration: none;
  font-size: 26px;
  color: black;
}

:deep(.v-navigation-drawer) {
  padding-top: 10px;
  margin-top: 60px;
  width: 250px;
  background-color: #FFFFFF;
  border: none;
  box-shadow: 4px 0 8px rgba(0, 0, 0, 0.15);
  z-index: 1 !important;
}

:deep(.v-list-item-title) {
  font-size: 18px;
}


</style>

