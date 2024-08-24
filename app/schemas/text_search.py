from pydantic import BaseModel
from typing import List, Optional
from .product import ProductSchema

class ProductQuerySchema(BaseModel):
    query: str

class ProductListResponse(BaseModel):
    products: List[ProductSchema]