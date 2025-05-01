<script setup>
defineProps({
  text: {
    type: String,
    default: '',
  },
  isDisabled: {
    type: Boolean,
    default: false
  }
});
</script>

<template>
  <v-btn
    variant="outlined"
    type="submit"
    width="200"
    class="mt-2"
    :text="text"
    :disabled="isDisabled"
  />
</template>
