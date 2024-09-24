from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.core.supabase import supabase
from fastapi import FastAPI, APIRouter, HTTPException
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
router = APIRouter()
from uuid import UUID
import os



# Pydantic model
class SendEmailRequest(BaseModel):
    user_id: UUID
    subject: str
    body: str


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


@router.post("/send-email")
async def send_email_endpoint(request: SendEmailRequest):
    # Retrieve user email from Supabase
    response = supabase.table("user_table").select("email").eq("user_id", request.user_id).execute()

    if len(response.data) == 0:
        raise HTTPException(status_code=404, detail="User not found")

    user_email = response.data[0]["email"]

    # Send the email
    send_email(user_email, request.subject, request.body)

    return {"message": "Email sent successfully"}
