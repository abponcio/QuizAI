<script setup>
import { ref } from 'vue';
import axios from 'axios';
import Quizzer from './components/Quizzer.vue';

const state = ref('data')
const results = ref('')
const question = ref('')
const submitting = ref(false)

const handleSubmit = async () => {
  submitting.value = true;

  const response = await axios.post('http://localhost:8000/faq', { question: question.value })

  results.value = response.data
  submitting.value = false;
};
</script>

<template>
  <nav>
    <ul>
      <li @click="() => state = 'quiz'">Quiz</li>
      <li @click="() => state = 'data'">Fine Tuned Data</li>
    </ul>
  </nav>
  <template v-if="state === 'quiz'">
    <Quizzer />
  </template>

  <template v-if="state === 'data'">
    <div class="quiz-wrapper">
      <h1>Fine Tuned Data Chatbot</h1>
      <div v-html="results" class="results" />
      <form @submit.prevent="handleSubmit" class="form">
        <div class="form-group-col">
          <label for="quiz-name">Ask anything about Hello Chef:</label>
          <textarea id="quiz-name" name="quiz-name" required v-model="question" placeholder="Ask here"
            :disabled="submitting" />
        </div>
        <button type="submit" :disabled="submitting" class="submit-btn">Submit</button>
      </form>
    </div>
  </template>
</template>

<style scoped>
nav ul {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin: 0;
  padding: 0
}

nav ul li {
  list-style: none;
  cursor: pointer;
  padding: 1rem;
}

nav ul li:hover {
  background-color: #eee;
  color: black;
}

.results {
  white-space: pre-line;
  text-align: left;
  overflow-y: auto;
  max-height: 300px;
  min-height: 300px;
  background-color: #eee;
  border-radius: 0.5rem;
  color: black;
  padding: 1rem;
}

.header {
  display: flex;
  gap: 1rem;
  justify-content: space-between;
  align-items: center;
}

.quiz-wrapper {
  display: grid;
  align-items: center;
  flex-direction: column;
  flex: 1;
  height: 100%;
  gap: 1rem;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  gap: 0.5rem;
}

.form-group-col {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label,
.form-group-col label {
  text-align: left;
}

.form-group input {
  flex: 1;
  padding: 0.5rem;
}

.questions-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group-col textarea {
  flex: 1;
  padding: 0.5rem;
}

.hr {
  width: 100%;
}

.start-test {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 1rem;
}

.correct-answer {
  background-color: aquamarine;
  padding: 0.5rem;
  width: 100%;
  border-radius: 0.5rem;
  margin-top: 0.5rem;
  font-weight: bold;
}

.complete-btn {
  background-color: cornflowerblue;
  color: white;
}

.submit-btn {
  background-color: cornflowerblue;
  color: white;
}
</style>
