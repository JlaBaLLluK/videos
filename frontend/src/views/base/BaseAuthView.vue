<script setup>
import {useRoute, useRouter} from 'vue-router';

const router = useRouter();
const route = useRoute();
const isRegistrationActive = ['registration', 'registrationConfirm'].includes(route.name);

</script>

<template>
  <div class="d-flex justify-center align-center h-75">
    <div class="p-5 border rounded shadow">
      <div class="d-flex justify-center gap-3" style="cursor: pointer; font-size: 22px;">
        <div class="px-3" :class="{ active: !isRegistrationActive }" @click="router.push({ name: 'login' })">
          Вход
        </div>
        <div class="px-3" :class="{ active: isRegistrationActive }" @click="router.push({ name: 'registration' })">
          Регистрация
        </div>
      </div>
      <slot></slot>
    </div>
  </div>
</template>

<style scoped>
.active {
  border-bottom: solid 2px black;
}
</style>
