from fastapi import APIRouter, HTTPException
from app.helpers.mcq_quiz.mcq_generate import mcq_quesation_set_generate
from app.schemas.mcq_quiz import QuizRequest, QuizResponse, Question
from app.helpers.qdrant_functions import file_fetch

router = APIRouter()

@router.post("/", response_model=QuizResponse)
async def generate_quiz(request: QuizRequest):
    
    if request.number_of_questions <= 0:
        raise HTTPException(status_code=400, detail="Number of questions must be greater than zero.")
    
    knowledge_base = file_fetch(str(request.collection_name), str(request.collection_id), str(request.file_id))
    print(knowledge_base)


    


    # Simulating quiz generation (this is where you would fetch/generate real questions)
    quiz_response = mcq_quesation_set_generate(str(request.topic_name),str(request.difficulty_level), request.number_of_questions, str(request.question_type),str(knowledge_base))
    generated_questions = quiz_response.questions[:request.number_of_questions]

    return QuizResponse(questions=generated_questions)

