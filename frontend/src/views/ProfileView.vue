<script setup>
import {onMounted, onUnmounted, ref} from "vue";
import {useRoute, useRouter} from "vue-router";
import {getUserData} from "@/api/index.js";

const router = useRouter();
const route = useRoute();

const username = route.params.username;
const isChannelOwner = ref(false);

onMounted(async () => {
  const userData = await getUserData(username);
  const storedUsername = localStorage.getItem("username");
  if (storedUsername === username) {
    isChannelOwner.value = true;

  }
  document.title = username.toString();
  console.log(userData);
});

onUnmounted(() => {
  document.title = "Videos";
})
</script>

<template>
<h1>Hello, {{username}}</h1>
</template>

<style scoped>

</style>