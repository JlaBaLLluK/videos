<script setup>
import DeleteEditMenu from '@/components/video/menu/DeleteEditMenu.vue';
import SubmitButton from '@/components/buttons/SubmitButton.vue';
import PhotoWithDefault from '@/components/PhotoWithDefault.vue';
import {ref} from 'vue';
import baseAPI from '@/api/api.js';

const emits = defineEmits(['commentEdit', 'commentDelete']);

const comment = defineModel();

const isCommentCollapsed = ref(true);
const commentEdit = ref(false);
const username = ref(JSON.parse(localStorage.getItem('user'))?.username);
const editedText = ref(comment.value.text);
const likeIcon = ref('mdi-thumb-up');
const dislikeIcon = ref('mdi-thumb-down');

async function likeClicked() {
  const response = await baseAPI.post(`comment/comments/${comment.value.id}/like/`);
  if (response.data.is_set) {
    likeIcon.value = 'mdi-thumb-up';
    dislikeIcon.value = 'mdi-thumb-down-outline';
  } else {
    likeIcon.value += '-outline';
  }

  comment.value.likes_count = response.data.new_likes_count;
  comment.value.dislikes_count = response.data.new_dislikes_count;
}

async function dislikeClicked() {
  const response = await baseAPI.post(`comment/comments/${comment.value.id}/like/`);
  if (response.data.is_set) {
    likeIcon.value = 'mdi-thumb-up-outline';
    dislikeIcon.value = 'mdi-thumb-down';
  } else {
    dislikeIcon.value += '-outline';
  }

  comment.value.likes_count = response.data.new_likes_count;
  comment.value.dislikes_count = response.data.new_dislikes_count;
}

async function submitEdit() {
  await baseAPI.patch(`comment/comments/${comment.value.id}/`, {text: editedText.value});
  commentEdit.value = false;
  emits('commentEdit');
}

</script>

<template>
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
        <!--              <like-dislike-buttons-->
        <!--                v-model="comments[index]"-->
        <!--                v-model:like-icon="likeIcon"-->
        <!--                v-model:dislike-icon="dislikeIcon"-->
        <!--                :size="20"-->
        <!--                @like-clicked="likeClicked(index)"-->
        <!--                @dislike-clicked="dislikeClicked(index)"-->
        <!--              />-->
      </div>
    </div>
    <div v-if="comment.author.username === username" class="d-flex justify-end">
      <delete-edit-menu
        @delete-clicked="$emit('commentDelete')"
        @edit-clicked="commentEdit = true"
      />
    </div>
  </div>
  <v-form
    v-if="commentEdit"
    class="mt-5"
    @submit.prevent="submitEdit"
  >
    <v-textarea
      v-model="editedText"
      label="Комментарий"
      placeholder="Введите комментарий"
    />
    <div class="d-flex justify-end ga-5">
      <v-btn class="mt-2" @click="commentEdit = false; editedText = comment.text">Отменить</v-btn>
      <submit-button text="Сохранить" :is-disabled="!comment.text.length" />
    </div>
  </v-form>
</template>
