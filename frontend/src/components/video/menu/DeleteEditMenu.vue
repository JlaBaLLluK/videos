<script setup>
defineEmits(['editClicked', 'deleteClicked']);
</script>

<template>
  <v-menu>
    <template v-slot:activator="{ props }">
      <v-btn icon v-bind="props" variant="plain">
        <v-icon>mdi-dots-vertical</v-icon>
      </v-btn>
    </template>
    <v-list>
      <v-list-item link @click="$emit('editClicked')">
        <div class="d-flex ga-3">
          <v-icon>mdi-pencil-outline</v-icon>
          <v-list-item-title>Редактировать</v-list-item-title>
        </div>
      </v-list-item>
      <v-list-item
        link
        class="text-danger ga-0"
        @click="$emit('deleteClicked')"
      >
        <div class="d-flex ga-3">
          <v-icon>mdi-delete-outline</v-icon>
          <v-list-item-title>Удалить</v-list-item-title>
        </div>
      </v-list-item>
    </v-list>
  </v-menu>
</template>
