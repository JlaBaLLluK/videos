<script setup>
defineProps(['user']);

const model = defineModel();
</script>

<template>
  <v-dialog v-model="model" width="600" persistent>
    <v-card>
      <v-card-title class="pl-5 d-flex justify-space-between h-100 align-center">
        <h4>{{ user.username }}</h4>
        <v-btn
          icon
          style="border: none; box-shadow: none"
          class="pa-0 ma-0"
          @click="model = false"
        >
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>
      <v-card-text class="pt-0 pl-5">
        <h4>Описание</h4>
        <p class="text-justify">
          {{ user.description }}
        </p>
        <h4>Дополнительная информация</h4>
        <v-list class="pa-0">
          <v-list-item class="pa-0">
            <div class="d-flex ga-3">
              <v-icon>mdi-email-outline</v-icon>
              <v-list-item-title>{{ user.email }}</v-list-item-title>
            </div>
          </v-list-item>
          <v-list-item class="pa-0">
            <div class="d-flex ga-3">
              <v-icon>mdi-calendar-outline</v-icon>
              <v-list-item-title>Дата регистрации: {{ user.created_at }}</v-list-item-title>
            </div>
          </v-list-item>
          <v-list-item class="pa-0">
            <div class="d-flex ga-3">
              <v-icon>mdi-play-box-outline</v-icon>
              <v-list-item-title>{{ user.videos_count }} видео</v-list-item-title>
            </div>
          </v-list-item>
          <v-list-item class="pa-0">
            <div class="d-flex ga-3">
              <v-icon>mdi-trending-up</v-icon>
              <v-list-item-title>{{ user.total_views_count }} просмотров</v-list-item-title>
            </div>
          </v-list-item>
        </v-list>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>
