
from app.core.openai import openaiClient
from app.schemas.mcq_quiz import Question, QuizResponse

def mcq_quesation_set_generate(topic_name: str, difficulty_level: str, number_of_questions: int, question_type: str, knowledge_base: str) -> QuizResponse:
    system_prompt = f"""
    You are an AI designed to generate quiz questions. Your goal is to create high-quality questions based on the topic, difficulty level, and type specified. The questions must be relevant, challenging based on the difficulty level, and derived directly from the provided knowledge base.
    You MUST follow the output format for a question
    - Question: <The question text>
    - Options: <List of 4 answer options>
    - CorrectAnswer: <Index of the correct option (0-3)>
    - Explanation: <Brief explanation of the answer>
    """
    human_prompt = f"""
    Consider these points:
    - Topic: {topic_name}
    - Difficulty Level: {difficulty_level} (easy, medium, hard)
    - Number of Questions: {number_of_questions}
    - Question Type: {question_type} (e.g., scenario-based, information-based, etc.)
    - Knowledge Base: The following content is the source material in markdown format
      {knowledge_base}
    """

    completion = openaiClient.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": human_prompt},
        ],
        response_format=QuizResponse,
    )
    print(completion.choices[0].message.parsed)

    return completion.choices[0].message.parsed