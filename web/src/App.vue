
<script setup>
  import axios from 'axios';
  import { onMounted, ref } from 'vue';

  const topic = ref('');
  const question = ref(4);
  const answer = ref(4);
  const submitting = ref(false);
  const submitted = ref(false);
  const results = ref(null);

  const questions = ref(null)
  const answers = ref(null)

  const studentAnswers = {}

  const finalScore = ref(0)

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

    finalScore.value = score
    submitted.value = true;

    results.value.showModal()
  }

  const handleSubmit = async () => {
    submitting.value = true;
    submitted.value = false;
    questions.value = null;
    answers.value = null;

    const quiz = {
      topic: topic.value,
      num_questions: parseInt(question.value),
      num_answers: parseInt(answer.value),
    };

    const response = await axios.post('http://localhost:8000/quiz', quiz)

    questions.value = response.data.questions
    answers.value = response.data.answers

    submitting.value = false;
  };

  const handleRegenerate = () => {
    questions.value = null;
    answers.value = null;
    submitted.value = false;
    topic.value = '';
    question.value = 4;
    answer.value = 4;
  }

  const tryAgain = async () => {
    await handleSubmit()
  }
</script>

<template>
  <h1>Quiz Generator</h1>
  <div class="quiz-wrapper" v-if="!questions">
      <form @submit.prevent="handleSubmit" class="form">
        <div class="form-group-col">
          <label for="quiz-name">Topic:</label>
          <textarea id="quiz-name" name="quiz-name" required v-model="topic" placeholder="Choose any topic to generate" :disabled="submitting"/>
        </div>

        <div class="form-group">
          <label for="quiz-description">Number of Questions:</label>
          <input type="number" max="4" min="1" id="quiz-description" name="quiz-description" v-model.number="question" :disabled="submitting" />
        </div>

        <div class="form-group">
          <label for="quiz-answers">Number of Answers:</label>
          <input type="number" min="1" max="4" id="quiz-answers" name="quiz-answers" v-model.number="answer" :disabled="submitting"/>
        </div>

        <button type="submit" :disabled="submitting" class="submit-btn">Submit</button>
      </form>

  </div>

  <div class="start-test" v-if="questions">
    <div class="header">
      <h2>Questions</h2>
      <div class="actions">
        <a href="#" @click.prevent="tryAgain">Try again</a>&nbsp;  |  &nbsp;<a href="#" @click.prevent="handleRegenerate">Generate a new one</a>
      </div>
    </div>
    <h3>Topic: {{ topic }}</h3>
    <div v-for="(question, index) in questions" :key="index" class="questions-list">
      <div v-html="question" style="white-space: pre-line; text-align: left;"/>
      <div style="text-align: left;">
        Answer:
        <input type="text" @input="(e) => handleAnswer(e.target.value, index)" :disabled="submitting">
      </div>
      <div v-if="submitted" v-html="answers[index]" style="white-space: pre-line; text-align: left;" class="correct-answer"/>
      <hr class="hr"/>
    </div>
    <button @click="submitTest" class="complete-btn">Complete Test</button>
  </div>

  <dialog ref="results">
    <h2 v-if="((finalScore / answer) * 100) >= 50">You Passed!</h2>
    <h2 v-else>You Failed!</h2>
    <p>Final Score: {{ finalScore }} / {{ answer }}</p>

    <form method="dialog">
      <button>OK</button>
    </form>
  </dialog>

</template>

<style scoped>
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
