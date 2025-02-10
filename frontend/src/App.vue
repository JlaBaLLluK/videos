<script setup>
import {onMounted, onUnmounted, ref} from "vue";
import {userLogout} from "@/api/index.js";

let isAuthenticated = ref(!!localStorage.getItem('refreshToken'))
const username = ref(localStorage.getItem("username"))

function isAuthenticatedUpdate() {
  isAuthenticated.value = !!localStorage.getItem('refreshToken')
  username.value = localStorage.getItem("username")
}

onMounted(() => {
  window.addEventListener("auth-changed", isAuthenticatedUpdate)
})

onUnmounted(() => {
  window.addEventListener("auth-changed", isAuthenticatedUpdate)
})

</script>

<template>
  <div class="site-container">
    <header>
      <nav class="navbar">
        <div class="header-left">
          <router-link to="/">
            Видео-Платформа
          </router-link>
        </div>
        <div class="header-right d-flex gap-4">
          <template v-if="isAuthenticated">
            <router-link :to="{name: 'profile', params: {'username': username}}">
              Профиль
            </router-link>
            <router-link to="/logout" @click="userLogout">
              Выход
            </router-link>
          </template>
          <template v-else>
            <router-link to="/login">
              Вход
            </router-link>
            <router-link to="/registration">
              Регистрация
            </router-link>
          </template>
        </div>
      </nav>
    </header>
    <router-view/>
  </div>

  <footer class="footer text-center">
    Footer
  </footer>
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
  font-size: 20px;
}

header a {
  text-decoration: none;
}

.header-left {
  padding-left: 30px;
}

.header-right {
  padding-right: 30px;
}

.footer {
  background-color: lightgray;
}

</style>

