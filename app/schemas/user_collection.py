from pydantic import BaseModel
from uuid import UUID


class collectionSchema(BaseModel):
    user_id: UUID
    collection_name: str