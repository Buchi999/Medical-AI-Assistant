import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_diagnosis(symptoms: list[str], age: int | None, history: list[str] | None):
    prompt = f"""You are a medical assistant AI. Based on the following patient information, 
suggest possible conditions and explain your reasoning clearly.

Symptoms: {', '.join(symptoms)}
Age: {age if age else 'not provided'}
Medical history: {', '.join(history) if history else 'none provided'}

Respond with:
1. Possible conditions (most likely first)
2. Reasoning for each
3. A recommendation to see a real doctor for confirmation
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
    )

    return response.choices[0].message.content