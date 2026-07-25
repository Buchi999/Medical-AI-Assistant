import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI"),
    auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))
)

def test_connection():
    with driver.session() as session:
        result = session.run("RETURN 'Connected!' AS message")
        return result.single()["message"]
def build_graph():
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")  # clear old data first

        data = [
            ("Influenza", ["fever", "headache", "cough", "muscle aches", "fatigue"]),
            ("Acute Bronchitis", ["cough", "mild fever", "chest discomfort"]),
            ("Pneumonia", ["high fever", "chills", "cough", "chest pain", "shortness of breath"]),
            ("Asthma Exacerbation", ["wheezing", "shortness of breath", "chest tightness", "cough"]),
            ("Common Cold", ["mild fever", "sneezing", "sore throat", "cough"]),
            ("Migraine", ["headache", "nausea", "sensitivity to light", "sensitivity to sound"]),
            ("Tension Headache", ["headache", "stress"]),
            ("Gastroenteritis", ["nausea", "vomiting", "diarrhea", "abdominal cramps", "mild fever"]),
            ("Urinary Tract Infection", ["burning urination", "frequent urination", "lower abdominal discomfort"]),
            ("Strep Throat", ["sore throat", "fever", "swollen tonsils", "painful swallowing"]),
            ("Sinusitis", ["facial pain", "nasal congestion", "thick nasal discharge", "reduced smell"]),
            ("Allergic Rhinitis", ["sneezing", "itchy eyes", "runny nose", "nasal congestion"]),
            ("GERD", ["heartburn", "chest discomfort", "regurgitation"]),
            ("Anemia", ["fatigue", "pale skin", "shortness of breath", "dizziness"]),
            ("Hypothyroidism", ["fatigue", "weight gain", "cold intolerance", "dry skin"]),
            ("Type 2 Diabetes", ["excessive thirst", "frequent urination", "fatigue", "blurred vision"]),
            ("Hypertension", ["headache", "dizziness", "nosebleeds"]),
            ("Anxiety Disorder", ["excessive worry", "restlessness", "rapid heartbeat", "difficulty concentrating"]),
            ("Depression", ["low mood", "fatigue", "loss of interest", "sleep disturbances"]),
            ("Appendicitis", ["abdominal pain", "fever", "nausea"]),
        ]

        for disease, symptoms in data:
            session.run(
                "MERGE (d:Disease {name: $disease})",
                disease=disease
            )
            for symptom in symptoms:
                session.run(
                    """
                    MERGE (s:Symptom {name: $symptom})
                    MERGE (d:Disease {name: $disease})
                    MERGE (s)-[:SYMPTOM_OF]->(d)
                    """,
                    symptom=symptom, disease=disease
                )

def find_diseases_by_symptoms(symptoms: list[str]):
    with driver.session() as session:
        result = session.run(
            """
            MATCH (s:Symptom)-[:SYMPTOM_OF]->(d:Disease)
            WHERE s.name IN $symptoms
            RETURN d.name AS disease, count(s) AS matching_symptoms
            ORDER BY matching_symptoms DESC
            """,
            symptoms=symptoms
        )
        return [{"disease": r["disease"], "matches": r["matching_symptoms"]} for r in result]