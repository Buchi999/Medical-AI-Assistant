import os
import json
from groq import Groq
from dotenv import load_dotenv
from app.services.rag_service import setup_knowledge_base, retrieve_relevant_knowledge
from app.services.graph_service import find_diseases_by_symptoms

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

setup_knowledge_base()

def get_diagnosis(symptoms: list[str], age: int | None, history: list[str] | None):
    relevant_facts = retrieve_relevant_knowledge(symptoms)
    context = "\n".join(f"- {fact}" for fact in relevant_facts)

    graph_matches = find_diseases_by_symptoms(symptoms)
    graph_context = "\n".join(
        f"- {m['disease']}: matches {m['matches']} of the patient's symptoms"
        for m in graph_matches
    )

    prompt = f"""You are a medical assistant AI. Use the reference medical knowledge and 
symptom-matching data below to help inform your answer, combined with your own medical knowledge.

Reference medical knowledge:
{context}

Symptom-graph matches (ranked by number of matching symptoms):
{graph_context}

Patient information:
Symptoms: {', '.join(symptoms)}
Age: {age if age else 'not provided'}
Medical history: {', '.join(history) if history else 'none provided'}

Respond ONLY with valid JSON in exactly this format, no extra text:
{{
  "possible_conditions": [
    {{"condition": "string", "likelihood": "high/medium/low", "reasoning": "string"}}
  ],
  "recommendation": "string"
}}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
    )

    return json.loads(response.choices[0].message.content)