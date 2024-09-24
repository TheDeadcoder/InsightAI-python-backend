# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from datetime import datetime, timedelta
# from typing import List
# from pydantic import BaseModel
# from app.core.supabase import supabase
# from .smtp_mail_send import send_email
# import json

# router = APIRouter()

# class Task(BaseModel):
#     name: str
#     deadline: datetime
#     status: str
#     description: str
#     id: int

# class ProjectWithTasks(BaseModel):
#     id: str
#     name: str
#     tasks: List[Task]

# def get_time_remaining(deadline: datetime) -> str:
#     now = datetime.now()
#     time_diff = deadline - now
#     if time_diff.days > 1:
#         return f"{time_diff.days} days"
#     elif time_diff.days == 1:
#         return "1 day"
#     elif time_diff.seconds // 3600 > 1:
#         return f"{time_diff.seconds // 3600} hours"
#     else:
#         return "less than 1 hour"

# def generate_email_body(user_name: str, projects: List[ProjectWithTasks]) -> str:
#     html_content = f"""
#     <html>
#     <head>
#         <style>
#             body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
#             .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
#             .header {{ background-color: #4A90E2; color: white; padding: 10px; text-align: center; }}
#             .task {{ background-color: #f9f9f9; border-left: 4px solid #4A90E2; margin-bottom: 10px; padding: 10px; }}
#             .footer {{ text-align: center; margin-top: 20px; font-size: 0.8em; color: #888; }}
#         </style>
#     </head>
#     <body>
#         <div class="container">
#             <div class="header">
#                 <img src="https://fgdanyiprenrzvmxnjxw.supabase.co/storage/v1/object/public/statics/insightAI%20main%20logo.png" alt="InsightAI Logo" style="max-width: 150px;">
#                 <h1>Task Reminder</h1>
#             </div>
#             <p>Hello {user_name},</p>
#             <p>We hope this email finds you well. We wanted to remind you about some upcoming tasks that require your attention:</p>
#     """
    
#     for project in projects:
#         html_content += f"<h2>{project.name}</h2>"
#         for task in project.tasks:
#             time_remaining = get_time_remaining(task.deadline)
#             html_content += f"""
#             <div class="task">
#                 <h3>{task.name}</h3>
#                 <p><strong>Deadline:</strong> {task.deadline.strftime('%Y-%m-%d %H:%M')} (in {time_remaining})</p>
#                 <p><strong>Status:</strong> {task.status}</p>
#                 <p><strong>Description:</strong> {task.description}</p>
#             </div>
#             """
    
#     html_content += """
#             <p>We encourage you to review these tasks and take necessary actions. If you need any assistance, please don't hesitate to reach out.</p>
#             <p>Best regards,<br>The InsightAI Team</p>
#             <div class="footer">
#                 <p>© 2024 InsightAI. All rights reserved.</p>
#             </div>
#         </div>
#     </body>
#     </html>
#     """
#     return html_content

# @router.post("/")
# async def send_task_reminders():
#     now = datetime.now()
#     reminder_threshold = now + timedelta(days=3)  # Adjust as needed

#     users = supabase.table("user_table").select("*").execute()
#     users = users.data

#     for user in users:
#         projects = (
#             supabase.table("projects")
#             .select("*")
#             .eq("user_id", user['user_id'])
#             .execute()
#         )
#         projects = projects.data

#         projects_with_pending_tasks = []
#         for project in projects:
#             # Parse the tasks JSON string into a Python list
#             tasks = json.loads(project['tasks'])
#             pending_tasks = [
#                 Task(**task) for task in tasks
#                 if task['status'] == 'Pending' and task['deadline'] and datetime.fromisoformat(task['deadline']) <= reminder_threshold
#             ]
#             if pending_tasks:
#                 projects_with_pending_tasks.append(ProjectWithTasks(
#                     id=project['id'],
#                     name=project['name'],
#                     tasks=pending_tasks
#                 ))

#         if projects_with_pending_tasks:
#             email_body = generate_email_body(user['user_name'], projects_with_pending_tasks)
#             try:
#                 send_email(
#                     to_email=user['email'],
#                     subject="Important: Upcoming Task Reminders",
#                     body=email_body
#                 )
#             except HTTPException as e:
#                 print(f"Failed to send email to {user['email']}: {str(e)}")

#     return {"message": "Task reminders sent successfully"}
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List
from pydantic import BaseModel
from app.core.supabase import supabase
from .smtp_mail_send import send_email
import json

router = APIRouter()

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

def get_time_remaining(deadline: datetime) -> str:
    now = datetime.now()
    time_diff = deadline - now
    if time_diff.days > 1:
        return f"{time_diff.days} days"
    elif time_diff.days == 1:
        return "1 day"
    elif time_diff.seconds // 3600 > 1:
        return f"{time_diff.seconds // 3600} hours"
    else:
        return "less than 1 hour"

# Function to generate HTML email body with support for code snippets
def generate_email_body(user_name: str, projects: List[ProjectWithTasks]) -> str:
    html_content = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #4A90E2; color: white; padding: 10px; text-align: center; }}
            .task {{ background-color: #f9f9f9; border-left: 4px solid #4A90E2; margin-bottom: 10px; padding: 10px; }}
            .footer {{ text-align: center; margin-top: 20px; font-size: 0.8em; color: #888; }}
            pre {{ background-color: #f4f4f4; padding: 10px; border-radius: 5px; }}
            code {{ font-family: 'Courier New', Courier, monospace; font-size: 0.9em; color: #c7254e; background-color: #f9f2f4; padding: 2px 4px; border-radius: 4px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <img src="https://fgdanyiprenrzvmxnjxw.supabase.co/storage/v1/object/public/statics/insightAI%20main%20logo.png" alt="InsightAI Logo" style="max-width: 150px;">
                <h1>Task Reminder</h1>
            </div>
            <p>Hello {user_name},</p>
            <p>We hope this email finds you well. We wanted to remind you about some upcoming tasks that require your attention:</p>
    """
    
    for project in projects:
        html_content += f"<h2>{project.name}</h2>"
        for task in project.tasks:
            time_remaining = get_time_remaining(task.deadline)
            html_content += f"""
            <div class="task">
                <h3>{task.name}</h3>
                <p><strong>Deadline:</strong> {task.deadline.strftime('%Y-%m-%d %H:%M')} (in {time_remaining})</p>
                <p><strong>Status:</strong> {task.status}</p>
                <p><strong>Description:</strong></p>
                <pre>{task.description}</pre>  <!-- Support for code snippets -->
            </div>
            """
    
    html_content += """
            <p>We encourage you to review these tasks and take necessary actions. If you need any assistance, please don't hesitate to reach out.</p>
            <p>Best regards,<br>The InsightAI Team</p>
            <div class="footer">
                <p>© 2024 InsightAI. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content

@router.post("/send_task_reminders")
async def send_task_reminders():
    now = datetime.now()
    reminder_threshold = now + timedelta(days=5)  # Adjust as needed

    users = supabase.table("user_table").select("*").execute()
    users = users.data

    for user in users:
        projects = (
            supabase.table("projects")
            .select("*")
            .eq("user_id", user['user_id'])
            .execute()
        )
        projects = projects.data

        projects_with_pending_tasks = []
        for project in projects:
            # Parse the tasks JSON string into a Python list
            tasks = json.loads(project['tasks'])
            pending_tasks = [
                Task(**task) for task in tasks
                if task['status'] == 'Pending' and task['deadline'] and datetime.fromisoformat(task['deadline']) <= reminder_threshold
            ]
            print(pending_tasks)
            if pending_tasks:
                projects_with_pending_tasks.append(ProjectWithTasks(
                    id=project['id'],
                    name=project['name'],
                    tasks=pending_tasks
                ))

        if projects_with_pending_tasks:
            email_body = generate_email_body(user['user_name'], projects_with_pending_tasks)
            try:
                send_email(
                    to_email=user['email'],
                    subject="Important: Upcoming Task Reminders",
                    body=email_body
                )
            except HTTPException as e:
                print(f"Failed to send email to {user['email']}: {str(e)}")

    return {"message": "Task reminders sent successfully"}
