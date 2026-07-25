from pydantic import BaseModel

class ConditionResult(BaseModel):
    condition: str
    likelihood: str  # "high", "medium", "low"
    reasoning: str

class DiagnosisResponse(BaseModel):
    possible_conditions: list[ConditionResult]
    recommendation: str