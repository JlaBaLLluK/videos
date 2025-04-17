<script setup>
import {ref} from 'vue';

defineProps(['errors', 'placeholder', 'label']);

const model = defineModel();
const passwordShown = ref(false);
</script>

<template>
  <v-text-field
    v-model="model"
    class="mt-3"
    variant="outlined"
    density="compact"
    :label="label"
    :placeholder="placeholder"
    :type="passwordShown ? 'text' : 'password'"
    :append-inner-icon="passwordShown ? 'mdi-eye' : 'mdi-eye-off'"
    :error-messages="errors"
    @click:append-inner="passwordShown = !passwordShown"
  />
</template>

<style scoped>

</style>