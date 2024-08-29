
from app.core.openai import openaiClient
from app.schemas.flashcard import QuizResponse_stepped

def stepped_flashcard_set_generate(topic_name: str, difficulty_level: str, number_of_questions: int, question_type: str, knowledge_base: str) -> QuizResponse_stepped:
    system_prompt = f"""
    You are an AI designed to generate flashcard based quiz. Your goal is to create high-quality questions based on the topic, difficulty level, and type specified. The questions must be relevant, challenging based on the difficulty level, and derived directly from the provided knowledge base.
    You MUST follow the output format for a question
    - Question: <The question text>
    - Answer: <A List of steps each step solving a sub-problem of the main problem>
    - Step: 
           - step_name: <Name of the subproblem>
           - step_solution: <Solution of the sub-problem>
    - Conclusion: <A brief summary of the steps and the approach to solve the problem>
    - tips_and_tricks: <Additional tips to tackle similar kind of questions>
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
        response_format=QuizResponse_stepped,
    )
    print(completion.choices[0].message.parsed)

    return completion.choices[0].message.parsed