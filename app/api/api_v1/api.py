from fastapi import APIRouter
from app.api.api_v1.endpoints import product_retrieve, product_search, collection_create, sentiment_analysis

api_router_v1 = APIRouter()

api_router_v1.include_router(product_retrieve.router, prefix="/product_retrieve", tags=["product_retrieve"])
api_router_v1.include_router(product_search.router, prefix="/product_search", tags=["product_search"])
api_router_v1.include_router(collection_create.router, prefix="/collection_create", tags=["collection_create"])
api_router_v1.include_router(sentiment_analysis.router, prefix="/sentiment_analysis", tags=["sentiment_analysis"])
# api_router_v1.include_router(protected.router, prefix="/protected", tags=["protected"])
# api_router_v1.include_router(users.router, prefix="/users", tags=["users"])
# api_router_v1.include_router(files.router, prefix="/files", tags=["files"])
# api_router_v1.include_router(chats.router, prefix="/chats", tags=["chats"])