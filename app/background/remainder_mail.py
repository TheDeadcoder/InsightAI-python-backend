
from datetime import datetime, timedelta
from typing import List

from app.core.supabase import supabase
import json
import markdown2
from fastapi import HTTPException
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from uuid import UUID
import os

from app.schemas.remainder import ProjectWithTasks, Task

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
    
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USERNAME = os.getenv('SMTP_USERNAME')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')

def send_email(to_email: str, subject: str, body: str):
    # Create the email
    msg = MIMEMultipart()
    msg['From'] = SMTP_USERNAME
    msg['To'] = to_email
    msg['Subject'] = subject

    # Change 'plain' to 'html' to send the email as HTML
    msg.attach(MIMEText(body, 'html'))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Secure the connection
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SMTP_USERNAME, to_email, msg.as_string())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")

# Function to generate HTML email body with support for code snippets
def generate_email_body(user_name: str, projects: List[ProjectWithTasks]) -> str:
    html_content = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #e5ffea; color: blue; padding: 10px; text-align: center; }}
            .task {{ background-color: #f9f9f9; border-left: 4px solid #4A90E2; margin-bottom: 10px; padding: 10px; }}
            .footer {{ text-align: center; margin-top: 20px; font-size: 0.8em; color: #888; }}
            pre {{ background-color: #f4f4f4; padding: 10px; border-radius: 5px; font-family: 'Courier New', Courier, monospace; color: #333; white-space: pre-wrap; }}
    code {{ font-family: 'Courier New', Courier, monospace; color: #c7254e; background-color: #f9f2f4; padding: 2px 4px; border-radius: 4px; }}
    
            </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <img src="https://fgdanyiprenrzvmxnjxw.supabase.co/storage/v1/object/public/statics/insightAI%20main%20logo.png" alt="InsightAI Logo" style="max-width: 200px;">
                <h1>Task Reminder</h1>
            </div>
            <p>Hello {user_name},</p>
            <p>We hope this email finds you well. We wanted to remind you about some upcoming tasks that require your attention:</p>
    """
    
    for project in projects:
        html_content += f"<h2>{project.name}</h2>"
        for task in project.tasks:
            time_remaining = get_time_remaining(task.deadline)
            # task_description_html = markdown2.markdown(task.description)
            task_description_html = markdown2.markdown(task.description, extras=["fenced-code-blocks", "code-friendly"])
            html_content += f"""
            <div class="task">
                <h3>{task.name}</h3>
                <p><strong>Deadline:</strong> {task.deadline.strftime('%Y-%m-%d %H:%M')} (in {time_remaining})</p>
                <p><strong>Status:</strong> {task.status}</p>
                <p><strong>Description:</strong></p>
                <pre>{task_description_html}</pre>  <!-- Support for code snippets -->
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

def bg_send_task_reminders():
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