<script setup>

</script>

<template>
  <div class="d-flex justify-center h-75 align-center">
    <v-card class="pa-6 d-flex flex-column align-center">
      <v-card-title>
        <h1>404</h1>
      </v-card-title>
      <v-card-text>
        <h3>Страница не найдена</h3>
      </v-card-text>
      <v-card-actions>
        <v-btn
          variant="outlined"
          :to="{name: 'home'}"
        >
          На главную
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>
