from typing import List
import uuid
from fastapi import APIRouter, Depends, HTTPException
from app.helpers.embedding_generate import get_image_embeddings
router = APIRouter()
from pydantic import BaseModel

class ImageLink(BaseModel):
    image_link: str

#################################################################################################
#   search with image only
#################################################################################################
@router.post("/image-embed")
async def submit_form(image: ImageLink):
    # Extract the image link from the request body
    image_link = image.image_link

    # Get the image embeddings using ViT-L-14
    embeddings = get_image_embeddings(image_link)

    return {
        "image_embeddings": embeddings
    }