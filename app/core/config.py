from pydantic_settings import BaseSettings
from pydantic import PostgresDsn
import os
from dotenv import load_dotenv

load_dotenv()  
class Settings(BaseSettings):
    SUPABASE_URL: str = os.getenv("SUPABASE_URL")
    SUPABASE_ANON_KEY:str = os.getenv("SUPABASE_ANON_KEY")
    SUPABASE_BUCKET_NAME: str = os.getenv("SUPABASE_BUCKET_NAME")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    QDRANT_HOST_SHOPGENIE: str = os.getenv("QDRANT_HOST_SHOPGENIE")
    QDRANT_API_KEY_SHOPGENIE: str = os.getenv("QDRANT_API_KEY_SHOPGENIE")
    QDRANT_COLLECTION_SHOPGENIE: str = os.getenv("QDRANT_COLLECTION_SHOPGENIE")
    BASE_URL: str = os.getenv("BASE_URL")
    COMPANY_NAME: str = os.getenv("COMPANY_NAME")
    ROBOFLOW_API_KEY: str = os.getenv("ROBOFLOW_API_KEY")
    QDRANT_HOST_FILE: str = os.getenv("QDRANT_HOST_FILE")
    QDRANT_API_KEY_FILE: str = os.getenv("QDRANT_API_KEY_FILE")



settings = Settings()