# data_manager.py
import os
import json
import pandas as pd
from config import ROUNDS, TEAMS_PER_ROUND, ROUND_OF_32_MATCHUPS

DATA_DIR = "data"
RESULTS_FILE = os.path.join(DATA_DIR, "results.csv")
LOCKS_FILE = os.path.join(DATA_DIR, "locks.json")

def init_db():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    if not os.path.exists(RESULTS_FILE):
        df = pd.DataFrame(columns=["ronda", "equipo"])
        df.to_csv(RESULTS_FILE, index=False)

    if not os.path.exists(LOCKS_FILE):
        with open(LOCKS_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)

def get_results():
    df = pd.read_csv(RESULTS_FILE)
    results = {r: [] for r in ROUNDS}
    for _, row in df.iterrows():
        if row["ronda"] in results:
            results[row["ronda"]].append(row["equipo"])
    return results

def save_result_batch(ronda, equipos):
    df = pd.read_csv(RESULTS_FILE)
    df = df[df["ronda"] != ronda]
    new_rows = pd.DataFrame([{"ronda": ronda, "equipo": eq} for eq in equipos])
    df = pd.concat([df, new_rows], ignore_index=True)
    df.to_csv(RESULTS_FILE, index=False)

def get_current_window():
    res = get_results()
    if len(res["dieciseisavos"]) < TEAMS_PER_ROUND["dieciseisavos"]: return "P1"
    if len(res["octavos"]) < TEAMS_PER_ROUND["octavos"]: return "P2"
    if len(res["cuartos"]) < TEAMS_PER_ROUND["cuartos"]: return "P3"
    if len(res["semis"]) < TEAMS_PER_ROUND["semis"]: return "P4"
    if len(res["final"]) < TEAMS_PER_ROUND["final"]: return "P5"
    if len(res["campeon"]) < TEAMS_PER_ROUND["campeon"]: return "FINISHED"
    return "FINISHED"

def get_teams_for_window(window):
    res = get_results()
    if window == "P1":
        teams = []
        for match in ROUND_OF_32_MATCHUPS:
            teams.extend(list(match))
        return teams
    if window == "P2": return res["dieciseisavos"]
    if window == "P3": return res["octavos"]
    if window == "P4": return res["cuartos"]
    if window == "P5": return res["semis"]
    return []

def save_user_prediction(user, window, predictions):
    filepath = os.path.join(DATA_DIR, f"predictions_{user.lower()}_{window}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(predictions, f, ensure_ascii=False, indent=4)

def lock_prediction(user, window):
    with open(LOCKS_FILE, "r", encoding="utf-8") as f:
        locks = json.load(f)

    if user not in locks:
        locks[user] = []

    if window not in locks[user]:
        locks[user].append(window)

    with open(LOCKS_FILE, "w", encoding="utf-8") as f:
        json.dump(locks, f)

def is_prediction_locked(user, window):
    if not os.path.exists(LOCKS_FILE):
        return False
    with open(LOCKS_FILE, "r", encoding="utf-8") as f:
        locks = json.load(f)
    return window in locks.get(user, [])

def load_user_prediction(user, window):
    filepath = os.path.join(DATA_DIR, f"predictions_{user.lower()}_{window}.json")
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def get_all_locked_windows(user):
    """Returns list of windows the user has locked predictions for."""
    if not os.path.exists(LOCKS_FILE):
        return []
    with open(LOCKS_FILE, "r", encoding="utf-8") as f:
        locks = json.load(f)
    return locks.get(user, [])
