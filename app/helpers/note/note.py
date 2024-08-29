
from app.core.openai import openaiClient
from app.helpers.youtube.youtube_video import search_youtube_videos
from app.schemas.note import Note, Note_Response
from .search_prompt import Generate_prompt

def generate_note_helper(topic_name: str, knowledge_level: str, knowledge_base: str) -> Note_Response:
    system_prompt = f"""
    You are an AI agent designed to generate Notes for students. Your goal is to create high-quality notes based on a given topic and a learner's current knowledge level on that topic. The contents of the note must be relevant, easy to understand, and derived directly from the provided knowledge base.
    You MUST follow the output format for a Note
    - introduction_and_motivation: <A Brief introduction about the topic and motivation to learn it>
    - slides: 
           - slide_name: <Name of the sub-topic>
           - slide_content: <Detailed contents of the sub-topic with examples>
    - questions: <generate at least 4 to 5 questions on the topic. Format of the question is given below>
           - question: <Question on the topic>
           - answer: <Answer of the question with detailed explanation>
    - Conclusion: <A brief summary of the note and what more to learn/explore>
    """
    human_prompt = f"""
    Consider these points:
    - Topic: {topic_name}
    - My Knowledge Level on the topic: {knowledge_level} (beginner, intermediate, advanced)
    - Knowledge Base: The following content is the source material in markdown format
      {knowledge_base}
    """

    completion = openaiClient.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": human_prompt},
        ],
        response_format=Note,
    )
    note_content = completion.choices[0].message.parsed
    search_prompt = Generate_prompt(knowledge_base)
    print(search_prompt)
    videos = search_youtube_videos(search_prompt)
    note_response = Note_Response(note=note_content, videos=videos)

    return note_response