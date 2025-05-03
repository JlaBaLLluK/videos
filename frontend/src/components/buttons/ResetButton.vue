<script setup>

import {onMounted, ref} from 'vue';

const props = defineProps({
  initial: {
    type: Object,
    required: true
  },
  initWithJson: {
    type: Boolean,
    default: false
  }
});

const form = defineModel();

const correctFormatData = ref({});

onMounted(() => {
  correctFormatData.value = props.initWithJson ? JSON.parse(JSON.stringify(props.initial)) : {...props.initial};
});

</script>

<template>
  <v-btn
    variant="outlined"
    width="200"
    class="mt-2"
    text="Отмена"
    @click="form = initWithJson ? JSON.parse(JSON.stringify(initial)) : {...initial}"
  />
</template>
