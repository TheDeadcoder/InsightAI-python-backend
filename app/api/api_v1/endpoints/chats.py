from fastapi import APIRouter, HTTPException

from app.helpers.openai_functions import create_chat_completion
from app.helpers.qdrant_functions import search_in_qdrant_collection_basis, search_in_qdrant_file_basis
from app.schemas.chats import Message, ChatRequestOnFile, ChatRequestOnCollection, ChatResponse
from typing import List

router = APIRouter()

def process_messages(messages: List[Message]) -> tuple[str, str]:
    concatenated_messages = ""
    last_message_text = ""

    for message in messages:
        sender = "assistant" if message.sender == "bot" else "human"
        concatenated_messages += f"sender: {sender}\ntext: {message.text}\n\n"
        last_message_text = message.text

    return concatenated_messages.strip(), last_message_text

@router.post("/on-file", response_model=ChatResponse)
async def answer_from_file(request: ChatRequestOnFile) -> ChatResponse:
    try:

        concatenated_messages, last_message = process_messages(request.messages)
        print(concatenated_messages)
        print(last_message)

        COLLECTION_NAME = f"{request.collection_id}_{request.collection_name}"

        search_results = search_in_qdrant_file_basis(COLLECTION_NAME,last_message,request.limit,request.file_id)
        
        
        result_list = []
        knowledge_basis = ""


        for result in search_results:
            knowledge_basis += f"{result.payload}\n\n"
            result_list.append(result.payload)
        
        
        
        openai_response = create_chat_completion(last_message,concatenated_messages,knowledge_basis,request.template_category)

        content = openai_response
        knowledge = result_list

        return ChatResponse(content=content, knowledge=knowledge)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@router.post("/on-collection", response_model=ChatResponse)
async def answer_from_collection(request: ChatRequestOnCollection) -> ChatResponse:
    try:

        concatenated_messages, last_message = process_messages(request.messages)
        print(concatenated_messages)
        print(last_message)

        COLLECTION_NAME = f"{request.collection_id}_{request.collection_name}"

        search_results = search_in_qdrant_collection_basis(COLLECTION_NAME,last_message,request.limit)
        
        
        result_list = []
        knowledge_basis = ""


        for result in search_results:
            knowledge_basis += f"{result.payload}\n\n"
            result_list.append(result.payload)
        
        
        
        openai_response = create_chat_completion(last_message,concatenated_messages,knowledge_basis,request.template_category)

        content = openai_response
        knowledge = result_list

        return ChatResponse(content=content, knowledge=knowledge)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))