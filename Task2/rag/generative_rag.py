"""
Here I use gemini's fastest model for better natural answer with provided context
"""
from pydantic import BaseModel
import google.generativeai as genai

genai.configure(api_key="AIzaSyBOG4Y7LxvZP8efCGRSqM8OBwh8cbdYoMo")

model = genai.GenerativeModel("models/gemini-2.5-flash-lite")

class Rag2Input(BaseModel):
    data: dict
    question: str

def gen_ans(prompt: Rag2Input):
    """
    Coordinate the multi-agent system to generate comprehensive answers.
    """
    context = f"""
    You are given the following data:
    {prompt.data}

    Now answer this question based on that data:
    {prompt.question} + Make it short , to the point , within provided data, if comparison is asked just compare the main things, dont use decorators
    Input Example:
    "question": "Compare Samsung Galaxy S23 Ultra and S22 Ultra" 
    
    Output Example:
    "answer": "Samsung Galaxy S23 Ultra has better camera and battery
    life than S22 Ultra. Display is similar. Overall, S23 Ultra is
    recommended for photography and long usage." 
    """

    response = model.generate_content(context)
    answer = response.text.strip()

    return {
        "answer": answer
    }
