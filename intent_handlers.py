from config import RESTAURANT_DATA

# --- Moduli di Azione per ogni Intento ---

def chiedere_informazioni(entities: dict, conversation_state: dict) -> str:
    # Per ora, risponde con dati statici. In futuro, potremmo differenziare
    # la risposta in base alle entità (es. se chiede solo l'indirizzo).
    return f"{RESTAURANT_DATA['opening_hours']} {RESTAURANT_DATA['address']}"

def creare_prenotazione(entities: dict, conversation_state: dict) -> str:
    # Uniamo le informazioni nuove (entities) con quelle vecchie (conversation_state)
    persone = entities.get("numero_persone") or conversation_state.get("numero_persone")
    orario = entities.get("orario") or conversation_state.get("orario")

    # Logica conversazionale per chiedere le informazioni mancanti
    if not persone:
        return "Certamente. Per quante persone desidera prenotare?"
    if not orario:
        # Aggiorniamo lo stato della conversazione con il numero di persone
        conversation_state["numero_persone"] = persone
        return f"Perfetto, per {persone}. A che ora?"
        
    # Se abbiamo tutto, confermiamo e resettiamo lo stato
    response = f"Ottimo. Confermo la sua prenotazione per {persone} alle {orario}. A presto!"
    conversation_state.clear() # Resettiamo lo stato per la prossima chiamata
    return response

def notificare_ritardo(entities: dict, conversation_state: dict) -> str:
    return "Grazie per averci avvisato, la aspettiamo."

def salutare(entities: dict, conversation_state: dict) -> str:
    return "Grazie per aver chiamato. Buona giornata!"

def richiesta_incomprensibile(entities: dict, conversation_state: dict) -> str:
    # In futuro, questa funzione attiverà il trasferimento di chiamata
    return "Mi scusi, non sono sicuro di aver capito. La passo a un operatore per aiutarla meglio."
