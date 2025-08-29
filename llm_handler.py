import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig
import json
import os

# Inizializzazione di Vertex AI (configurabile via env)
PROJECT_ID = os.environ.get("GCP_PROJECT", "receptionistai-470420")
LOCATION = os.environ.get("GCP_LOCATION", "europe-west1")
vertexai.init(project=PROJECT_ID, location=LOCATION)

# Modello configurabile via env per gestire disponibilità per regione
MODEL_NAME = os.environ.get("MODEL_NAME", "gemini-1.5-flash")

# Gli unici "compiti" che il nostro cervello MVP sa eseguire
KNOWN_INTENTS = [
    "creare_prenotazione",
    "chiedere_informazioni",
    "notificare_ritardo",
    "salutare",
    "richiesta_incomprensibile",
]


def analyze_text_with_gemini(text: str, restaurant_data: dict) -> (str, dict):
    """
    Interroga il modello Gemini per estrarre intento ed entità, usando i dati
    forniti come unica fonte di verità per evitare allucinazioni.
    """
    model = GenerativeModel(MODEL_NAME)

    context = f"""
    Contesto del Ristorante:
    - Nome: {restaurant_data.get('name')}
    - Orari: {restaurant_data.get('opening_hours')}
    - Indirizzo: {restaurant_data.get('address')}
    """

    # Prompt few-shot ottimizzato
    prompt = f"""Analizza la richiesta dell'utente per un ristorante e classifica l'intento.

CONTESTO RISTORANTE:
{context}

ESEMPI DI CLASSIFICAZIONE:
- "avete posto per due stasera?" → {{"intento": "creare_prenotazione", "entita": {{"numero_persone": "2", "data": "stasera"}}}}
- "dove siete?" / "dove vi trovate?" / "qual è il vostro indirizzo?" → {{"intento": "chiedere_informazioni", "entita": {{"richiesta_specifica": "indirizzo"}}}}
- "che orari fate?" / "siete aperti?" / "a che ora aprite?" → {{"intento": "chiedere_informazioni", "entita": {{"richiesta_specifica": "orari"}}}}
- "posso parlare col proprietario?" / "chi è il responsabile?" → {{"intento": "richiesta_incomprensibile", "entita": {{}}}}

FRASE DA ANALIZZARE: "{text}"

Restituisci SOLO il JSON con intento ed entità.
"""

    config = GenerationConfig(
        temperature=0.0,
        response_mime_type="application/json",
    )

    try:
        response = model.generate_content(prompt, generation_config=config)
        result = json.loads(response.text)
        return result.get("intento", "richiesta_incomprensibile"), result.get("entita", {})
    except Exception as e:
        print(f"Errore durante l'analisi con Gemini: {e}")
        return "richiesta_incomprensibile", {}
