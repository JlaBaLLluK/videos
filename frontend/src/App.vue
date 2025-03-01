<script setup>
import {computed, ref} from "vue";
import {useRoute} from "vue-router";

const route = useRoute()

let isAuthenticated = ref(!!localStorage.getItem('refreshToken'));
const username = ref(localStorage.getItem("username"));
const routeName = computed(() => isAuthenticated.value ? "profile" : "registration");
const showSidebar = computed(() => !["registration", "login"].includes(route.name));
</script>

<template>
  <div class="site-container d-flex vh-100">
    <header class="w-100" style="position: fixed">
      <nav class="navbar">
        <div class="px-4">
          <router-link to="/">
            Видео-Платформа
          </router-link>
        </div>
        <div class="px-4">
          <router-link :to="{name: routeName, params: {username: username}}">Профиль</router-link>
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
}

header a {
  text-decoration: none;
  font-size: 22px;
}
</style>

