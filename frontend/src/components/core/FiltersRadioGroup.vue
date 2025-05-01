<script setup>
import {computed} from 'vue';

defineProps({
  items: {
    type: Array,
    required: true
  },
  needChangeSortOrder: {
    type: Boolean,
    default: false
  }
});

const model = defineModel();
const isDescendingOrder = defineModel('isDescendingOrder');

const sortIcon = computed(() => isDescendingOrder.value ? 'mdi-chevron-down' : 'mdi-chevron-up');

</script>

<template>
  <v-radio-group v-model="model">
    <div v-for="item in items" :key="item" class="d-flex">
      <v-radio :label="item.label" :value="item.value" />
      <div v-if="model === item.value" class="d-flex">
        <v-icon v-if="needChangeSortOrder" class="h-100 align-center" @click="isDescendingOrder = !isDescendingOrder">{{ sortIcon }}</v-icon>
        <v-icon class="h-100 align-center" @click="model = null">mdi-close</v-icon>
      </div>
    </div>
  </v-radio-group>
</template>
