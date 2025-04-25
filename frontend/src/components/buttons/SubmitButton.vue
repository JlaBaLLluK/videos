<script setup>
defineProps(['text']);
</script>

<template>
  <v-btn
    variant="outlined"
    type="submit"
    width="200"
    class="mt-2"
    :text="text"
  />
</template>
