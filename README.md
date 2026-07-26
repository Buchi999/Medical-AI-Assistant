# Medical AI Diagnosis Assistant

An AI-powered medical diagnosis assistant that suggests possible conditions from symptoms and medical history, with transparent reasoning. Built as a learning project covering the full modern AI application stack: LLMs, Retrieval-Augmented Generation (RAG), knowledge graphs, and production backend practices.

## Features

- Accepts patient symptoms, age, and medical history via a REST API
- Uses an LLM (Groq/Llama 3.3) to generate possible diagnoses with reasoning
- Grounds answers in a retrieval system (RAG) using a curated medical knowledge base
- Cross-references a Neo4j knowledge graph to rank conditions by symptom overlap
- Returns structured, validated JSON output (not free-text)
- Fully tested with pytest
- Containerized with Docker for consistent, portable deployment

## Architecture

    Client Request
          |
       FastAPI (/diagnose)
          |
          ├──> RAG (ChromaDB) ──> retrieves relevant medical facts
          ├──> Neo4j Graph ──> ranks diseases by symptom overlap
          |
       Combined into LLM prompt (Groq)
          |
       Structured JSON response (Pydantic-validated)

## Tech Stack

- **Backend:** FastAPI, Pydantic
- **LLM:** Groq API (Llama 3.3 70B)
- **RAG:** ChromaDB, sentence-transformers
- **Knowledge Graph:** Neo4j
- **Testing:** pytest
- **Containerization:** Docker

## Running Locally

1. Clone the repo and set up a virtual environment
2. `pip install -r requirements.txt`
3. Set up `.env` with your `GROQ_API_KEY` and Neo4j credentials
4. Run Neo4j Desktop locally and build the graph: `python -c "from app.services.graph_service import build_graph; build_graph()"`
5. Start the server: `uvicorn app.main:app --reload`
6. Visit `http://127.0.0.1:8000/docs` for interactive API docs

## Running with Docker

```
docker build -t medical-ai-assistant .
docker run -p 8000:8000 --env-file .env medical-ai-assistant
```

## Example Request

```json
POST /diagnose
{
  "symptoms": ["fever", "headache", "cough"],
  "age": 25,
  "history": ["asthma"]
}
```

## Disclaimer

This is an educational portfolio project and is not a substitute for professional medical advice.