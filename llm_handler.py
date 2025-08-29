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

    # Esempio JSON separato per evitare errori di formattazione nelle f-string
    json_structure_example = (
        '{"intento": "nome_intento", '
        '"entita": {"numero_persone": "..", "data": "..", "orario": "..", "richiesta_specifica": "indirizzo|orari"}}'
    )

    prompt = f"""
        Sei un analista di linguaggio naturale super-efficiente per il centralino di un ristorante.
        Il tuo unico compito è analizzare la frase dell'utente e restituire la tua analisi in un formato JSON pulito.
        Il contesto con le informazioni certe del ristorante è il seguente:
        {context}

        Analizza questa frase dell'utente: "{text}"

        Segui queste regole in modo ferreo:
        1. Identifica l'intento tra i seguenti valori: {", ".join(KNOWN_INTENTS)}.
        2. Estrai le entità rilevanti. Le chiavi valide sono: 'numero_persone', 'data', 'orario', 'richiesta_specifica'.
        3. Per 'richiesta_specifica', i valori possibili sono solo 'indirizzo' o 'orari'.
        4. Se la richiesta dell'utente è ambigua, non rientra negli intenti, o chiede informazioni non presenti nel contesto, DEVI usare l'intento 'richiesta_incomprensibile'.
        5. Il tuo output deve essere solo e soltanto l'oggetto JSON. Non includere mai commenti, spiegazioni o testo conversazionale.

        JSON Output:
        {json_structure_example}
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
