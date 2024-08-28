from pydantic import BaseModel, conlist, field_validator, Field
from typing import Optional, List

class flashcardRequest(BaseModel):
    topic_name: str
    difficulty_level: str
    collection_id: str
    collection_name: str
    file_id: str
    number_of_questions: int
    question_type: str

class Step(BaseModel):
    step_name: str
    step_solution: str


class Question_without_step(BaseModel):
    question: str
    answer: str
    tips_and_tricks: str

class Question_with_step(BaseModel):
    question: str
    answer: List[Step]
    tips_and_tricks: str
    conclusion: str


class QuizResponse_stepped(BaseModel):
    questions: List[Question_with_step]

class QuizResponse_non_stepped(BaseModel):
    questions: List[Question_without_step]