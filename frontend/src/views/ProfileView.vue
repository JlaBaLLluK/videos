<script setup>
import {onMounted, onUnmounted, ref} from "vue";
import {useRoute, useRouter} from "vue-router";
import {getUserData} from "@/api/index.js";

const router = useRouter();
const route = useRoute();

const username = route.params.username;
const isChannelOwner = ref(false);

onMounted(async () => {
  const user = JSON.parse(localStorage.getItem("user"));
  document.title = user.username.toString();
});

onUnmounted(() => {
  document.title = "VidFlow";
})
</script>

<template>
<h1>Hello, {{username}}</h1>
</template>

<style scoped>

</style>