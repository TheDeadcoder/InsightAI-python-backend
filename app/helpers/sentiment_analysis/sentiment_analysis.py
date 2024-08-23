
from app.core.openai import openaiClient
from app.schemas.sentiment import SentimentEnum, SentimentAnalysis

def analyze_sentiment(text: str) -> SentimentAnalysis:
    system_prompt='''
        You are a helpful assistant. You analyze the sentiment from user-feedback on a product. Sentiment can be positive, negative or neutral
    '''

    completion = openaiClient.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ],
        response_format=SentimentAnalysis,
    )

    return completion.choices[0].message.parsed

    sentiments = list(SentimentEnum)
    sentiment = random.choice(sentiments)
    confidence = random.uniform(0.7, 1.0)
    
    return SentimentAnalysis(
        text=text,
        sentiment=sentiment,
        confidence=confidence
    )

def get_ticket_response_pydantic(query: str):
    completion = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query},
        ],
        response_format=TicketResolution,
    )

    return completion.choices[0].message.parsed