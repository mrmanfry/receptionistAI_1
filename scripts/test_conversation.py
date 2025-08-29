import sys
import os

# Ensure project root is on the path when running from this file
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, os.pardir))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from intent_handlers import creare_prenotazione


def run_simulated_booking_conversation() -> None:
    state = {}

    # Turn 1: user provides number of people, missing time
    entities_turn1 = {"numero_persone": "quattro"}
    response1 = creare_prenotazione(entities_turn1, state)
    print("Turno 1 - Risposta:", response1)
    print("Turno 1 - Stato:", state)

    # Turn 2: user provides time, carries over prior state
    entities_turn2 = {"orario": "otto e mezza"}
    response2 = creare_prenotazione(entities_turn2, state)
    print("Turno 2 - Risposta:", response2)
    print("Turno 2 - Stato:", state)


if __name__ == "__main__":
    run_simulated_booking_conversation()


