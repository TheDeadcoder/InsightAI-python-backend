from fastapi import APIRouter
from app.api.api_v1.endpoints import product_retrieve

api_router_v1 = APIRouter()

api_router_v1.include_router(product_retrieve.router, prefix="/product_retrieve", tags=["product_retrieve"])
# api_router_v1.include_router(protected.router, prefix="/protected", tags=["protected"])
# api_router_v1.include_router(users.router, prefix="/users", tags=["users"])
# api_router_v1.include_router(files.router, prefix="/files", tags=["files"])
# api_router_v1.include_router(chats.router, prefix="/chats", tags=["chats"])