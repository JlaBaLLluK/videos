<script setup>

</script>

<template>
  <div class="site-container">
    <header class="header">
      <div class="header-container w-100 h-100">
        <div class="header-content h-100 d-flex justify-content-between align-items-center">
          <router-link to="/">
            <div class="header-left">
              <div>Видео-Платформа</div>
            </div>
          </router-link>
          <router-link to="/">
            <div class="header-right">
              <div class="to-profile right">Профиль</div>
            </div>
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
  height: 50px
}

.header-right, .header-left {
  background-color: aqua;
}

.footer {
  background-color: lightgray;
}

</style>

