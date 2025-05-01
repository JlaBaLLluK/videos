<script setup>
import {useRoute} from 'vue-router';
import {onMounted, ref} from 'vue';
import ProgressBar from '@/components/ProgressBar.vue';
import {getVideo} from '@/api/video.js';
import PhotoWithDefault from '@/components/PhotoWithDefault.vue';
import SubscribeButton from '@/components/SubscribeButton.vue';
import baseAPI from '@/api/api.js';
import CommentsList from '@/components/comment/CommentsList.vue';

const route = useRoute();

const loading = ref(true);
const video = ref({});
const visitorUsername = ref(JSON.parse(localStorage.getItem('user'))?.username);
const descriptionCollapsed = ref(true);
const likeIcon = ref('mdi-thumb-up');
const dislikeIcon = ref('mdi-thumb-down');

async function likeClicked() {
  const response = await baseAPI.post(`video/videos/${video.value.id}/like/`);
  if (response.data.is_set) {
    likeIcon.value = 'mdi-thumb-up';
    dislikeIcon.value = 'mdi-thumb-down-outline';
  } else {
    likeIcon.value += '-outline';
  }

  video.value.likes_count = response.data.new_likes_count;
  video.value.dislikes_count = response.data.new_dislikes_count;
}

async function dislikeClicked() {
  const response = await baseAPI.post(`video/videos/${video.value.id}/dislike/`);
  if (response.data.is_set) {
    likeIcon.value = 'mdi-thumb-up-outline';
    dislikeIcon.value = 'mdi-thumb-down';
  } else {
    dislikeIcon.value += '-outline';
  }

  video.value.likes_count = response.data.new_likes_count;
  video.value.dislikes_count = response.data.new_dislikes_count;
}

async function fetchComments() {
  const response = await baseAPI.get('comment/comments', {params: {by_video: video.value.id}});
  video.value.comments = response.data;
}

async function deleteComment(commentId) {
  await baseAPI.delete(`comment/comments/${commentId}/`);
  await fetchComments();
}

onMounted(async () => {
  video.value = await getVideo(route.params.id);
  if (!video.value.is_request_user_liked) {
    likeIcon.value += '-outline';
  }
  if (!video.value.is_request_user_disliked) {
    dislikeIcon.value += '-outline';
  }

  loading.value = false;
});
</script>

<template>
  <progress-bar v-if="loading" />
  <div v-else class="d-flex flex-column">
    <div class="d-flex justify-center">
      <h1>БЛОК ВИДЕО</h1>
    </div>
    <div class="d-flex w-50 justify-space-between">
      <div>
        <div>
          <h3 class="fw-bold">{{ video.title }}</h3>
        </div>
        <div class="d-flex ga-3">
          <photo-with-default :photo="video.author.profile_photo" :text-placeholder="video.author.channel_name" :size="65" />
          <div class="d-flex flex-column justify-space-between">
            <span class="fw-bold fs-5">{{ video.author.channel_name }}</span>
            <span class="fs-5">Подписчиков: {{ video.author.subscribers_count }}</span>
          </div>
          <div class="h-100 align-c">
            <subscribe-button v-if="video.author.username !== visitorUsername" class="ml-3" :user="video.author" />
          </div>
        </div>
      </div>
      <div class="d-flex align-center">
        <v-btn-group>
          <v-tooltip location="bottom" text="Нравится">
            <template v-slot:activator="{props}">
              <v-btn icon v-bind="props" @click="likeClicked">
                <v-icon size="30">{{ likeIcon }}</v-icon>
              </v-btn>
            </template>
          </v-tooltip>
          <div class="d-flex align-center ga-2" style="font-size: 20px">
            <span>{{ video.likes_count }}</span>
            <div style="border-right: solid 1px #b3b2b2; height: 40px"></div>
            <span>{{ video.dislikes_count }}</span>
          </div>
          <v-tooltip location="bottom" text="Не нравится">
            <template v-slot:activator="{props}">
              <v-btn icon v-bind="props" @click="dislikeClicked">
                <v-icon size="30">{{ dislikeIcon }}</v-icon>
              </v-btn>
            </template>
          </v-tooltip>
        </v-btn-group>
      </div>
    </div>
    <v-card class="mt-5 text-justify w-50">
      <v-card-title>
        <span style="font-weight: 600">Просмотров: {{ video.views_count }} · {{ video.published_ago }}</span>
      </v-card-title>
      <v-card-text style="font-size: 18px">
        <p v-if="descriptionCollapsed">
          {{ video.description_preview }}
          <b v-if="video.description !== video.description_preview" class="cursor-pointer" @click="descriptionCollapsed = false">
            ещё
          </b>
        </p>
        <p v-else>
          {{ video.description }}
          <br>
          <b class="cursor-pointer" @click="descriptionCollapsed = true">
            Свернуть
          </b>
        </p>
      </v-card-text>
    </v-card>
    <div class="mt-5 w-50">
      <comments-list
        v-model="video.comments"
        class="mt-5"
        :video-id="video.id"
        @comment-published="fetchComments"
        @comment-deleted="deleteComment"
      />
    </div>
  </div>
</template>

<style scoped>
:deep(.unsubscribe-button), :deep(.subscribe-button) {
  border-radius: 20px;
}
</style>
