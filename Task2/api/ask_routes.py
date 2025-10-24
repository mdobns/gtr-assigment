"""
This files handles the /ask part and return answer
"""

from fastapi import APIRouter
from pydantic import BaseModel
from Task2 import DB_CONFIG
from Task2 import PhoneRAGAgent


ask_router = APIRouter()
rag = PhoneRAGAgent(DB_CONFIG)

# Input model for POST request
class QuestionInput(BaseModel):
    question: str
    

@ask_router.post("/ask")
async def ask_question(payload: QuestionInput):
    try:
        question = payload.question
        answer = rag.answer_question(question)

        return answer

    except Exception as e:
        return {
            "answer": f"Sorry, I encountered an error while processing your question: {str(e)}"
        }
