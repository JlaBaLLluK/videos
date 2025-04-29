<script setup>
defineProps(['items']);

const model = defineModel();
</script>

<template>
  <v-radio-group v-model="model">
    <div v-for="item in items" :key="item" class="d-flex">
      <v-radio :label="item.label" :value="item.value" />
      <v-icon v-if="model === item.value" class="h-100 align-center" @click="model = null">mdi-close</v-icon>
    </div>
  </v-radio-group>
</template>
