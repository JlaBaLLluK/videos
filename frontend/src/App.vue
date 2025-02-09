<script setup>
import {computed} from "vue";

const isAuthenticated = computed(() => localStorage.getItem('refreshToken'))
</script>

<template>
  <div class="site-container">
    <header class="header">
      <div class="header-content h-100 d-flex justify-content-between align-items-center">
        <router-link to="/">
          <div class="header-left">
            <div>Видео-Платформа</div>
          </div>
        </router-link>

        <div class="header-right" v-if="isAuthenticated">
          <router-link to="/">
            <div>Профиль</div>
          </router-link>
          <router-link to="/">
            <div>Выйти</div>
          </router-link>
        </div>
        <div class="header-right" v-else>
          <router-link to="/register">
            <div>Регистрация</div>
          </router-link>
          <router-link to="/login">
            <div>Вход</div>
          </router-link>
        </div>

      </div>
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

.header {
  background-color: bisque;
  height: 50px;
  font-size: 20px;
}

.header a {
  text-decoration: none;
}

.header-left {
  padding-left: 15px;
}

.header-right {
  display: flex;
  gap: 25px;
  padding-right: 10px;
}

.footer {
  background-color: lightgray;
}

</style>

