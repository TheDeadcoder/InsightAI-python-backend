from app.core.openai import openaiClient


# TODO: Research the prompt, temperature, max_token

def clean_page_content(page_content:str, page_title:str):
    try:
        response = openaiClient.chat.completions.create(
            model="gpt-4o-2024-08-06",  
            messages=[
                {"role": "system", "content": "You are an AI assistant that cleans and improves text extracted by bs4 from web-page. Your task is to improve formatting, keeping only relevant parts and ensuring the text is clear and readable. Add no additional token"},
                {"role": "user", "content": f"Please clean and improve the following text extracted from a web-page titled:{page_title}\n\nPage content:\n{page_content}"}
            ],
            max_tokens=3000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error cleaning page content: {e}")
        return page_content  