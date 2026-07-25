from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Medical AI Assistant API is running"}

def test_diagnose_valid_input():
    response = client.post("/diagnose", json={
        "symptoms": ["fever", "headache", "cough"],
        "age": 25,
        "history": ["asthma"]
    })
    assert response.status_code == 200
    data = response.json()
    assert "possible_conditions" in data
    assert "recommendation" in data
    assert len(data["possible_conditions"]) > 0

def test_diagnose_missing_symptoms():
    response = client.post("/diagnose", json={
        "age": 25
    })
    assert response.status_code == 422  # missing required field