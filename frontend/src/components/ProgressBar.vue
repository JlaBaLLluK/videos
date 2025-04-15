<script setup>

</script>

<template>
  <v-progress-linear indeterminate class="progress-bar" />
</template>

<style scoped>
:deep(.v-progress-linear__background) {
  background-color: white;
}

.progress-bar {
  color: gray !important;
  position: absolute;
  left: 0;
  top: 60px !important;
  width: 100%;
  z-index: 100000000;
}
</style>
