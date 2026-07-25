import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_diagnosis(symptoms: list[str], age: int | None, history: list[str] | None):
    prompt = f"""You are a medical assistant AI. Based on the following patient information, 
suggest possible conditions.

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