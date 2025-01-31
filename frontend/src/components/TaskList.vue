<script setup>
  import {ref} from "vue";

  let task = ref('');
  let tasksList = ref([]);

  function addTask() {
    if (task.value.trim()) {
      tasksList.value.push(task.value);
      task.value = "";
    }
  }

  function removeTask(index) {
    tasksList.value.splice(index, 1);
  }
</script>

<template>
  <div>
    <h2>Список задач</h2>
    <input v-model="task" @keyup.enter="addTask" placeholder="Введите задачу">
    <button @click="addTask">Добавить</button>

    <ul>
      <li v-for="(elem, index) in tasksList" :key="index">
        {{ elem }}
        <button @click="removeTask(index)">Удалить</button>
      </li>
    </ul>
  </div>
</template>

<style scoped>
ul {
  list-style: none;
  padding: 0;
}
li {
  display: flex;
  justify-content: space-between;
  padding: 8px;
  border-bottom: 1px solid #ddd;
}
button {
  background: red;
  color: white;
  border: none;
  cursor: pointer;
}
</style>

