import openai

class AI():
    def __init__(self, api_key):
        openai.api_key = api_key

    def create_test_prompt(self, topic, num_questions, num_possible_answers):
        print(topic, num_questions, num_possible_answers)
        prompt = f"Create a multiple choice quiz on the topic about {topic}. "
        prompt += f"with {num_questions} questions that starts with 'Q#: ' that is based on a fact and not opinionated. "
        prompt += f"Each question should have {num_possible_answers} possible answers starts with capital letter bullet points with this format 'A. '. "
        prompt += f"Also include the correct answer for each question with a starting string of 'Correct Answer: '"

        response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=256, temperature=0.7)

        student_questions = self.create_student_view(response['choices'][0]['text'], num_questions)
        answer_questions = self.create_answers_view(response['choices'][0]['text'], num_questions)

        return {"questions": student_questions, "answers": answer_questions}

    def create_student_view(self, quiz, num_questions):
        student_view = {1: ''}
        question_number = 1

        for line in quiz.split('\n'):
          if not line.startswith('Correct Answer:'):
              student_view[question_number] += line + '\n'
          else:
              if question_number < num_questions:
                  question_number += 1
                  student_view[question_number] = ''

        return student_view

    def create_answers_view(self, quiz, num_questions):
      answer_view = {1: ''}
      question_number = 1

      for line in quiz.split('\n'):
        if line.startswith('Correct Answer:'):
            answer_view[question_number] += line + '\n'
            if question_number < num_questions:
                question_number += 1
                answer_view[question_number] = ''

      return answer_view
