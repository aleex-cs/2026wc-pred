import streamlit as st
import pandas as pd
from config import ROUNDS, ROUND_LABELS, TEAMS_PER_ROUND, ROUND_OF_32_MATCHUPS, FLAGS
from data_manager import get_current_window, get_teams_for_window, save_user_prediction, lock_prediction, is_prediction_locked, load_user_prediction, get_results, is_window_enabled
from styles import inject_custom_styles, render_bracket_view

st.set_page_config(page_title="Predicción · Mundial 2026", layout="wide", page_icon="🔮")
inject_custom_styles()

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Por favor, inicia sesión en la página principal.")
    if st.button("← Volver al inicio"):
        st.switch_page("app.py")
    st.stop()

# ── Sidebar ──
with st.sidebar:
    st.markdown(f"""
    <div style="padding: 16px 0 8px 0;">
        <p style="font-size:0.75rem; text-transform:uppercase; letter-spacing:0.1em; color:#FFD700 !important; margin:0;">Sesión activa</p>
        <h3 style="margin:4px 0 0 0; font-size:1.3rem; color:#fff !important;">{st.session_state.username.capitalize()}</h3>
    </div>
    """, unsafe_allow_html=True)
    st.divider()
    st.page_link("app.py", label="🏠 Inicio")
    st.page_link("pages/1___Predicción.py", label="🔮 Mi Predicción")
    st.page_link("pages/2___Clasificación.py", label="📊 Clasificación")
    st.page_link("pages/4___Reglamento.py", label="📋 Reglamento")
    if st.session_state.get("is_admin"):
        st.page_link("pages/3___Admin.py", label="👑 Admin")
    st.divider()
    from auth import logout_user
    if st.button("Cerrar Sesión", type="primary", use_container_width=True):
        logout_user()

username = st.session_state.username
window = get_current_window()

if window == "FINISHED":
    st.info("🏁 El torneo ha finalizado. Ya no se pueden hacer más predicciones.")
    st.stop()

if not is_window_enabled(window):
    st.error(f"🔒 La ventana de predicción {window} está desactivada por el administrador. No se pueden hacer predicciones en este momento.")
    st.stop()

# ── Header ──
st.markdown(f"""
<div style="margin-bottom:24px;">
    <p style="font-size:0.75rem; text-transform:uppercase; letter-spacing:0.12em; color:#FFD700; margin:0;">Ventana activa</p>
    <h1 style="margin:4px 0 0 0; font-size:2.2rem;">🔮 Predicción · {window}</h1>
</div>
""", unsafe_allow_html=True)

locked = is_prediction_locked(username, window)

if locked:
    st.success("🔒 Tu predicción está bloqueada. ¡Mucha suerte!")
    pred = load_user_prediction(username, window)
    results = get_results()
    if pred:
        st.markdown("### Tu Bracket")
        render_bracket_view(pred, results)

        # Legend
        st.markdown("""
        <div style="display:flex; gap:16px; margin-top:12px; font-size:0.78rem; color:#8892a4;">
            <span style="display:flex; align-items:center; gap:6px;">
                <span style="width:12px; height:12px; border-radius:3px; background:rgba(74,222,128,0.3); display:inline-block;"></span> Acertado
            </span>
            <span style="display:flex; align-items:center; gap:6px;">
                <span style="width:12px; height:12px; border-radius:3px; background:rgba(255,255,255,0.06); display:inline-block;"></span> Por confirmar
            </span>
        </div>
        """, unsafe_allow_html=True)
    st.stop()

# ── Build bracket UI ──
st.markdown("Selecciona el ganador de cada partido. Los ganadores avanzan automáticamente.")

if f"bracket_{window}" not in st.session_state:
    st.session_state[f"bracket_{window}"] = {r: [] for r in ROUNDS}

current_bracket = st.session_state[f"bracket_{window}"]

start_idx = int(window.replace("P", "")) - 1
rondas_a_jugar = ROUNDS[start_idx:-1]

def render_team_button(team, selected, key):
    flag = FLAGS.get(team, "🏳️")
    label = f"{flag} {team}"
    btn_type = "primary" if selected else "secondary"
    return st.button(label, key=key, type=btn_type, use_container_width=True)

def get_matchups(teams):
    return [(teams[i], teams[i+1]) for i in range(0, len(teams)-1, 2)] if len(teams) > 1 else []

current_round_teams = get_teams_for_window(window)

# ── Round Headers ──
header_cols = st.columns(len(rondas_a_jugar))
for i, col in enumerate(header_cols):
    ronda_juego = rondas_a_jugar[i]
    with col:
        st.markdown(f"""
        <div style="text-align:center; margin-bottom:12px; padding:8px; background:rgba(255,215,0,0.08); border-radius:8px; border:1px solid rgba(255,215,0,0.15);">
            <p style="margin:0; font-size:0.7rem; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; color:#FFD700 !important;">
                {ROUND_LABELS[ronda_juego]}
            </p>
        </div>
        """, unsafe_allow_html=True)

# ── Matches ──
st.markdown("<div id='bracket-start' style='display:none'></div>", unsafe_allow_html=True)
cols = st.columns(len(rondas_a_jugar))

for i, col in enumerate(cols):
    ronda_juego = rondas_a_jugar[i]
    ronda_destino = ROUNDS[start_idx + i + 1]

    with col:
        if ronda_juego == "dieciseisavos":
            matchups = ROUND_OF_32_MATCHUPS
        else:
            matchups = get_matchups(current_round_teams)

        next_round_teams = []

        for m_idx, match in enumerate(matchups):
            if len(match) == 2:
                t1, t2 = match
                with st.container(border=True):
                    t1_selected = t1 in current_bracket.get(ronda_destino, [])
                    t2_selected = t2 in current_bracket.get(ronda_destino, [])

                    if render_team_button(t1, t1_selected, f"btn_{ronda_juego}_{m_idx}_1_{t1}"):
                        if not t1_selected:
                            if t2 in current_bracket[ronda_destino]:
                                current_bracket[ronda_destino].remove(t2)
                            if t1 not in current_bracket[ronda_destino]:
                                current_bracket[ronda_destino].append(t1)
                            for next_r in ROUNDS[start_idx + i + 2:]:
                                current_bracket[next_r] = []
                            st.rerun()

                    if render_team_button(t2, t2_selected, f"btn_{ronda_juego}_{m_idx}_2_{t2}"):
                        if not t2_selected:
                            if t1 in current_bracket[ronda_destino]:
                                current_bracket[ronda_destino].remove(t1)
                            if t2 not in current_bracket[ronda_destino]:
                                current_bracket[ronda_destino].append(t2)
                            for next_r in ROUNDS[start_idx + i + 2:]:
                                current_bracket[next_r] = []
                            st.rerun()

                    if t1_selected: next_round_teams.append(t1)
                    elif t2_selected: next_round_teams.append(t2)
            else:
                st.markdown("<p style='color:#555; font-size:0.8rem; text-align:center;'>Esperando rival...</p>", unsafe_allow_html=True)

        current_round_teams = next_round_teams

# ── Progress indicator ──
st.markdown("---")
rondas_a_predecir = ROUNDS[start_idx + 1:]
total_needed = sum(TEAMS_PER_ROUND[r] for r in rondas_a_predecir)
total_done = sum(len(current_bracket.get(r, [])) for r in rondas_a_predecir)
progress = total_done / total_needed if total_needed > 0 else 0

col1, col2 = st.columns([3, 1])
with col1:
    st.progress(progress, text=f"Bracket completado: {total_done}/{total_needed} equipos seleccionados")
with col2:
    is_valid = all(len(current_bracket.get(r, [])) == TEAMS_PER_ROUND[r] for r in rondas_a_predecir)
    if st.button(
        "🔒 Confirmar y Bloquear" if is_valid else "⚠️ Completa el bracket",
        type="primary" if is_valid else "secondary",
        use_container_width=True,
        disabled=not is_valid
    ):
        save_user_prediction(username, window, current_bracket)
        lock_prediction(username, window)
        st.success("¡Predicción bloqueada con éxito!")
        st.rerun()
