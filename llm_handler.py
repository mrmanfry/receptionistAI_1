import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig
import json
import os

# Inizializzazione di Vertex AI
PROJECT_ID = os.environ.get("GCP_PROJECT", "default-project") # Aggiunto un default per test locali
LOCATION = "europe-west1"
vertexai.init(project=PROJECT_ID, location=LOCATION)

# Gli unici "compiti" che il nostro cervello MVP sa eseguire
KNOWN_INTENTS = [
    "creare_prenotazione", 
    "chiedere_informazioni", 
    "notificare_ritardo",
    "salutare",
    "richiesta_incomprensibile"
]

def analyze_text_with_gemini(text: str) -> (str, dict):
    """
    Interroga il modello Gemini per estrarre intento ed entità.
    """
    model = GenerativeModel("gemini-1.5-flash-001")
    
    prompt = f"""
        Analizza la seguente frase di un utente che ha chiamato un ristorante italiano: "{text}"
        Il tuo compito è identificare l'intento principale e estrarre le entità.
        Gli intenti validi sono: {", ".join(KNOWN_INTENTS)}.
        Le entità valide sono: 'numero_persone', 'data', 'orario'.
        Restituisci la tua analisi esclusivamente in formato JSON, con la seguente struttura:
        {{"intento": "nome_intento", "entita": {{"nome_entita": "valore_entita"}}}}
        Se non riesci a identificare un intento valido, usa "richiesta_incomprensibile".
    """
    
    config = GenerationConfig(
        temperature=0.0,
        response_mime_type="application/json"
    )

    try:
        response = model.generate_content(prompt, generation_config=config)
        result = json.loads(response.text)
        return result.get("intento", "richiesta_incomprensibile"), result.get("entita", {})
    except Exception as e:
        print(f"Errore durante l'analisi con Gemini: {e}")
        return "richiesta_incomprensibile", {}
