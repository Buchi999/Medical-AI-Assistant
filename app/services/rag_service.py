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