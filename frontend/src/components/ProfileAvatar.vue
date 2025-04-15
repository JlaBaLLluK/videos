<script setup>
defineProps({
  size: {
    type: Number,
    default: 150
  },
  profilePhoto: {
    required: true,
  },
  username: {
    type: String,
    required: true,
  }
});

</script>

<template>
  <v-avatar :size="size" rounded="lg">
    <v-img v-if="profilePhoto" :src="profilePhoto" />
    <span v-else class="default-photo fs-1">{{ username[0].toUpperCase() }}</span>
  </v-avatar>
</template>

<style scoped>
.v-avatar {
  box-shadow: 0 0 10px 3px rgba(0, 0, 0, 0.15) !important;
}
</style>
