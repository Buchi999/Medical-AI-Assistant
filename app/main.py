from fastapi import FastAPI
from pydantic import BaseModel
from app.services.llm_service import get_diagnosis
from app.models.schemas import DiagnosisResponse

app = FastAPI()

class SymptomRequest(BaseModel):
    symptoms: list[str]
    age: int | None = None
    history: list[str] | None = None

@app.get("/")
def read_root():
    return {"message": "Medical AI Assistant API is running"}

@app.post("/diagnose", response_model=DiagnosisResponse)
def diagnose(request: SymptomRequest):
    result = get_diagnosis(request.symptoms, request.age, request.history)
    return result