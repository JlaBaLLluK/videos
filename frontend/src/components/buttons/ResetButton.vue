<script setup>
defineProps(['initial']);

const form = defineModel();

</script>

<template>
  <v-btn
    variant="outlined"
    width="200"
    class="mt-2"
    text="Отмена"
    @click="form = JSON.parse(JSON.stringify(initial))"
  />
</template>
