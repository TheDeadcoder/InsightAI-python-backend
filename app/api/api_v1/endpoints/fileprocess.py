from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.schemas.fileprocess import FileProcessRequest
from app.background.pdf_parse import process_pdf_and_generate_summaries

router = APIRouter()

@router.post("/")
async def process_file(request: FileProcessRequest, background_tasks: BackgroundTasks):
    try:
        background_tasks.add_task(process_pdf_and_generate_summaries, request.file_url, request.file_id, request.user_id, request.collection_name)
        return {
            "message": "File processing initiated. The summary will be saved locally when done.",
            "file_id": request.file_id,
            "user_id": request.user_id,
            "collection_name": request.collection_name
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error while initiating file processing: {str(e)}")
