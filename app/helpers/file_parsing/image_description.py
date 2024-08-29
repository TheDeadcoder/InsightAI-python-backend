import base64
from app.core.openai import openaiClient

# TODO: Maybe USE STRUCTURED LLM HERE


def generate_image_description(base64_image):
    try:
        
        
        response = openaiClient.chat.completions.create(
            model="gpt-4o-2024-08-06",  
            messages=[
                {    
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Describe the image in brief, highlighting all key features and relevant information points concisely. Don't add anything other than the description"},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
                    ]   
                }
            ],
            max_tokens=200
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating image description: {e}")
        return "[Image description generation failed]"