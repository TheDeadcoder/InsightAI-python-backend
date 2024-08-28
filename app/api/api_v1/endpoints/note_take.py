from fastapi import APIRouter, HTTPException

from app.helpers.note.note import generate_note_helper
from app.schemas.note import Note_Request, Note, Note_Response
from app.helpers.qdrant_functions import file_fetch

router = APIRouter()

@router.post("/", response_model=Note_Response)
async def generate_note(request: Note_Request):
    knowledge_base = file_fetch(str(request.collection_name), str(request.collection_id), str(request.file_id))
    print(knowledge_base)

    note_response = generate_note_helper(request.topic_name,request.knowledge_level,knowledge_base)
    return note_response