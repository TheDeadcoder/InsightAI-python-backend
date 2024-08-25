from fastapi import FastAPI, HTTPException
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File as FastAPIFile, Form
from bs4 import BeautifulSoup
import requests
from app.schemas.youtube_transcript import videoIdRequest
from app.helpers.openai_functions import clean_content
from app.helpers.youtube.transcript_fetch import get_and_upload_transcript

router = APIRouter()

@router.post("/")
async def get_transcript(request: videoIdRequest):
    video_id = request.video_id

    try:
        ret_content = get_and_upload_transcript(video_id)
        return {"supabase_file_url": ret_content}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Failed to retrieve content: {str(e)}")

