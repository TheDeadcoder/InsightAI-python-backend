import qdrant_client
from qdrant_client import QdrantClient
from app.core.config import settings

qdrantClient_ShopGenie = qdrant_client.QdrantClient(settings.QDRANT_HOST_SHOPGENIE, api_key = settings.QDRANT_API_KEY_SHOPGENIE)
qdrantClient_File = qdrant_client.QdrantClient(settings.QDRANT_HOST_FILE, api_key = settings.QDRANT_API_KEY_FILE)