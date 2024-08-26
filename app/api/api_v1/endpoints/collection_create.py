from fastapi import APIRouter, Depends, HTTPException
router = APIRouter()

from app.schemas.user_collection import collectionSchema
from app.helpers.qdrant_functions import make_collection, delete_collection


@router.post("/create_collection")
async def create_collection(collection: collectionSchema):
    result = make_collection(collection.user_id, collection.collection_name)
    return {"message": result}

@router.post("/delete_collection")
async def create_collection(collection: collectionSchema):
    result = delete_collection(collection.user_id, collection.collection_name)
    return {"message": result}
