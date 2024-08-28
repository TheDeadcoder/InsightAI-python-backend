from fastapi import APIRouter, HTTPException

from app.helpers.flashcard_quiz.non_stepped import non_stepped_flashcard_set_generate
from app.helpers.flashcard_quiz.stepped import stepped_flashcard_set_generate
from app.schemas.flashcard import flashcardRequest, QuizResponse_non_stepped, QuizResponse_stepped
from app.helpers.qdrant_functions import file_fetch

router = APIRouter()

@router.post("/non-step", response_model=QuizResponse_non_stepped)
async def generate_non_stepped_flashcards(request: flashcardRequest):
    
    if request.number_of_questions <= 0:
        raise HTTPException(status_code=400, detail="Number of questions must be greater than zero.")
    
    knowledge_base = file_fetch(str(request.collection_name), str(request.collection_id), str(request.file_id))
    print(knowledge_base)

    quiz_response = non_stepped_flashcard_set_generate(str(request.topic_name),str(request.difficulty_level), request.number_of_questions, str(request.question_type),str(knowledge_base))
    generated_questions = quiz_response.questions[:request.number_of_questions]

    return QuizResponse_non_stepped(questions=generated_questions)

@router.post("/step", response_model=QuizResponse_stepped)
async def generate_non_stepped_flashcards(request: flashcardRequest):
    
    if request.number_of_questions <= 0:
        raise HTTPException(status_code=400, detail="Number of questions must be greater than zero.")
    
    knowledge_base = file_fetch(str(request.collection_name), str(request.collection_id), str(request.file_id))
    print(knowledge_base)

    quiz_response = stepped_flashcard_set_generate(str(request.topic_name),str(request.difficulty_level), request.number_of_questions, str(request.question_type),str(knowledge_base))
    generated_questions = quiz_response.questions[:request.number_of_questions]

    return QuizResponse_stepped(questions=generated_questions)

