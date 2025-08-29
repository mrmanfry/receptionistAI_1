## AI Receptionist Backend (MVP)

### Endpoint
`POST /` (Google Cloud Function)

Body esempio (turno 1):
```json
{
  "transcript": "Vorrei prenotare un tavolo per quattro persone.",
  "state": {}
}
```

Risposta attesa:
```json
{
  "response_text": "Perfetto, per quattro. A che ora?",
  "state": { "numero_persone": "quattro" }
}
```

Body esempio (turno 2):
```json
{
  "transcript": "Per le otto e mezza.",
  "state": { "numero_persone": "quattro" }
}
```

Risposta attesa:
```json
{
  "response_text": "Ottimo. Confermo la sua prenotazione per quattro alle otto e mezza. A presto!",
  "state": {}
}
```

### Test locale senza Vertex AI
Esegui la simulazione della conversazione (2 turni) usando solo la logica degli intenti:

```bash
python3 scripts/test_conversation.py
```

Output atteso:
```
Turno 1 - Risposta: Perfetto, per quattro. A che ora?
Turno 1 - Stato: {'numero_persone': 'quattro'}
Turno 2 - Risposta: Ottimo. Confermo la sua prenotazione per quattro alle otto e mezza. A presto!
Turno 2 - Stato: {}
```

### Note Retell AI
- Invia al webhook il campo `state` ricevuto nella risposta precedente.
- Il backend risponde sempre con `state` aggiornato da usare nel turno successivo.
- Se la tua integrazione usa una chiave diversa (es. `memory`), mappa a `state` in ingresso/uscita in `main.py`.

### Configurazione Vertex AI
Imposta le variabili d'ambiente:
```bash
export GCP_PROJECT="<project-id>"
export GOOGLE_APPLICATION_CREDENTIALS="/path/service-account.json"
```


