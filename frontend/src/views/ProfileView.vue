<script setup>
import {useRoute} from "vue-router";

const route = useRoute()
const username = route.params.username
</script>

<template>
<h1>Hello, {{username}}</h1>
</template>

<style scoped>

</style>