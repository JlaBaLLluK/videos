<script setup>
const model = defineModel();
</script>

<template>
  <v-progress-linear
    v-model="model"
    height="8"
  />
</template>
