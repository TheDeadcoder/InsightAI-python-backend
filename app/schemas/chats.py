from pydantic import BaseModel
from typing import List, Dict, Optional, Literal

class Message(BaseModel):
    text: str
    sender: str

TemplateCategory = Literal[
    "Storyteller",
    "General",
    "Summarizer",
    "Analyzer",
    "Teacher",
    "Researcher",
    "Creative Writer",
    "Code Assistant",
    "Translator",
    "Interviewer"
]

class ChatRequestOnCollection(BaseModel):
    collection_id: str
    collection_name: str
    messages: List[Message]
    limit: int
    template_category: TemplateCategory

class ChatRequestOnFile(BaseModel):
    collection_id: str
    collection_name: str
    file_id: str
    messages: List[Message]
    limit: int
    template_category: TemplateCategory

class ChatResponse(BaseModel):
    content: str
    knowledge: Optional[List[Dict]] = None
