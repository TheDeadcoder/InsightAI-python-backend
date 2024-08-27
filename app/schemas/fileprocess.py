# app/schemas.py
from pydantic import BaseModel, HttpUrl

class FileProcessRequest(BaseModel):
    file_url: HttpUrl
    file_id: str
    user_id: str
    collection_name: str
