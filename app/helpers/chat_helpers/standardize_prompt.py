from app.core.openai import openaiClient
from app.helpers.qdrant_functions import search_in_qdrant
from fastapi import  HTTPException
from app.core.config import settings

def standardize_prompt_for_RAG(conversation_history):
    
    prompt = f"{conversation_history}\n"
    
    try:
        response = openaiClient.chat.completions.create(
            model="gpt-4o-2024-08-06",
            messages=[
                {
                    "role": "system", 
                    "content": 
                    f"""
                    You are a agent who helps people get banking information.
                    You represent the bank {settings.BANK_NAME} in Bangladesh
                    Your name is 'BankGPT'. You were created by 'BUET Incubator'.
                    You have access to a vector database that has knowledge all about {settings.BANK_NAME} bank's information.
                    You will be given an entire conversation history. You need to standardize the user prompt to properly search into the vector database.
                    You MUST return only the standardized prompt and nothing else
                    """
                    },
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=200
        )
        return response.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating chat completion: {str(e)}")