from fastapi import FastAPI, APIRouter, HTTPException
import httpx
import mimetypes

from app.background.pdf_parse import process_pdf_and_generate_summaries, process_txt_and_generate_summaries
from app.core.supabase import supabase

router = APIRouter()

@router.get("/print-file-names-and-types")
def print_file_names_and_types():
    # Step 1: Query the database for rows with status = 'pending'
    response = supabase.table("files").select("*").eq("status", "Pending").execute()
    pending_files = response.data

    if not pending_files:
        return {"message": "No pending files found."}

    for file_info in pending_files:
        file_url = file_info['url']
        file_id = file_info['id']
        user_id = file_info['collection_id']
        collection_name = file_info['collection_name']


        with httpx.Client(timeout=60.0) as client:
            download_response = client.get(file_url)
        
        if download_response.status_code == 200:
            file_type = mimetypes.guess_extension(download_response.headers.get('Content-Type'))
            if file_type:
                if file_type == ".txt":
                    process_txt_and_generate_summaries(file_url, file_id, user_id, collection_name)
                elif file_type == ".pdf":
                    process_pdf_and_generate_summaries(file_url, file_id, user_id, collection_name)
            else:
                print(f"Unsupported file type: {file_type} for file ID: {file_id}")

    return {"message": "Pending files processed successfully."}
