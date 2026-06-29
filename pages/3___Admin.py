import streamlit as st
import pandas as pd
from config import ROUNDS, ROUND_LABELS, TEAMS_PER_ROUND
from data_manager import get_current_window, get_results, save_result_batch, get_teams_for_window, get_windows_state, set_window_state, get_round_matchups, save_match_result, get_match_results
from styles import inject_custom_styles
from auth import get_all_registered_users
from scoring import calculate_user_score

st.set_page_config(page_title="Admin · Mundial 2026", layout="centered", page_icon="👑")
inject_custom_styles()

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Por favor, inicia sesión.")
    if st.button("← Volver"):
        st.switch_page("app.py")
    st.stop()

if not st.session_state.is_admin:
    st.error("🚫 No tienes permisos de administrador.")
    st.stop()

# ── Sidebar ──
with st.sidebar:
    st.markdown("""
    <div style="padding: 16px 0 8px 0;">
        <p style="font-size:0.75rem; text-transform:uppercase; letter-spacing:0.1em; color:#FFD700 !important; margin:0;">Admin</p>
        <h3 style="margin:4px 0 0 0; font-size:1.3rem; color:#fff !important;">Panel de control</h3>
    </div>
    """, unsafe_allow_html=True)
    st.divider()
    st.page_link("app.py", label="🏠 Inicio")
    st.page_link("pages/1___Predicción.py", label="🔮 Predicción")
    st.page_link("pages/2___Clasificación.py", label="📊 Clasificación")
    st.page_link("pages/4___Reglamento.py", label="📋 Reglamento")
    st.page_link("pages/3___Admin.py", label="👑 Admin")
    st.divider()
    from auth import logout_user
    if st.button("Cerrar Sesión", type="primary", use_container_width=True):
        logout_user()

# ── Header ──
st.markdown("""
<div style="margin-bottom:24px;">
    <p style="font-size:0.75rem; text-transform:uppercase; letter-spacing:0.12em; color:#FFD700; margin:0;">Panel exclusivo</p>
    <h1 style="margin:4px 0 0 0; font-size:2.2rem;">👑 Administración</h1>
</div>
""", unsafe_allow_html=True)

current_window = get_current_window()
res = get_results()

# ── Tournament status ──
st.markdown("#### Estado del Torneo")

# Progress through rounds
status_cols = st.columns(len(ROUNDS))
for i, ronda in enumerate(ROUNDS):
    teams_count = len(res.get(ronda, []))
    needed = TEAMS_PER_ROUND[ronda]
    completed = teams_count >= needed

    with status_cols[i]:
        icon = "✅" if completed else ("🔄" if ronda != "campeon" else "⏳")
        label = ROUND_LABELS.get(ronda, ronda)
        st.markdown(f"""
        <div style="text-align:center; padding:8px 4px; background:{'rgba(74,222,128,0.1)' if completed else 'rgba(255,255,255,0.04)'}; border-radius:8px; border:1px solid {'rgba(74,222,128,0.3)' if completed else 'rgba(255,255,255,0.1)'};">
            <div style="font-size:1.2rem;">{icon}</div>
            <p style="font-size:0.65rem; margin:2px 0 0 0; color:#8892a4 !important; line-height:1.2;">{label}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown(f"**Ventana activa:** `{current_window}`")
st.markdown("---")

# ── Window control ──
st.markdown("#### Control de Ventanas de Predicción")
st.info("Activa o desactiva las ventanas de predicción. Si una ventana está desactivada, los usuarios no podrán hacer predicciones en esa fase.")

windows_state = get_windows_state()
window_labels = {
    "P1": "P1 - Inicio (×4)",
    "P2": "P2 - Octavos (×3)",
    "P3": "P3 - Cuartos (×2)",
    "P4": "P4 - Semis (×1.5)",
    "P5": "P5 - Final (×1)"
}

col1, col2, col3, col4, col5 = st.columns(5)
cols = [col1, col2, col3, col4, col5]

for i, (window, label) in enumerate(window_labels.items()):
    with cols[i]:
        is_enabled = windows_state.get(window, True)
        if st.toggle(label, value=is_enabled, key=f"toggle_{window}"):
            set_window_state(window, True)
        else:
            set_window_state(window, False)

st.markdown("---")

# ── Results input ──
tab_results, tab_users = st.tabs(["📥 Cargar Resultados", "👥 Gestión de Usuarios"])

with tab_results:
    # Select round to input results
    round_options = ["dieciseisavos", "octavos", "cuartos", "semis", "final", "campeon"]
    selected_round = st.selectbox(
        "Selecciona la ronda para introducir resultados:",
        round_options,
        format_func=lambda x: ROUND_LABELS.get(x, x)
    )

    st.markdown("---")
    
    # Get matchups for selected round
    matchups = get_round_matchups(selected_round)
    
    if not matchups:
        st.warning(f"No se pueden generar los emparejamientos de {ROUND_LABELS.get(selected_round, selected_round)} aún. Primero completa la ronda anterior.")
    else:
        st.markdown(f"### {ROUND_LABELS.get(selected_round, selected_round)} - Resultados por partido")
        st.info("Introduce el ganador de cada partido. Los resultados se guardarán automáticamente.")
        
        # Get existing results for this round
        existing_results = get_match_results()
        existing_dict = {r["partido_id"]: r["ganador"] for r in existing_results if r["ronda"] == selected_round}
        
        from config import FLAGS
        
        for i, (team1, team2) in enumerate(matchups):
            partido_id = i + 1
            current_winner = existing_dict.get(partido_id)
            
            with st.container(border=True):
                col1, col2, col3 = st.columns([3, 1, 3])
                
                with col1:
                    flag1 = FLAGS.get(team1, "🏳️")
                    st.markdown(f"**{flag1} {team1}**")
                
                with col2:
                    st.markdown("<div style='text-align:center; padding:10px 0;'>**VS**</div>", unsafe_allow_html=True)
                
                with col3:
                    flag2 = FLAGS.get(team2, "🏳️")
                    st.markdown(f"**{flag2} {team2}**")
                
                st.markdown("---")
                
                # Winner selection
                winner_options = [team1, team2]
                winner = st.radio(
                    f"Ganador del partido {partido_id}:",
                    winner_options,
                    key=f"winner_{selected_round}_{partido_id}",
                    horizontal=True,
                    label_visibility="collapsed"
                )
                
                # Save button for this match
                if st.button(f"💾 Guardar resultado partido {partido_id}", key=f"save_{selected_round}_{partido_id}", use_container_width=True):
                    save_match_result(selected_round, partido_id, team1, team2, winner)
                    st.success(f"✅ Resultado guardado: {FLAGS.get(winner, '🏳️')} {winner}")
                    st.rerun()
    
    # Show current results for this round
    st.markdown("---")
    st.markdown(f"### Resultados actuales - {ROUND_LABELS.get(selected_round, selected_round)}")
    
    round_results = [r for r in get_match_results() if r["ronda"] == selected_round]
    
    if round_results:
        for r in round_results:
            flag = FLAGS.get(r["ganador"], "🏳️")
            st.markdown(f"**Partido {r['partido_id']}:** {FLAGS.get(r['equipo_local'], '🏳️')} {r['equipo_local']} vs {FLAGS.get(r['equipo_visitante'], '🏳️')} {r['equipo_visitante']} → **{flag} {r['ganador']}**")
    else:
        st.info("No hay resultados guardados para esta ronda aún.")

with tab_users:
    st.markdown("#### Usuarios registrados")
    users = get_all_registered_users()
    if "admin" in users:
        users.remove("admin")

    if not users:
        st.info("No hay usuarios registrados.")
    else:
        user_data_list = []
        for u in users:
            score, _ = calculate_user_score(u)
            from data_manager import is_prediction_locked
            locked_windows = [w for w in ["P1","P2","P3","P4","P5"] if is_prediction_locked(u, w)]
            user_data_list.append({
                "Usuario": u.capitalize(),
                "Puntos": score,
                "Predicciones bloqueadas": ", ".join(locked_windows) if locked_windows else "Ninguna"
            })

        user_data_list.sort(key=lambda x: x["Puntos"], reverse=True)
        df = pd.DataFrame(user_data_list)
        st.table(df)
        st.markdown(f"**Total de jugadores:** {len(users)}")
