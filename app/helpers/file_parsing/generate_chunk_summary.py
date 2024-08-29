from app.core.openai import openaiClient

#################################################################################################
#   Helper function to generate the summary for a chunk. The summary is then prepended
#   input: semantic chunks, output: array of strings
#################################################################################################
def generate_summary(semantic_chunks):  
    summaries = []  # New list to store summaries
    for semantic_chunk in semantic_chunks:   
        prompt = f"Content: {semantic_chunk.page_content}"
        prompt += "\nPlease provide a brief summary about this content within 1 sentence."

        response = openaiClient.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
        ],
        )
        raw_response = response.choices[0].message.content
        summaries.append(raw_response)  
    
    return summaries  