<script setup>
import {computed, ref} from 'vue';
import {getSubscribeButtonText} from '@/utils/userUtils.js';
import {subscribe} from '@/api/index.js';

const props = defineProps({
  user: {
    type: Object
  },
  needRemoveElement: {
    type: Boolean,
    default: false
  }
});
const emits = defineEmits(['updateSubscribersCount', 'removeElement']);

const isSubscribed = ref(props.user.is_request_user_subscribed);
const subscribeButtonText = computed(() => getSubscribeButtonText(isSubscribed.value));

async function click() {
  const response = await subscribe(props.user.username);
  isSubscribed.value = response.data.is_request_user_subscribed;
  emits('updateSubscribersCount', response.data.subscribers_count);
  if (props.needRemoveElement) {
    emits('removeElement', props.user.username);
  }
}

</script>

<template>
  <v-btn
    variant="outlined"
    width="150"
    class="mt-3"
    :class="isSubscribed ? 'unsubscribe-button' : 'subscribe-button'"
    @click.prevent="click"
  >
    {{ subscribeButtonText }}
  </v-btn>
</template>

<style scoped>
.subscribe-button {
  background-color: white !important;
  color: black !important;
}

.unsubscribe-button {
  background-color: #706f6f !important;
  color: #e3e0e0 !important;
}
</style>