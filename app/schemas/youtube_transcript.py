from pydantic import BaseModel

# Pydantic model to validate the incoming URL data
class videoIdRequest(BaseModel):
    video_id: str