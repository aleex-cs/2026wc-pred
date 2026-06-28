import streamlit as st
import pandas as pd
from config import ROUNDS, ROUND_LABELS, TEAMS_PER_ROUND
from data_manager import get_current_window, get_results, save_result_batch, get_teams_for_window, get_windows_state, set_window_state
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
    ronda_a_rellenar = None
    equipos_disponibles = []

    if len(res["octavos"]) < TEAMS_PER_ROUND["octavos"]:
        ronda_a_rellenar = "octavos"
        equipos_disponibles = get_teams_for_window("P1")
    elif len(res["cuartos"]) < TEAMS_PER_ROUND["cuartos"]:
        ronda_a_rellenar = "cuartos"
        equipos_disponibles = res["octavos"]
    elif len(res["semis"]) < TEAMS_PER_ROUND["semis"]:
        ronda_a_rellenar = "semis"
        equipos_disponibles = res["cuartos"]
    elif len(res["final"]) < TEAMS_PER_ROUND["final"]:
        ronda_a_rellenar = "final"
        equipos_disponibles = res["semis"]
    elif len(res["campeon"]) < TEAMS_PER_ROUND["campeon"]:
        ronda_a_rellenar = "campeon"
        equipos_disponibles = res["final"]
    else:
        st.success("🏁 ¡Mundial finalizado! Todos los resultados están cargados.")

    if ronda_a_rellenar:
        needed = TEAMS_PER_ROUND[ronda_a_rellenar]
        label = ROUND_LABELS.get(ronda_a_rellenar, ronda_a_rellenar)

        st.markdown(f"#### ¿Quiénes avanzan a {label}?")
        st.info(f"Selecciona exactamente **{needed}** equipos clasificados.")

        equipos_seleccionados = st.multiselect(
            f"Equipos que avanzan:",
            sorted(equipos_disponibles),
            max_selections=needed
        )

        sel_count = len(equipos_seleccionados)
        progress = sel_count / needed
        st.progress(progress, text=f"{sel_count}/{needed} equipos seleccionados")

        if sel_count == needed:
            st.markdown(f"**Equipos seleccionados:**")
            from config import FLAGS
            teams_str = "  ·  ".join([f"{FLAGS.get(t,'🏳️')} {t}" for t in equipos_seleccionados])
            st.markdown(teams_str)

            if st.button(f"✅ Guardar resultados de {label}", type="primary", use_container_width=True):
                save_result_batch(ronda_a_rellenar, equipos_seleccionados)
                st.success(f"✅ Resultados de {label} guardados correctamente.")
                st.rerun()
        else:
            st.button(f"Selecciona {needed - sel_count} más...", disabled=True, use_container_width=True)

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
