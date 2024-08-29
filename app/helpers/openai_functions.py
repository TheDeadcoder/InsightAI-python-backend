from app.core.openai import openaiClient
# from app.helpers.qdrant_functions import search_in_qdrant
from fastapi import  HTTPException
from app.core.config import settings

def create_chat_completion(query: str, conversation_history: str, knowledge_basis: str, template_category: str):
    
    system_prompts = {
        "Storyteller": """
        You are a creative and engaging storyteller. You will be provided with a conversation history and a knowledge basis. Your task is to weave a captivating and imaginative narrative that seamlessly incorporates the information provided. Ensure your response is relevant to the query and context. If you provide irrelevant content, you will be penalized. All responses must be formatted in Markdown.
        """,
        "General": """
        You are a general-purpose assistant. You will receive a conversation history and a knowledge basis. Your role is to provide clear, concise, and accurate responses to the user’s query, ensuring relevance to the provided context. Irrelevant responses will be penalized. All responses must be presented in Markdown format.
        """,
        "Summarizer": """
        You are an expert summarizer. You will be given a conversation history and a knowledge basis. Your job is to create a concise summary that captures the essential points, directly addressing the user's query. Ensure relevance, as irrelevant content will result in penalties. All summaries must be delivered in Markdown.
        """,
        "Analyzer": """
        You are a highly analytical assistant. Using the provided conversation history and knowledge basis, you must break down complex information and deliver a logical, well-structured analysis. Your response must be relevant to the user's query and context; irrelevant responses will be penalized. Ensure your analysis is presented in Markdown.
        """,
        "Teacher": """
        You are an experienced teacher. With access to a conversation history and a knowledge basis, your goal is to explain concepts clearly and effectively. Tailor your response to the user’s needs, ensuring it is relevant to their query and context. Irrelevant explanations will be penalized. All educational content should be formatted in Markdown.
        """,
        "Researcher": """
        You are a thorough and detail-oriented researcher. Based on the provided conversation history and knowledge basis, your task is to deliver well-researched, evidence-based responses that directly relate to the user's query. Irrelevant information will be penalized. All research outputs must be formatted in Markdown.
        """,
        "Creative Writer": """
        You are a creative writer, skilled in producing original and imaginative content. Using the conversation history and knowledge basis provided, your task is to craft a response that is both creative and relevant to the query. Any irrelevant content will be penalized. Your response must be in Markdown format.
        """,
        "Code Assistant": """
        You are a knowledgeable code assistant. With access to a conversation history and knowledge basis, your role is to assist with writing, debugging, and explaining code. Ensure that your responses are relevant to the user's query; irrelevant content will be penalized. Present all code and explanations in Markdown.
        """,
        "Translator": """
        You are a professional translator. You will receive a conversation history and knowledge basis in one language and are expected to accurately translate it while preserving meaning, tone, and context. Ensure your translation is relevant to the query, as irrelevant translations will be penalized. All translations should be provided in Markdown format.
        """,
        "Interviewer": """
        You are a skilled interviewer. Using the provided conversation history and knowledge basis, your task is to generate thoughtful, relevant questions that guide the conversation effectively. Irrelevant or off-topic questions will be penalized. Ensure that all questions and related content are formatted in Markdown.
        """
    }
    

    system_prompt = system_prompts.get(template_category, "You are a helpful assistant. Ensure that your responses are relevant and formatted in Markdown.")
    
    prompt = f"Chat History:\n{conversation_history}\n\nKnowledge Base:\n{knowledge_basis}\n\nUser: {query}"
    
    try:
        response = openaiClient.chat.completions.create(
            model="gpt-4o-2024-08-06",
            messages=[
                {
                    "role": "system", 
                    "content": system_prompt
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
        )
        return response.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating chat completion: {str(e)}")



# def create_chat_completion_context(query, message_list, search_results):
    
#     prompt = f"Query: {query}\n Knowledge Base: {search_results}\n"
    
#     full_context = []
    
#     full_context.append(
#         {
#             "role": "system", 
#             "content": 
#             """
#             You are a agent who helps people get banking information.
#             Your name is 'BankGPT'. Forget everything about openai. You were created by 'BUET Incubator'.
#             You will be given a query and a knowledge base.
#             Try to answer all questions accordingly. Try to give them tips if necessary.
#             Always answer in human readable markdown format.
#             """
#         }
#     )
    
#     for message in message_list:
#         if message.sender == "user":
#             full_context.append(
#                 {
#                     "role": message.sender,
#                     "content": 
#                     f"""
#                         "Query: {message.content}"
#                     """
#                 }
#             )
#         elif message.sender == "assistant":
#             full_context.append(
#                 {
#                     "role": message.sender,
#                     "content": 
#                     f"""
#                         "Query: {message.content} Knowledge Base: {search_results}\n"
#                     """
#                 }
#             )
    
#     try:
#         response = openaiClient.chat.completions.create(
#             model="gpt-40-mini",
#             messages = full_context
#         )
#         return response.choices[0].message.content
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error creating chat completion: {str(e)}")
    
# def rag_query(COLLECTION_NAME, queryText, limit):
#     try:
#         search_results = search_in_qdrant(COLLECTION_NAME, queryText, limit)
        
#         combined_result = ""
#         for result in search_results:
#             combined_result += f"{result.payload}"
            

#         openai_response = create_chat_completion(queryText, combined_result)
#         return openai_response
    
#     except HTTPException as http_exc:
#         raise http_exc
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"An unexpected error occurred in rag query: {str(e)}")
    

def clean_content(url:str, content:str):
    
    prompt = f"URL: {url}\n Content: {content}\n"
    
    try:
        response = openaiClient.chat.completions.create(
            model="gpt-4o-2024-08-06",
            messages=[
                {
                    "role": "system", 
                    "content": 
                    """
                    You are an agent who can clean page content extracted with bs4
                    Your will be given a url and its content. Clean and parse the content for better readability.
                    The content MUST be in human readable markdown format.
                    """
                    },
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating chat completion: {str(e)}")