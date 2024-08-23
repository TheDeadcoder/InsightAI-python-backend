from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings
from fastapi import HTTPException

#################################################################################################
#   Helper function to get the chunks for any text
#   input: string, output: array of semantically similar chunks
#   used method: percentile -> default value for breakpoint = 95%
#################################################################################################
def create_semantic_chunks_95(text_content):
    try:
        semantic_chunker = SemanticChunker(OpenAIEmbeddings(model="text-embedding-3-large"), breakpoint_threshold_type="percentile")
        semantic_chunks = semantic_chunker.create_documents([text_content])
        return semantic_chunks
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating embedding: {str(e)}")
    

#################################################################################################
#   Helper function to get the chunks for any text
#   input: string, output: array of semantically similar chunks
#   used method: percentile -> Here I fixed the percentile to 70%
#   NEED TO TEST THE PERCENTILE FOR BETTER PERFORMANCE
#################################################################################################
def create_semantic_chunks_70(text_content, breakpoint_threshold=70):
    try:
        semantic_chunker = SemanticChunker(
            embeddings=OpenAIEmbeddings(model="text-embedding-3-large"),
            breakpoint_threshold_type="percentile",
            breakpoint_threshold_amount=breakpoint_threshold
        )
        semantic_chunks = semantic_chunker.create_documents([text_content])
        return semantic_chunks
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating embedding: {str(e)}")
    

#################################################################################################
#   Helper function to get the chunks for any text
#   input: string, output: array of semantically similar chunks
#   used method: percentile -> Here I fixed the percentile to 80%
#   NEED TO TEST THE PERCENTILE FOR BETTER PERFORMANCE
#################################################################################################
def create_semantic_chunks_80(text_content, breakpoint_threshold=80):
    try:
        semantic_chunker = SemanticChunker(
            embeddings=OpenAIEmbeddings(model="text-embedding-3-large"),
            breakpoint_threshold_type="percentile",
            breakpoint_threshold_amount=breakpoint_threshold
        )
        semantic_chunks = semantic_chunker.create_documents([text_content])
        return semantic_chunks
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating embedding: {str(e)}")
