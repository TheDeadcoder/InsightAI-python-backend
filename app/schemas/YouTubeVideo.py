from pydantic import BaseModel, HttpUrl
from typing import Optional

class YouTubeVideo(BaseModel):
    title: Optional[str]
    link: Optional[HttpUrl]
    imageUrl: Optional[HttpUrl]
    duration: Optional[str]
    source: Optional[str]
    date: Optional[str]
