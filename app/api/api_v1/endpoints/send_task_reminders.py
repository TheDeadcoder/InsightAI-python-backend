from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from datetime import datetime, timedelta
from typing import List
from pydantic import BaseModel
from app.background.remainder_mail import bg_send_task_reminders
from app.core.supabase import supabase
from .smtp_mail_send import send_email
import json
import markdown2 

router = APIRouter()



@router.get("/")
async def send_task_reminders( background_tasks: BackgroundTasks):
    
    background_tasks.add_task(bg_send_task_reminders)
    return {"message": "Task reminders sent successfully"}
