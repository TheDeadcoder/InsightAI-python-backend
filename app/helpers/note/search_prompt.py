from app.core.openai import openaiClient
from app.schemas.note import search_prompt

def Generate_prompt(text: str) -> str:
    system_prompt='''
        You are a helpful assistant. You will have a knowledge basis. Based on this, You need to generate an appropriate string that will be used to search in YouTube.
        You MUST give Rational search-string under 5 words otherwise You will be fined 500$
    '''

    completion = openaiClient.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ],
        response_format=search_prompt,
    )

    outcome =  completion.choices[0].message.parsed
    return outcome.prompt