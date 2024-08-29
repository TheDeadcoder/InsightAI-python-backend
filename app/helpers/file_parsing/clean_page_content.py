from app.core.openai import openaiClient


# TODO: Research the prompt, temperature, max_token

def clean_page_content(page_content):
    try:
        response = openaiClient.chat.completions.create(
            model="gpt-4o-2024-08-06",  
            messages=[
                {"role": "system", "content": "You are an AI assistant that cleans and improves text extracted from PDFs. Your task is to correct any OCR errors, improve formatting, and ensure the text is clear and readable. Add no additional token"},
                {"role": "user", "content": f"Please clean and improve the following text extracted from a PDF:\n\n{page_content}"}
            ],
            max_tokens=3000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error cleaning page content: {e}")
        return page_content  