import functions_framework
from flask import jsonify
import llm_handler
import intent_handlers

@functions_framework.http
def handle_call(request):
    """
    Questo è il nostro "cervello orchestratore".
    """
    try:
        request_json = request.get_json(silent=True)
        transcribed_text = request_json.get('transcript', '')
        # Per ora lo stato della conversazione è un dizionario vuoto
        # In futuro, lo riceveremo da Retell ad ogni turno
        conversation_state = request_json.get('state', {})

        # 1. CAPIRE: Chiamiamo il modulo LLM per l'analisi
        intent, entities = llm_handler.analyze_text_with_gemini(transcribed_text)
        
        # 2. DECIDERE: Troviamo la funzione giusta da eseguire in base all'intento
        handler_function = getattr(intent_handlers, intent, intent_handlers.richiesta_incomprensibile)
        
        # 3. AGIRE: Eseguiamo la funzione e otteniamo la risposta
        response_text = handler_function(entities, conversation_state)

        # 4. RISPONDERE: Inviamo la risposta e il nuovo stato della conversazione
        response_data = {
            "response_text": response_text,
            "state": conversation_state
        }
        return jsonify(response_data), 200

    except Exception as e:
        print(f"Errore critico in main.py: {e}")
        return jsonify({"response_text": "Si è verificato un problema, la passo a un operatore."}), 200
