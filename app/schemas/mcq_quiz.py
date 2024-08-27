from pydantic import BaseModel, conlist, field_validator, Field
from typing import Optional, List

class QuizRequest(BaseModel):
    topic_name: str
    difficulty_level: str
    collection_id: str
    collection_name: str
    file_id: str
    number_of_questions: int
    question_type: str

class Question(BaseModel):
    question: str
    options: List[str]
    correctAnswer: int
    explanation: str


class QuizResponse(BaseModel):
    questions: List[Question]