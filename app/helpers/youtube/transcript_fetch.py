from youtube_transcript_api import YouTubeTranscriptApi
from datetime import datetime
import os
from app.core.supabase import supabase
import logging

logging.basicConfig(level=logging.INFO)

bucket_name = "transcripts"


def generate_transcript_text(transcript, file_name):
    with open(file_name, "w") as file:
        for entry in transcript:
            file.write(f"{entry['text']}\n")


def upload_to_supabase(file_path, bucket_name):


    with open(file_path, "rb") as file:
        data = file.read()

    response = supabase.storage.from_(bucket_name).upload(
        path=file_path,
        file=data,
    )

    public_url = supabase.storage.from_(bucket_name).get_public_url(file_path)
    clean_url = public_url.rstrip('?')
    return clean_url
    return public_url


def get_and_upload_transcript(video_id: str):
    try:
        logging.info(f"Attempting to get transcript for video ID: {video_id}")
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        logging.info("Transcript successfully retrieved")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"transcript_{timestamp}.txt"

        generate_transcript_text(transcript, file_name)

        file_url = upload_to_supabase(file_name, bucket_name)

        if os.path.exists(file_name):
            os.remove(file_name)

        return file_url

    except Exception as e:
        raise Exception(f"Error while getting transcript: {str(e)}")