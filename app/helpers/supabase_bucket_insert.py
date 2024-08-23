from fastapi import HTTPException
from app.core.supabase import supabase
from app.core.config import settings
from datetime import datetime

bucket_name = settings.SUPABASE_BUCKET_NAME
def upload_file_to_supabase(file: bytes, filename: str, user_id: str) -> str:
    try:
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        unique_filename = f"{user_id}_{current_time}_{filename}"

        supabase.storage.from_(bucket_name).upload(
            file=file,
            path=unique_filename,
            file_options={
                "content-type": "application/pdf"
            }
        )
        # Construct the public URL
        public_url = supabase.storage.from_(bucket_name).get_public_url(unique_filename)
        public_url = public_url.rstrip('?')

        return public_url

    except Exception as e:
        raise Exception(f"Error uploading file to Supabase: {str(e)}")
    
def delete_file_from_supabase(file_path: str) -> bool:
    try:
        print("file Path is", file_path)
        supabase.storage.from_(bucket_name).remove(file_path)
        return True
    except Exception as e:
        print(f"Error deleting file from Supabase: {str(e)}")
        return False