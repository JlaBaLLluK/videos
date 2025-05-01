<script setup>
defineEmits(['removeFromHistoryClicked']);
</script>

<template>
  <v-menu>
    <template v-slot:activator="{ props }">
      <v-btn icon v-bind="props" variant="plain">
        <v-icon>mdi-dots-vertical</v-icon>
      </v-btn>
    </template>
    <v-list>
      <v-list-item @click="$emit('removeFromHistoryClicked')">
        Удалить из истории
      </v-list-item>
    </v-list>
  </v-menu>
</template>
