from pydantic import BaseModel
from typing import List

class Product(BaseModel):
    product_id: int
    link: str
    name: str
    description: str
    price: float
    specifications: str
    image_links: List[str]
    gender: str
    category: str
    company: str