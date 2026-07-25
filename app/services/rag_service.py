import chromadb
from chromadb.utils import embedding_functions

client = chromadb.Client()

embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

collection = client.get_or_create_collection(
    name="medical_knowledge",
    embedding_function=embedding_fn
)

# Sample medical knowledge — replace/expand later with a real dataset
knowledge_base = [
    {"id": "1", "text": "Influenza (flu) commonly causes fever, headache, muscle aches, cough, and fatigue. Onset is usually sudden."},
    {"id": "2", "text": "Acute bronchitis causes a persistent cough, often with mucus, mild fever, and chest discomfort. Often follows a cold."},
    {"id": "3", "text": "Pneumonia causes high fever, chills, cough with phlegm, chest pain when breathing, and shortness of breath."},
    {"id": "4", "text": "Asthma exacerbation causes wheezing, shortness of breath, chest tightness, and cough, often triggered by infection or allergens."},
    {"id": "5", "text": "The common cold causes mild fever, sneezing, sore throat, and cough, with gradual onset over a few days."},
    {"id": "6", "text": "Migraine causes throbbing headache, often one-sided, with nausea, and sensitivity to light and sound."},
    {"id": "7", "text": "Tension headache causes a dull, constant ache on both sides of the head, often linked to stress or poor posture."},
    {"id": "8", "text": "Gastroenteritis causes nausea, vomiting, diarrhea, abdominal cramps, and sometimes mild fever."},
    {"id": "9", "text": "Urinary tract infection causes burning during urination, frequent urge to urinate, and lower abdominal discomfort."},
    {"id": "10", "text": "Strep throat causes severe sore throat, fever, swollen tonsils, and painful swallowing, without cough."},
    {"id": "11", "text": "Sinusitis causes facial pain and pressure, nasal congestion, thick nasal discharge, and reduced sense of smell."},
    {"id": "12", "text": "Allergic rhinitis causes sneezing, itchy eyes, runny nose, and nasal congestion, often triggered by pollen or dust."},
    {"id": "13", "text": "Gastroesophageal reflux disease (GERD) causes heartburn, chest discomfort, and regurgitation, often worse after meals."},
    {"id": "14", "text": "Anemia causes fatigue, pale skin, shortness of breath, and dizziness, due to low red blood cell count."},
    {"id": "15", "text": "Hypothyroidism causes fatigue, weight gain, cold intolerance, dry skin, and depression."},
    {"id": "16", "text": "Type 2 diabetes causes excessive thirst, frequent urination, fatigue, and blurred vision."},
    {"id": "17", "text": "Hypertension is often asymptomatic but can cause headaches, dizziness, and nosebleeds in severe cases."},
    {"id": "18", "text": "Anxiety disorder causes excessive worry, restlessness, rapid heartbeat, and difficulty concentrating."},
    {"id": "19", "text": "Depression causes persistent low mood, fatigue, loss of interest, and sleep disturbances."},
    {"id": "20", "text": "Appendicitis causes sudden abdominal pain starting near the navel and moving to the lower right side, with fever and nausea."},
]

def setup_knowledge_base():
    existing = collection.count()
    if existing == 0:
        collection.add(
            ids=[item["id"] for item in knowledge_base],
            documents=[item["text"] for item in knowledge_base],
        )

def retrieve_relevant_knowledge(symptoms: list[str], n_results: int = 3):
    query = ", ".join(symptoms)
    results = collection.query(query_texts=[query], n_results=n_results)
    return results["documents"][0]