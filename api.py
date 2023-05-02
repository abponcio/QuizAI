import os

from dotenv import load_dotenv
from ai import AI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

load_dotenv()

class Quiz(BaseModel):
    topic: str
    num_questions: int
    num_answers: int

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

myAI = AI(os.getenv("OPENAI_API_KEY"))

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/quiz")
def create_quiz(data: Quiz):
    quiz_results = myAI.create_test_prompt(data.topic, data.num_questions, data.num_answers)
    questions = quiz_results["questions"]
    correct_answers = quiz_results["answers"]
    return {"questions": questions, "answers": correct_answers}