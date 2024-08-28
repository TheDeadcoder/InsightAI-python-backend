from fastapi import APIRouter
from app.api.api_v1.endpoints import product_retrieve, product_search, collection_create, sentiment_analysis, url_content,youtube_content, fileprocess,mcq_quiz,flashcard, note_take,chats,task_planner

api_router_v1 = APIRouter()

api_router_v1.include_router(product_retrieve.router, prefix="/product_retrieve", tags=["product_retrieve"])
api_router_v1.include_router(product_search.router, prefix="/product_search", tags=["product_search"])
api_router_v1.include_router(collection_create.router, prefix="/collection-manage", tags=["collection-manage"])
api_router_v1.include_router(sentiment_analysis.router, prefix="/sentiment_analysis", tags=["sentiment_analysis"])
api_router_v1.include_router(url_content.router, prefix="/url-content", tags=["url-content"])
api_router_v1.include_router(youtube_content.router, prefix="/youtube-content", tags=["youtube-content"])
api_router_v1.include_router(fileprocess.router, prefix="/process-file", tags=["process-file"])
api_router_v1.include_router(mcq_quiz.router, prefix="/generate-quiz", tags=["generate-quiz"])
api_router_v1.include_router(flashcard.router, prefix="/flashcard", tags=["flashcard"])
api_router_v1.include_router(note_take.router, prefix="/note_take", tags=["note_take"])
api_router_v1.include_router(chats.router, prefix="/chats", tags=["chats"])
api_router_v1.include_router(task_planner.router, prefix="/task-planner", tags=["task-planner"])