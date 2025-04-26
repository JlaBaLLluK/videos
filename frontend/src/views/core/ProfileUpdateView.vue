<script setup>
import {onBeforeMount, onMounted, ref, watch} from 'vue';
import {updateUserData} from '@/api/index.js';
import {useRoute, useRouter} from 'vue-router';
import UpdatePassword from '@/components/dialogs/UpdatePassword.vue';
import DeleteAccount from '@/components/dialogs/DeleteAccount.vue';
import {getFileFromUrl} from '@/utils/imageUtils.js';
import SubmitButton from '@/components/buttons/SubmitButton.vue';
import ResetButton from '@/components/buttons/ResetButton.vue';

const emits = defineEmits(['profilePhotoChanged']);

const router = useRouter();
const route = useRoute();

const user = JSON.parse(localStorage.getItem('user'));
const initial = ref({
  username: user.username,
  email: user.email,
  last_name: user.last_name,
  first_name: user.first_name,
  description: user.description,
});

const form = ref({});
const errors = ref({});
const profilePhotoPreview = ref(null);
const updatePasswordDialogOpen = ref(false);
const deleteAccountDialogOpen = ref(false);

async function submit() {
  const response = await updateUserData(user.username, form.value);
  if (response.status !== 200) {
    errors.value = response.data;
  } else {
    await router.push({name: 'profile', params: {username: response.data.username}});
  }
}

watch(
  () => form.value.profile_photo,
  (file) => {
    emits('profilePhotoChanged', file);
  }
);

onBeforeMount(() => {
  if (route.params.username !== JSON.parse(localStorage.getItem('user')).username) {
    router.push({name: 'profile', params: {username: route.params.username}});
  }
});

onMounted(async () => {
  form.value = {...initial.value};
  if (user.profile_photo) {
    profilePhotoPreview.value = user.profile_photo;
    const file = await getFileFromUrl(user.profile_photo);
    form.value.profile_photo = file;
    initial.value.profile_photo = file;
  }
});

</script>

<template>
  <div class="w-50">
    <v-form @submit.prevent="submit">
      <v-text-field
        v-model="form.username"
        variant="outlined"
        density="compact"
        label="Имя пользователя"
        placeholder="Введите имя пользователя"
        :error-messages="errors.username"
      />
      <v-text-field
        v-model="form.email"
        class="mt-3"
        variant="outlined"
        density="compact"
        type="email"
        label="Электронная почта"
        placeholder="Введите электронную почту"
        :error-messages="errors.email"
      />
      <v-text-field
        v-model="form.first_name"
        class="mt-3"
        variant="outlined"
        density="compact"
        type="email"
        label="Имя"
        placeholder="Введите имя"
        :error-messages="errors.first_name"
      />
      <v-text-field
        v-model="form.last_name"
        class="mt-3"
        variant="outlined"
        density="compact"
        type="text"
        label="Фамилия"
        placeholder="Введите фамилия"
        :error-messages="errors.last_name"
      />
      <v-textarea
        v-model="form.description"
        class="mt-3"
        variant="outlined"
        density="compact"
        type="text"
        label="Описание"
        placeholder="Введите описание"
        :error-messages="errors.description"
      />
      <v-file-input
        v-model="form.profile_photo"
        label="Выберите фото"
        :error-messages="errors.profile_photo"
      />
      <p class="cursor-pointer" style="font-size: 1.1rem" @click="updatePasswordDialogOpen = true"><u>Сменить пароль</u></p>
      <p class="cursor-pointer text-danger" style="font-size: 1.1rem" @click="deleteAccountDialogOpen = true"><u>Удалить аккаунт</u></p>
      <div class="d-flex w-100 justify-center ga-3">
        <reset-button v-model="form" :initial="initial" />
        <submit-button text="Сохранить" />
      </div>
    </v-form>
  </div>
  <update-password v-model="updatePasswordDialogOpen" />
  <delete-account v-model="deleteAccountDialogOpen" />
</template>
