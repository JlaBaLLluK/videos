<script setup>

import {ref} from "vue";
import {userLogin, userRegister} from "@/api/index.js";
import {useRouter} from "vue-router";

let username = ref()
let email = ref()
let password = ref()
let passwordConfirm = ref()
let photo = ref()
let preview = ref()
let errorMessage = ref()

const router = useRouter()

function handleFileUpload(event) {
  const file = event.target.files[0]
  if (file) {
    photo.value = file
    preview.value = URL.createObjectURL(file)
  } else {
    photo.value = null
    preview.value = null
  }
}

function onRegistrationCLicked() {
  if (password.value !== passwordConfirm.value) {
    errorMessage.value = "Пароли не совпадают. Пожалуйста, проверьте ввод"
    return
  }

  const credentials = {
    "username": username.value,
    "email": email.value,
    "password": password.value,
    "profile_photo": photo.value,
  }
  userRegister(credentials)
      .then((success) => {
        if (success) {
          const loginCredentials = {
            "username_or_email": username.value,
            "password": password.value
          }
          userLogin(loginCredentials)
              .then((loginSuccess) => {
                if (loginSuccess) {
                  router.push("/")
                }
              })
        }
      })
}
</script>

<template>
  <h1>Register</h1>
  <form @submit.prevent novalidate enctype="multipart/form-data">
    <p>{{ errorMessage }}</p>
    <label for="username">Имя пользователя</label><input v-model="username" id="username"
                                                         placeholder="Имя пользователя"><br>
    <label for="email">Электронная почта</label><input v-model="email" id="email"
                                                       placeholder="Электронная почта" type="email"><br>
    <label for="password">Пароль</label><input v-model="password" id="password" type="password"
                                               placeholder="Пароль"><br>
    <label for="password_confirm">Повторите пароль</label><input v-model="passwordConfirm" id="password_confirm"
                                                                 type="password" placeholder="Пароль"><br>
    <label for="photo">Фото профиля</label><input type="file" id="photo" accept="image/*"
                                                  @change="handleFileUpload"><br>

    <div v-if="preview">
      <p>Предпросмотр:</p>
      <img :src="preview" alt="Предпросмотр" class="preview">
    </div>

    <button type="submit" @click="onRegistrationCLicked">Регистрация</button>
  </form>
</template>

<style scoped>
.preview {
  max-width: 200px;
  max-height: 200px;
  margin-top: 10px;
  border-radius: 10px;
}
</style>