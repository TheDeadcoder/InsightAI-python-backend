from app.core.openai import openaiClient
from app.schemas.task_planner import Task, SearchResult, TaskPlan

def project_planning(project_name: str, project_description: str, web_content: list[SearchResult]) -> TaskPlan:
    system_prompt = f"""
    You are a task planning assistant. You will receive a project title, description, and relevant web search content. 
    Your job is to create a detailed task plan including subtasks based on this information.
    You will be penalized for irrelevant content.
    The Output format: 
    - Task: <A list of Subtasks>
    - Subtask:
            - subtask_name: <Name of the Sub-task>
            - subtask_description: <Detailed description of the subtask including preparation, procedure, requirements etc>
    """
    
    content_md = "\n\n".join([f"### {result.title}\n{result.content}" for result in web_content])
    
    human_prompt = f"""
    Project Title: {project_name}
    Project Description: {project_description}
    Knowledge Base: The following content is the source material in markdown format:
    {content_md}
    """

    completion = openaiClient.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": human_prompt},
        ],
        response_format=Task,
    )

    tasks = completion.choices[0].message.parsed
    task_plan = TaskPlan(tasks=tasks.tasks, search_results=web_content)

    return task_plan
