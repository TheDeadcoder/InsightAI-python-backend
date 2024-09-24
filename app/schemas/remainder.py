from datetime import datetime, timedelta
from typing import List
from pydantic import BaseModel

class Task(BaseModel):
    name: str
    deadline: datetime
    status: str
    description: str
    id: int

class ProjectWithTasks(BaseModel):
    id: str
    name: str
    tasks: List[Task]