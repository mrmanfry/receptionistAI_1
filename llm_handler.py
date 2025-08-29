import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig
import json
import os

# Inizializzazione di Vertex AI
# Forziamo l'uso dell'ID progetto corretto per evitare ambiguità
PROJECT_ID = "receptionistai-478428"
LOCATION = "europe-west1"
vertexai.init(project=PROJECT_ID, location=LOCATION)

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
    model = GenerativeModel("gemini-1.5-flash-001")

    context = f"""
    Contesto del Ristorante:
    - Nome: {restaurant_data.get('name')}
    - Orari: {restaurant_data.get('opening_hours')}
    - Indirizzo: {restaurant_data.get('address')}
    """

    prompt = f"""
        {context}

        Analizza la seguente frase di un utente: "{text}"

        Il tuo compito è:
        1. Identificare l'intento principale dell'utente. Gli intenti validi sono: {", ".join(KNOWN_INTENTS)}.
        2. Estrarre le entità. Le entità valide sono: 'numero_persone', 'data', 'orario', e 'richiesta_specifica' (valori ammessi: 'indirizzo'|'orari').
        3. Se l'intento è 'chiedere_informazioni', basa la tua risposta ESCLUSIVAMENTE sulle informazioni fornite nel "Contesto del Ristorante".
        4. NON DEVI ASSOLUTAMENTE inventare o aggiungere informazioni non presenti nel contesto (es. fermate della metropolitana, parcheggi, etc.). Se la domanda riguarda informazioni non presenti nel contesto, l'intento deve essere 'richiesta_incomprensibile'.

        Restituisci la tua analisi esclusivamente in formato JSON valido, con la seguente struttura precisa e senza testo extra:
        {"intento": "nome_intento", "entita": {"numero_persone": "..", "data": "..", "orario": "..", "richiesta_specifica": "indirizzo|orari"}}

        Il tuo unico e solo output deve essere un oggetto JSON valido. Non generare mai testo conversazionale o spiegazioni al di fuori dell'oggetto JSON.
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
