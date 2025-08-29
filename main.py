import functions_framework
from flask import jsonify
import llm_handler
import intent_handlers
from config import RESTAURANT_DATA
import json

@functions_framework.http
def handle_call(request):
    """
    Questo è il nostro "cervello orchestratore".
    """
    try:
        # Log richiesta in entrata
        incoming_data = request.get_json(silent=True)
        print("--- DATI RICEVUTI DA RETELL AI ---")
        import json as _json
        print(_json.dumps(incoming_data, indent=2))
        print("-----------------------------------")
        transcribed_text = (incoming_data or {}).get('transcript', '')
        # Per ora lo stato della conversazione è un dizionario vuoto
        # In futuro, lo riceveremo da Retell ad ogni turno
        conversation_state = (incoming_data or {}).get('state', {})

        # 1. CAPIRE: Chiamiamo il modulo LLM per l'analisi con grounding sui dati del ristorante
        dati_ristorante_corrente = RESTAURANT_DATA
        intent, entities = llm_handler.analyze_text_with_gemini(transcribed_text, dati_ristorante_corrente)
        
        # 2. DECIDERE: Troviamo la funzione giusta da eseguire in base all'intento
        handler_function = getattr(intent_handlers, intent, intent_handlers.richiesta_incomprensibile)
        
        # 3. AGIRE: Eseguiamo la funzione e otteniamo la risposta
        response_text = handler_function(entities, conversation_state)

        # 4. RISPONDERE: Inviamo la risposta e il nuovo stato della conversazione
        response_data = {
            "response_text": response_text,
            "state": conversation_state
        }

        print("--- OUTPUT INVIATO A RETELL AI ---")
        import json as _json
        print(_json.dumps(response_data, indent=2))
        print("------------------------------------")
        return jsonify(response_data), 200

    except Exception as e:
        print(f"Errore critico in main.py: {e}")
        return jsonify({"response_text": "Si è verificato un problema, la passo a un operatore."}), 200
