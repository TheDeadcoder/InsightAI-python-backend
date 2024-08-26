from typing import List
import uuid
from fastapi import APIRouter, Depends, HTTPException
from app.helpers.product_retrieve.multiple_product import retrieve_multiple_products_from_qdrant
from app.schemas.product import ProductSchema, CategoryRequestSchema, CategoryResponseSchema, ProductRetrieveResponseSchema, ProductRetrieveMultipleRequestSchema, ProductRetrieveMultipleResponseSchema
from app.helpers.product_retrieve.single_product import retrieve_single_product_from_qdrant, retrieve_similar_products
from app.helpers.product_retrieve.category import get_products_by_category
router = APIRouter()

CATEGORY_MAPPING = {
    "men": {
        "Coaty-Fatua": ["men coaty", "men short-kurta", "men fatua"],
        "Footwear": [
            "men boots", "men canvas", "men footwear", "men casual-shoes", "men formal-shoes", "men sports-sandals", "men sports-shoes"
        ],
        "casual pant": ['men shorts', 'men track pants & joggers', 'men trousers'],
        "formal pant": ['men jeans'],
        "new arrivals": ['men new-arrivals'],
        "panjabi": ['men panjabi-pajama-sets', 'men panjabi'],
        "shirts":  ['men shirts', 'men casual shirts', 'men formal shirts'],
        "suit": ['men blazers', 'men suits'],
        "t-shirts": ['men t-shirts', 'men polos', 'men formal shirts'],
        "wallets": ['men wallets']
    },
    "women": {
        "saree": ["women saree"],
        "Bags": ['women bags'],
        "Western": ['women dresses', 'women nightwear'],
        "casual": ['women shalwar-kameez', 'women scarves', 'women skirts'],
        "daily life": ['women jumpsuits', 'women leggings & jeggings', 'women tops', 'women tunics'],
        "footwear": ['women canvas', 'women heels', 'women footwear'],
        "new arrivals": ['women new-arrivals'],
        "panjabi-kurta": ['women kurta', 'women panjabi'],
        "winter wear": ['women winterwear', 'women shawls']
    },
    "boy": {
        "Western": ['boys suits & blazers'],
        "daily-life": ['boys track pants', 'boys fatua', 'boys pajama', 'boys trousers'],
        "formal": ['boys shirts', 'boys shirt-pant-sets'],
        "panjabi": ['boys panjabi-pajama-sets', 'boys panjabi'],
        "pant": ['boys pants', 'boys jeans', 'boys shorts'],
        "t-shirt": ['boys t-shirts-polos', 'boys polo t-shirts', 'boys round neck & v neck t-shirts'],
        "winter-wear": ['boys jackets', 'boys sweatshirts', 'boys gloves', 'boys masks']
    },
    "girl": {
        "Special": ['girls ghagra-choli', 'girls shalwar-kameez'],
        "casual": ['girls tops', 'girls skirts', 'girls tops & t-shirts'],
        "daily life": ['girls frocks', 'girls dungarees', 'girls frocks & dresses', 'girls leggings & jeggings'],
        "winter-wear": ['girls sweaters', 'girls shawls', 'girls sweaters-jackets']
    }
}

#################################################################################################
#   GET a particular product
#################################################################################################
@router.get("/{product_id}", response_model=ProductRetrieveResponseSchema)
async def get_product_by_id(product_id: uuid.UUID) -> ProductRetrieveResponseSchema:
    product = await retrieve_single_product_from_qdrant(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    similar_products = await retrieve_similar_products(product_id)
    
    return ProductRetrieveResponseSchema(
        product=ProductSchema(**product),
        similar_products=[ProductSchema(**p) for p in similar_products]
    )

#################################################################################################
#   GET a category-based product
#################################################################################################
@router.post("/category", response_model=CategoryResponseSchema)
async def get_category_products(request: CategoryRequestSchema):
    category = request.category
    sub_category = request.sub_category

    granular_categories = CATEGORY_MAPPING.get(category, {}).get(sub_category)
    
    if not granular_categories:
        raise HTTPException(status_code=404, detail="Invalid category or sub-category")
    
    # Fetch products using the helper function
    products_data = await get_products_by_category(
        category=category,
        granular_categories=granular_categories,
        limit=request.limit,
        offset=request.offset
    )
    
    if not products_data["products"]:
        raise HTTPException(status_code=404, detail="No products found")
    
    return CategoryResponseSchema(
        products=products_data["products"],
        next_offset=products_data["next_offset"]
    )


#################################################################################################
#   GET a List of products
#################################################################################################
@router.post("/retrieve-multiple", response_model=ProductRetrieveMultipleResponseSchema)
async def get_multiple_products_by_ids(request: ProductRetrieveMultipleRequestSchema) -> ProductRetrieveMultipleResponseSchema:
    product_ids = request.product_ids
    products = await retrieve_multiple_products_from_qdrant(product_ids)
    
    if not products:
        raise HTTPException(status_code=404, detail="No products found")
    
    return ProductRetrieveMultipleResponseSchema(
        products=[ProductSchema(**product) for product in products]
    )