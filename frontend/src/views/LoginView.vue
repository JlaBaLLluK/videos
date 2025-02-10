<script setup>
import {userLogin} from "@/api/index.js";
import {ref} from "vue";
import {useRouter} from "vue-router";

const usernameOrEmail = ref()
const password = ref()
const router = useRouter()

function onLoginClick() {
  const credentials = {
    "username_or_email": usernameOrEmail.value,
    "password": password.value
  }
  userLogin(credentials)
      .then((success) => {
        if (success) {
          router.push("/")
        }
      })
}
</script>

<template>
  <h1>Login</h1>
  <form @submit.prevent>
    <label for="username_input">Username or email</label><input v-model="usernameOrEmail" id="username_input"
                                                                type="text"
                                                                placeholder="username or email"><br>
    <label for="password_input">Password</label><input v-model="password" id="password_input" type="password"
                                                       placeholder="password"><br>
    <button type="submit" @click="onLoginClick">Login</button>
  </form>
</template>

<style scoped>

</style>