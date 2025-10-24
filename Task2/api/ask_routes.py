from fastapi import APIRouter
from pydantic import BaseModel
from Task2 import DB_CONFIG
from Task2 import PhoneRAGAgent



router = APIRouter()
rag = PhoneRAGAgent(DB_CONFIG)

# Input model for POST request
class QuestionInput(BaseModel):
    question: str
    

@router.post("/")  # Changed to /ask to match requirements
async def ask_question(payload: QuestionInput):
    try:
        question = payload.question
        answer = rag.answer_question(question)
        # Ensure the response matches the example format
        if isinstance(answer, dict) and "answer" in answer:
            return answer
        else:
            return {"answer": str(answer)}
    except Exception as e:
        return {
            "answer": f"Sorry, I encountered an error while processing your question: {str(e)}"
        }
