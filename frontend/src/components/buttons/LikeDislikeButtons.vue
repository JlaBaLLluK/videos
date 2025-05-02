<script setup>
defineProps(['size']);

defineEmits(['likeClicked', 'dislikeClicked']);

const model = defineModel();
const likeIcon = defineModel('likeIcon');
const dislikeIcon = defineModel('dislikeIcon');
</script>

<template>
  <v-btn-group>
    <v-tooltip location="bottom" text="Нравится">
      <template v-slot:activator="{props}">
        <v-btn icon v-bind="props" @click="$emit('likeClicked')">
          <v-icon :size="size">{{ likeIcon }}</v-icon>
        </v-btn>
      </template>
    </v-tooltip>
    <div class="d-flex align-center ga-1">
      <span>{{ model.likes_count }}</span>
      <div style="border-right: solid 1px #b3b2b2;" :style="{height: `${size}px`}"></div>
      <span>{{ model.dislikes_count }}</span>
    </div>
    <v-tooltip location="bottom" text="Не нравится">
      <template v-slot:activator="{props}">
        <v-btn icon v-bind="props" @click="$emit('dislikeClicked')">
          <v-icon :size="size">{{ dislikeIcon }}</v-icon>
        </v-btn>
      </template>
    </v-tooltip>
  </v-btn-group>
</template>
