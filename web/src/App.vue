
<script setup>
  import axios from 'axios';
  import { ref } from 'vue';

  const topic = ref(null);
  const question = ref(null);
  const answer = ref(null);
  const submitting = ref(false);
  const submitted = ref(false);

  const questions = ref(null)
  const answers = ref(null)

  const studentAnswers = {}

  const handleAnswer = (value, index) => {
    studentAnswers[index] = value
  }

  const submitTest = () => {
    const score = Object.keys(studentAnswers).reduce((acc, index) => {
      if (studentAnswers[index].toLowerCase() === answers.value[index].charAt(16).toLowerCase()) {
        return acc + 1
      }

      return acc
    }, 0)

    submitted.value = true;

    alert(`Your score is ${score}/${Object.keys(questions.value).length}`)
  }

  const handleSubmit = async () => {
    submitting.value = true;
    const quiz = {
      topic: topic.value.value,
      num_questions: parseInt(question.value.value),
      num_answers: parseInt(answer.value.value),
    };

    const response = await axios.post('http://localhost:8000/quiz', quiz)

    questions.value = response.data.questions
    answers.value = response.data.answers

    submitting.value = false;
  };
</script>

<template>
  <div class="quiz-wrapper">
    <div>
      <h1>Quiz Generator</h1>

      <form @submit.prevent="handleSubmit" class="form">
        <div class="form-group-col">
          <label for="quiz-name">Topic:</label>
          <textarea id="quiz-name" name="quiz-name" required ref="topic" placeholder="Choose any topic to generate" :disabled="submitting"/>
        </div>

        <div class="form-group">
          <label for="quiz-description">Number of Questions:</label>
          <input type="number" max="4" min="1" id="quiz-description" name="quiz-description" ref="question" value="2" :disabled="submitting" />
        </div>

        <div class="form-group">
          <label for="quiz-answers">Number of Answers:</label>
          <input type="number" min="1" max="4" id="quiz-answers" name="quiz-answers" ref="answer" value="2" :disabled="submitting"/>
        </div>

        <input type="submit" value="Submit" :disabled="submitting"/>
      </form>
    </div>
  </div>

  <div class="start-test" v-if="questions">
    <h2>Questions</h2>
    <div v-for="(question, index) in questions" :key="index">
      <div v-html="question" style="white-space: pre-line; text-align: left;"/>
      <div style="text-align: left;">
        Answer:
        <input type="text" @input="(e) => handleAnswer(e.target.value, index)">
      </div>
      <div v-if="submitted" v-html="answers[index]" style="white-space: pre-line; text-align: left;"/>
      <hr/>
    </div>
    <button @click="submitTest">Complete Test</button>
  </div>

</template>

<style scoped>
.quiz-wrapper {
  display: grid;
  align-items: center;
  flex-direction: column;
  flex: 1;
  height: 100%;
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

.form-group-col textarea {
  flex: 1;
  padding: 0.5rem;
}

.start-test {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 1rem;
}
</style>
