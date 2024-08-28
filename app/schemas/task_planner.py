from pydantic import BaseModel, HttpUrl

from typing import Optional, List

class SearchResult(BaseModel):
    title: str
    link: str
    content: Optional[str] = None

class TaskPlannerRequest(BaseModel):
    title: str
    description: str

class Subtask(BaseModel):
    subtask_name: str
    subtask_description: str

class Task(BaseModel):
    tasks: List[Subtask]

class TaskPlan(BaseModel):
    tasks: List[Subtask]
    search_results: List[SearchResult]