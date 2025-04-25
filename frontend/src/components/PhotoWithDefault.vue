<script setup>
defineProps({
  size: {
    type: Number,
    default: 150
  },
  photo: {
    required: true,
  },
  textPlaceholder: {
    type: String,
    required: true,
  }
});

</script>

<template>
  <v-avatar :size="size" rounded="lg">
    <v-img v-if="photo" :src="photo" />
    <span v-else class="default-photo fs-1">{{ textPlaceholder[0].toUpperCase() }}</span>
  </v-avatar>
</template>

<style scoped>
.v-avatar {
  box-shadow: 0 0 10px 3px rgba(0, 0, 0, 0.15) !important;
}
</style>
