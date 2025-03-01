<script setup>
import {useRoute, useRouter} from "vue-router";

const router = useRouter();
const route = useRoute();
const isRegistrationActive = route.name === "registration";

</script>

<template>
  <div class="d-flex justify-center align-center h-75">
    <div class="p-5 border rounded shadow bg-white">
      <div class="d-flex justify-center gap-3 mb-6" style="cursor: pointer; font-size: 22px;">
        <div class="px-3" :class="{ active: !isRegistrationActive }" @click="router.push({ name: 'login' })">
          Вход
        </div>
        <div class="px-3" :class="{ active: isRegistrationActive }" @click="router.push({ name: 'registration' })">
          Регистрация
        </div>
      </div>
      <slot/>
    </div>
  </div>
</template>

<style scoped>
.active {
  border-bottom: solid 2px black;
}
</style>