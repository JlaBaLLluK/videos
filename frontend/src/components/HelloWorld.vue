<script setup>
import {ref} from "vue";

let clicks = ref(0);
defineProps({
  is_disabled: Boolean
});
function handleClick() {
  console.log("clicked");
  clicks.value += 1
}
</script>

<template>
  <button :disabled=is_disabled @click=handleClick>Clicked {{ clicks }}</button>
</template>
