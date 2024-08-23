from fastapi import HTTPException
from qdrant_client import models

from app.schemas.files import File

from app.core.qdrant import qdrantClient
from app.helpers.embedding_generate import create_embedding
from qdrant_client.http.models import VectorParams, Distance

#################################################################################################
#   Helper function to make a collection
#   input: collection name, output: integer
#################################################################################################
def make_collection(collection_name:str):
    try:
        qdrantClient.get_collection(collection_name)
        return "Collection Already exists"
    except Exception as e:
        if "Not found" in str(e):
            qdrantClient.create_collection(
                collection_name,
                vectors_config={
                    "content": VectorParams(
                        size=3072,
                        distance=Distance.COSINE
                    ),
                },
            )
            rt_str = "Collection named:" + collection_name + "has been successfully created"
            return rt_str
        else:
            raise HTTPException(status_code=500, detail="Error occurred making the collection")


#################################################################################################
#   Helper function to Return the number of vector points in a particular collection
#   input: collection name, output: integer
#################################################################################################
def vector_point_count(collection_name:str):
    point_count = qdrantClient.count(collection_name)
    return point_count.count


#################################################################################################
#   Helper function to upload into qdrant cloud
#   input: modular file, page_no, semantic chunks, summaries and output: nothing
#################################################################################################
def upload_to_qdrant(file_id: str, file_url:str, file_name:str, page_no:str, semantic_chunks, summaries, collection_name:str):
    index = vector_point_count(collection_name)
    summary_index = 0

    for semantic_chunk in semantic_chunks:
        # Create payload from File object fields
        payload = {
            "file_id": file_id,
            "content": semantic_chunk.page_content,
            "file_url": file_url,
            "file_name": file_name,
            "page_no": page_no
        }

        str_to_embed = summaries[summary_index] + "\n" + semantic_chunk.page_content
        content_embedding = create_embedding(str_to_embed)

        qdrantClient.upsert(
            collection_name,
            points=[
                {
                    "id": index,
                    "vector": {
                        "content": content_embedding
                    },
                    "payload": payload
                }
            ]
        )
        index += 1
        summary_index += 1

#################################################################################################
#   Helper function to Get all the vector-point IDs for a particular UUID of a file
#   input: UUID of file and output: array of points
#################################################################################################
def get_points_by_uuid(collection_name:str, uuid:str):
    offset = None
    all_points = []
    
    while True:
        result = qdrantClient.scroll(
            collection_name=collection_name,
            scroll_filter=models.Filter(
                must=[
                    models.FieldCondition(key="file_id", match=models.MatchValue(value=uuid)),
                ]
            ),
            limit=10,  
            with_payload=False,
            with_vectors=False,
            offset=offset
        )
        
        points, next_offset = result
        all_points.extend(points)
        
        if next_offset is None:
            break
        
        offset = next_offset
    
    all_point_ids = []
    all_point_ids.extend([point.id for point in points])
    return all_point_ids


#################################################################################################
#   Helper function to DELETE all the vector-point IDs for a particular UUID of a file
#   input: UUID and output: array of points
#################################################################################################
def delete_points_by_uuid(collection_name, uuid):
    try:
        qdrantClient.delete(
            collection_name=collection_name,
            points_selector=models.FilterSelector(
                filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="file_id",
                            match=models.MatchValue(value=uuid),
                        ),
                    ],
                )
            ),
        )

        return True
  
    except Exception as e:
         raise HTTPException(status_code=500, detail="Error occurred while deleting from vectorDB")
    
#################################################################################################
#   Helper function to SEARCH in a collection with given query
#   input: collection, query and limit and output: array of vector points
#################################################################################################

def search_in_qdrant(collection_name, query, limit):
    try:
        embedding = create_embedding(query)
        results = qdrantClient.search(
                collection_name = collection_name,
                query_vector = ("content", embedding),
                limit=limit,
                with_payload=True,
                with_vectors=False,
            )

        return results
    
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred while searching in vectorDB {str(e)}")