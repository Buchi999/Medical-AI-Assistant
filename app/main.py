from fastapi import FastAPI
from pydantic import BaseModel
from app.services.llm_service import get_diagnosis

app = FastAPI()

class SymptomRequest(BaseModel):
    symptoms: list[str]
    age: int | None = None
    history: list[str] | None = None

@app.get("/")
def read_root():
    return {"message": "Medical AI Assistant API is running"}

@app.post("/diagnose")
def diagnose(request: SymptomRequest):
    result = get_diagnosis(request.symptoms, request.age, request.history)
    return {
        "received_symptoms": request.symptoms,
        "diagnosis": result
    }