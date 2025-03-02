<script setup>
import {computed, onMounted, onUnmounted, ref} from "vue";
import {useRoute, useRouter} from "vue-router";
import {userLogout} from "@/api/index.js";

const router = useRouter()
const route = useRoute();

const isAuthenticated = ref();
const username = ref();
const isMenuOpened = ref(false);
const showSidebar = computed(() => !["registration", "login"].includes(route.name));

function userLoginEventHandler() {
  isAuthenticated.value = true;
  username.value = localStorage.getItem("username");
}

function userLogoutEventHandler() {
  isAuthenticated.value = false;
  username.value = null;
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
  const storedUsername = localStorage.getItem("username");
  isAuthenticated.value = !!storedUsername;
  username.value = storedUsername || null;
  window.addEventListener("user-login", userLoginEventHandler);
  window.addEventListener("user-logout", userLogoutEventHandler);
});

onUnmounted(() => {
  window.removeEventListener("user-login", userLoginEventHandler);
  window.removeEventListener("user-logout", userLogoutEventHandler);
});

</script>

<template>
  <div class="site-container d-flex vh-100">
    <header class="w-100 d-flex align-center">
      <nav class="navbar d-flex align-center justify-space-between w-100">
        <div class="pl-5">
          <router-link to="/">
            Видео-Платформа
          </router-link>
        </div>
        <div class="pr-5">
          <v-menu v-model="isMenuOpened">
            <template v-slot:activator="{ props }">
              <v-btn v-bind="props" icon style="font-size: 24px; height: 40px; width: 40px;" @click="toggleMenu">
                <v-icon>mdi-account</v-icon>
              </v-btn>
            </template>
            <v-list>
              <v-list-item :to="{name: 'profile', params: {username: username}}">
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
    <aside v-if="showSidebar" class="sidebar d-flex flex-column p-3" style="margin-top: 50px; background-color: aqua">
      <router-link to="/history">История</router-link>
      <router-link to="/videos">Ваши видео</router-link>
      <router-link to="/liked">Понравившиеся</router-link>
    </aside>
    <div class="d-flex justify-center w-100">
      <router-view/>
    </div>
  </div>
</template>

<style>
body {
  margin: 0;
  padding: 0;
}
</style>

<style scoped>

header {
  background-color: bisque;
  height: 50px;
  position: fixed;
}

header a {
  text-decoration: none;
  font-size: 24px;
}
</style>

