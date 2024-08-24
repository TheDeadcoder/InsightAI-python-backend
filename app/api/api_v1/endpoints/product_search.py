from typing import List
import uuid
from fastapi import APIRouter, Depends, HTTPException
from app.helpers.embedding_generate import get_image_embeddings
from app.helpers.product_fetch.text import get_search_products_from_text
router = APIRouter()
from pydantic import BaseModel
from app.schemas.text_search import ProductQuerySchema, ProductListResponse
from app.schemas.text_search import ProductSchema
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


#################################################################################################
#   search with Text only
#################################################################################################

@router.post("/text-search", response_model=ProductListResponse)
async def search_products(query: ProductQuerySchema):
    products = get_search_products_from_text(query.query)
    return ProductListResponse(products=products)