<script setup>
import { ref, defineProps } from 'vue'

const props = defineProps({
  initial_count: {
    type: Number,
    default: 100
  },
})


const count = ref(props.initial_count)
function increment() {
  count.value++
}
</script>

<template>
  <button @click="increment">Count is: {{ count }}</button>
</template>

