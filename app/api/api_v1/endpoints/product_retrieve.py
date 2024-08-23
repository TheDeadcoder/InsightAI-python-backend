from typing import List
import uuid
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.product import Product
from app.helpers.product_retrieve.single_product import retrieve_single_product_from_qdrant
router = APIRouter()

#################################################################################################
#   GET a particular product
#################################################################################################
@router.get("/{product_id}", response_model=Product)
async def get_product_by_id(product_id: uuid.UUID) -> Product:
    product = await retrieve_single_product_from_qdrant(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return Product(**product)