<script setup>
import {ref} from 'vue';
import {useRoute} from 'vue-router';
import SubmitButton from '@/components/buttons/SubmitButton.vue';
import baseAPI from '@/api/api.js';
import PhotoWithDefault from '@/components/PhotoWithDefault.vue';
import DeleteEditMenu from '@/components/video/menu/DeleteEditMenu.vue';

const emits = defineEmits(['commentPublished', 'commentDeleted']);

const route = useRoute();

const comments = defineModel();

const isCommentCollapsed = ref(true);
const username = ref(JSON.parse(localStorage.getItem('user'))?.username);
const commentToEditId = ref(0);

const form = ref({
  text: '',
  video: Number(route.params.id),
});

async function submit() {
  await baseAPI.post('comment/comments/', form.value);
  form.value.text = '';
  emits('commentPublished');
}

async function submitEdit(commentId, commentText) {
  await baseAPI.patch(`comment/comments/${commentId}/`, {text: commentText});
  commentToEditId.value = 0;
  emits('commentPublished');
}

</script>

<template>
  <v-form @submit.prevent="submit">
    <v-textarea
      v-model="form.text"
      label="Комментарий"
      placeholder="Введите комментарий"
    />
    <div class="d-flex justify-end">
      <submit-button text="Оставить" :is-disabled="!form.text.length" />
    </div>
  </v-form>
  <h4 v-if="!comments || !comments.length">Комментариев нет.</h4>
  <div v-else>
    <h4>Комментарии ({{ comments.length }}):</h4>
    <v-list>
      <v-list-item v-for="comment in comments" :key="comment.id" class="border-b pa-4">
        <div class="d-flex ga-2 justify-space-between">
          <div class="d-flex ga-3">
            <photo-with-default
              class="cursor-pointer"
              :photo="comment.author.profile_photo"
              :text-placeholder="comment.author.channel_name"
              :size="60"
              @click="$router.push({name: 'profile', params: {username: comment.author.username}})"
            />
            <div class="d-flex flex-column">
              <div class="d-flex ga-2">
                <span
                  class="fw-bold cursor-pointer"
                  @click="$router.push({name: 'profile', params: {username: comment.author.username}})"
                >
                  {{ comment.author.channel_name }}
                </span>
                <span style="color: gray">{{ comment.published_ago }}</span>
              </div>
              <p v-if="isCommentCollapsed" class="text-justify">
                {{ comment.text_preview }}
                <b
                  v-if="comment.text !== comment.text_preview"
                  class="cursor-pointer"
                  @click="isCommentCollapsed = false"
                >
                  ещё
                </b>
              </p>
              <p v-else class="text-justify">
                {{ comment.text }}<br>
                <b
                  v-if="comment.text !== comment.text_preview"
                  class="cursor-pointer"
                  @click="isCommentCollapsed = true"
                >
                  Свернуть
                </b>
              </p>
            </div>
          </div>
          <div v-if="comment.author.username === username" class="d-flex justify-end">
            <delete-edit-menu
              @delete-clicked="$emit('commentDeleted', comment.id)"
              @edit-clicked="commentToEditId = comment.id"
            />
          </div>
        </div>
        <v-form
          v-if="commentToEditId === comment.id"
          class="mt-5"
          @submit.prevent="submitEdit(comment.id, comment.text)"
        >
          <v-textarea
            v-model="comment.text"
            label="Комментарий"
            placeholder="Введите комментарий"
          />
          <div class="d-flex justify-end ga-5">
            <v-btn class="mt-2" @click="commentToEditId = 0">Отменить</v-btn>
            <submit-button text="Сохранить" :is-disabled="!comment.text.length" />
          </div>
        </v-form>
      </v-list-item>
    </v-list>
  </div>
</template>
