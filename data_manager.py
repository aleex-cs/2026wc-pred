# data_manager.py
from config import ROUNDS, TEAMS_PER_ROUND, ROUND_OF_32_MATCHUPS
from auth import supabase

def init_db():
    """Initialize database - no-op for Supabase (schema created via SQL)"""
    pass

def get_results():
    """Get results from Supabase."""
    response = supabase.table("results").select("*").execute()
    results = {r: [] for r in ROUNDS}
    for row in response.data:
        if row["ronda"] in results:
            results[row["ronda"]].append(row["equipo"])
    return results

def save_result_batch(ronda, equipos):
    """Save batch of results to Supabase."""
    # Delete existing results for this round
    supabase.table("results").delete().eq("ronda", ronda).execute()
    
    # Insert new results
    new_rows = [{"ronda": ronda, "equipo": eq} for eq in equipos]
    supabase.table("results").insert(new_rows).execute()

def get_current_window():
    """Get current prediction window based on results."""
    res = get_results()
    if len(res["dieciseisavos"]) < TEAMS_PER_ROUND["dieciseisavos"]: return "P1"
    if len(res["octavos"]) < TEAMS_PER_ROUND["octavos"]: return "P2"
    if len(res["cuartos"]) < TEAMS_PER_ROUND["cuartos"]: return "P3"
    if len(res["semis"]) < TEAMS_PER_ROUND["semis"]: return "P4"
    if len(res["final"]) < TEAMS_PER_ROUND["final"]: return "P5"
    if len(res["campeon"]) < TEAMS_PER_ROUND["campeon"]: return "FINISHED"
    return "FINISHED"

def get_teams_for_window(window):
    """Get available teams for a prediction window."""
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
    """Save user prediction to Supabase. predictions is a dict {ronda: [equipos]}."""
    # Check if prediction exists
    existing = supabase.table("predictions").select("*").eq("username", user).eq("prediction_window", window).execute()
    
    if existing.data:
        # Update existing - save entire bracket as JSON
        supabase.table("predictions").update({
            "ronda": "full_bracket",
            "equipos": predictions
        }).eq("username", user).eq("prediction_window", window).execute()
    else:
        # Insert new - save entire bracket as JSON
        supabase.table("predictions").insert({
            "username": user,
            "prediction_window": window,
            "ronda": "full_bracket",
            "equipos": predictions
        }).execute()

def lock_prediction(user, window):
    """Lock user prediction for a window."""
    existing = supabase.table("prediction_locks").select("*").eq("username", user).eq("prediction_window", window).execute()
    
    if not existing.data:
        supabase.table("prediction_locks").insert({
            "username": user,
            "prediction_window": window
        }).execute()

def is_prediction_locked(user, window):
    """Check if user prediction is locked for a window."""
    response = supabase.table("prediction_locks").select("*").eq("username", user).eq("prediction_window", window).execute()
    return len(response.data) > 0

def load_user_prediction(user, window):
    """Load user prediction from Supabase. Returns the full bracket dict."""
    response = supabase.table("predictions").select("*").eq("username", user).eq("prediction_window", window).execute()
    if response.data:
        row = response.data[0]
        return row["equipos"]
    return None

def get_all_locked_windows(user):
    """Returns list of windows the user has locked predictions for."""
    response = supabase.table("prediction_locks").select("*").eq("username", user).execute()
    return [row["prediction_window"] for row in response.data]

def get_windows_state():
    """Returns dict of window -> enabled status."""
    response = supabase.table("windows_state").select("*").execute()
    return {row["prediction_window"]: row["enabled"] for row in response.data}

def set_window_state(window, enabled):
    """Enable or disable a prediction window."""
    supabase.table("windows_state").update({
        "enabled": enabled
    }).eq("prediction_window", window).execute()

def is_window_enabled(window):
    """Check if a prediction window is enabled by admin."""
    response = supabase.table("windows_state").select("*").eq("prediction_window", window).execute()
    if response.data:
        return response.data[0]["enabled"]
    return True
