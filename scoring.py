# scoring.py
from config import POINTS, VALID_WINDOWS_FOR_ROUND, ROUNDS
from data_manager import get_results, load_user_prediction

def calculate_user_score(user):
    results = get_results()
    total_score = 0
    breakdown = []

    for ronda, equipos_reales in results.items():
        if not equipos_reales:
            continue

        ventanas_validas = VALID_WINDOWS_FOR_ROUND[ronda]

        for equipo in equipos_reales:
            user_windows_submitted = []
            for w in ventanas_validas:
                pred = load_user_prediction(user, w)
                if pred is not None:
                    user_windows_submitted.append(w)

            if not user_windows_submitted:
                continue

            latest_window = user_windows_submitted[-1]
            latest_pred = load_user_prediction(user, latest_window)

            if equipo not in latest_pred.get(ronda, []):
                continue

            earliest_chain_window = latest_window
            for w in reversed(user_windows_submitted[:-1]):
                past_pred = load_user_prediction(user, w)
                if past_pred and equipo in past_pred.get(ronda, []):
                    earliest_chain_window = w
                else:
                    break

            puntos_ganados = POINTS[ronda].get(earliest_chain_window, 0)
            total_score += puntos_ganados

            if puntos_ganados > 0:
                breakdown.append({
                    "Ronda": ronda,
                    "Equipo": equipo,
                    "Ventana": earliest_chain_window,
                    "Puntos": puntos_ganados
                })

    return total_score, breakdown


def calculate_user_score_by_round(user):
    """Returns a dict of {ronda: (score, breakdown)} for each round."""
    results = get_results()
    round_scores = {r: {"score": 0, "breakdown": []} for r in ROUNDS}

    for ronda, equipos_reales in results.items():
        if not equipos_reales:
            continue

        ventanas_validas = VALID_WINDOWS_FOR_ROUND[ronda]

        for equipo in equipos_reales:
            user_windows_submitted = []
            for w in ventanas_validas:
                pred = load_user_prediction(user, w)
                if pred is not None:
                    user_windows_submitted.append(w)

            if not user_windows_submitted:
                continue

            latest_window = user_windows_submitted[-1]
            latest_pred = load_user_prediction(user, latest_window)

            if equipo not in latest_pred.get(ronda, []):
                continue

            earliest_chain_window = latest_window
            for w in reversed(user_windows_submitted[:-1]):
                past_pred = load_user_prediction(user, w)
                if past_pred and equipo in past_pred.get(ronda, []):
                    earliest_chain_window = w
                else:
                    break

            puntos_ganados = POINTS[ronda].get(earliest_chain_window, 0)
            round_scores[ronda]["score"] += puntos_ganados

            if puntos_ganados > 0:
                round_scores[ronda]["breakdown"].append({
                    "Equipo": equipo,
                    "Ventana": earliest_chain_window,
                    "Puntos": puntos_ganados
                })

    return round_scores
