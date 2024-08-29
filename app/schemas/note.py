from pydantic import BaseModel, conlist, field_validator, Field
from typing import Optional, List
from .YouTubeVideo import YouTubeVideo

class Note_Request(BaseModel):
    topic_name: str
    collection_id: str
    collection_name: str
    file_id: str
    knowledge_level: str

class Slide(BaseModel):
    slide_name: str
    slide_content: str

class Question(BaseModel):
    question: str
    answer: str


class Note(BaseModel):
    introduction_and_motivation: str
    slides: List[Slide]
    questions: List[Question]
    conclusion: str


class Note_Response(BaseModel):
    note: Note
    videos: List[YouTubeVideo]

class search_prompt(BaseModel):
    prompt: str
