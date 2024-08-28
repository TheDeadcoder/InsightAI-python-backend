from fastapi import APIRouter, HTTPException
from app.helpers.task_planner.openai_response import project_planning
from app.helpers.task_planner.search_relevant import fetch_top_results
from app.schemas.task_planner import TaskPlannerRequest, TaskPlan
from typing import List


router = APIRouter()

@router.post("/", response_model=TaskPlan)
async def process_file(request: TaskPlannerRequest):
    results = fetch_top_results(request.title)
    if not results:
        raise HTTPException(status_code=404, detail="No relevant search results found.")

    task_plan = project_planning(request.title, request.description, results)

    return task_plan
