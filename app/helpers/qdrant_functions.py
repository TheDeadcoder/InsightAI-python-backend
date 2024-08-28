from fastapi import HTTPException
from qdrant_client import models
import uuid
from uuid import UUID
# from app.schemas.files import File

from app.core.qdrant import qdrantClient_File
from app.helpers.embedding_generate import get_text_embedding
from qdrant_client.http.models import VectorParams, Distance

#################################################################################################
#   Helper function to make a collection
#   input: collection name, output: integer
#################################################################################################

def make_collection(user_id: UUID, collection_name: str):
    full_collection_name = f"{user_id}_{collection_name}"
    try:
        qdrantClient_File.get_collection(full_collection_name)
        return "Collection Already exists"
    except Exception as e:
        if "Not found" in str(e):
            qdrantClient_File.create_collection(
                full_collection_name,
                vectors_config={
                    "content": VectorParams(
                        size=3072,
                        distance=Distance.COSINE
                    ),
                },
            )
            rt_str = "Collection named:" + full_collection_name + "has been successfully created"
            return rt_str
        else:
            raise HTTPException(status_code=500, detail="Error occurred making the collection")
        
#################################################################################################
#   Helper function to Delete a collection
#   input: collection name, output: integer
#################################################################################################
def delete_collection(user_id: UUID, collection_name: str):
    full_collection_name = f"{user_id}_{collection_name}"
    try:
        qdrantClient_File.delete_collection(collection_name=full_collection_name)
        return f"Collection {full_collection_name} has been deleted successfully"
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error occurred while deleting the collection")


#################################################################################################
#   Helper function to Return the number of vector points in a particular collection
#   input: collection name, output: integer
#################################################################################################
def vector_point_count(collection_name:str):
    point_count = qdrantClient_File.count(collection_name)
    return point_count.count


#################################################################################################
#   Helper function to upload into qdrant cloud
#   input: modular file, page_no, semantic chunks, summaries and output: nothing
#################################################################################################
def upload_to_qdrant(file_id: str, file_url:str, page_no:str, semantic_chunk:str, summary:str, collection_name:str):

    payload = {
            "file_id": file_id,
            "content": semantic_chunk,
            "file_url": file_url,
            "page_no": page_no
    }

    str_to_embed = summary + semantic_chunk
    content_embedding = get_text_embedding(str_to_embed)
    document_id = str(uuid.uuid4())
    qdrantClient_File.upsert(
            collection_name,
            points=[
                {
                    "id": document_id,
                    "vector": {
                        "content": content_embedding
                    },
                    "payload": payload
                }
            ]
    )

# #################################################################################################
# #   Helper function to Get all the vector-point IDs for a particular UUID of a file
# #   input: UUID of file and output: array of points
# #################################################################################################
# def get_points_by_uuid(collection_name:str, uuid:str):
#     offset = None
#     all_points = []
    
#     while True:
#         result = qdrantClient_File.scroll(
#             collection_name=collection_name,
#             scroll_filter=models.Filter(
#                 must=[
#                     models.FieldCondition(key="file_id", match=models.MatchValue(value=uuid)),
#                 ]
#             ),
#             limit=10,  
#             with_payload=False,
#             with_vectors=False,
#             offset=offset
#         )
        
#         points, next_offset = result
#         all_points.extend(points)
        
#         if next_offset is None:
#             break
        
#         offset = next_offset
    
#     all_point_ids = []
#     all_point_ids.extend([point.id for point in points])
#     return all_point_ids


# #################################################################################################
# #   Helper function to DELETE all the vector-point IDs for a particular UUID of a file
# #   input: UUID and output: array of points
# #################################################################################################
def delete_points_by_uuid(collection_name, uuid):
    try:
        qdrantClient_File.delete(
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
    
# #################################################################################################
# #   Helper function to SEARCH in a collection with given query
# #   input: collection, query and limit and output: array of vector points
# #################################################################################################

# def search_in_qdrant(collection_name, query, limit):
#     try:
#         embedding = create_embedding(query)
#         results = qdrantClient_File.search(
#                 collection_name = collection_name,
#                 query_vector = ("content", embedding),
#                 limit=limit,
#                 with_payload=True,
#                 with_vectors=False,
#             )

#         return results
    
#     except HTTPException as http_exc:
#         raise http_exc
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error occurred while searching in vectorDB {str(e)}")



# file_id: str
#     collection_name: str
#     file_id: str

# #################################################################################################
# #   Helper to return all the points in a particular file
# #################################################################################################
def file_fetch(collection_name:str, collection_id: str, file_id:str):
    offset = None
    all_points = []
    full_collection_name = f"{collection_id}_{collection_name}"
    
    while True:
        result = qdrantClient_File.scroll(
            collection_name=full_collection_name,
            scroll_filter=models.Filter(
                must=[
                    models.FieldCondition(key="file_id", match=models.MatchValue(value=file_id)),
                ]
            ),
            limit=20,  
            with_payload=True,
            with_vectors=False,
            offset=offset
        )
        
        points, next_offset = result
        all_points.extend(points)
        
        if next_offset is None:
            break
        
        offset = next_offset
    
    sorted_points = sorted(all_points, key=lambda point: point.payload.get('page_no', 0))
    
    # Concatenating content with page numbers
    concatenated_content = ""
    for point in sorted_points:
        page_no = point.payload.get('page_no', "Unknown Page")
        content = point.payload.get('content', "")
        concatenated_content += f"Page {page_no}:\n{content}\n\n"
    
    return concatenated_content


def search_in_qdrant_file_basis(collection_name:str, query:str, limit:int, file_id: str):
    try:
        embedding = get_text_embedding(query)

        filter_conditions = {
            "must": [
                {
                    "key": "file_id",
                    "match": {"value": file_id}
                }
            ]
        }

        results = qdrantClient_File.search(
            collection_name=collection_name,
            query_vector=("content", embedding),
            limit=limit,
            with_payload=True,
            with_vectors=False,
            query_filter=filter_conditions  
        )

        return results

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred while searching in vectorDB: {str(e)}")
    
def search_in_qdrant_collection_basis(collection_name:str, query:str, limit:int):
    try:
        embedding = get_text_embedding(query)

        results = qdrantClient_File.search(
            collection_name=collection_name,
            query_vector=("content", embedding),
            limit=limit,
            with_payload=True,
            with_vectors=False
        )

        return results

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred while searching in vectorDB: {str(e)}")