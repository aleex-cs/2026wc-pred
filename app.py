# app.py
import streamlit as st
from data_manager import init_db
from auth import init_auth, register_user, login_user, logout_user
from styles import inject_custom_styles
from config import FLAGS

st.set_page_config(
    page_title="Mundial 2026",
    layout="centered",
    page_icon="🏆",
    initial_sidebar_state="collapsed"
)

init_db()
init_auth()
inject_custom_styles()

# ── Hide sidebar nav until logged in ──
if not st.session_state.get("logged_in"):
    st.markdown("""
    <style>
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    </style>
    """, unsafe_allow_html=True)

# ── Logged-in sidebar ──
if st.session_state.get("logged_in"):
    with st.sidebar:
        st.markdown(f"""
        <div style="padding: 16px 0 8px 0;">
            <p style="font-size:0.75rem; text-transform:uppercase; letter-spacing:0.1em; color:#FFD700 !important; margin:0;">Sesión activa</p>
            <h3 style="margin:4px 0 0 0; font-size:1.3rem; color:#fff !important;">{st.session_state.username.capitalize()}</h3>
        </div>
        """, unsafe_allow_html=True)
        st.divider()

        st.page_link("app.py", label="🏠 Inicio", icon=None)
        st.page_link("pages/1___Predicción.py", label="🔮 Mi Predicción")
        st.page_link("pages/2___Clasificación.py", label="📊 Clasificación")
        st.page_link("pages/4___Reglamento.py", label="📋 Reglamento")
        if st.session_state.is_admin:
            st.page_link("pages/3___Admin.py", label="👑 Admin")

        st.divider()
        if st.button("Cerrar Sesión", type="primary", use_container_width=True):
            logout_user()

# ── Main content ──
if st.session_state.get("logged_in"):
    # Welcome page
    st.markdown(f"""
    <div style="text-align:center; padding: 40px 0 20px 0;">
        <div style="font-size:4rem; margin-bottom:16px;">🏆</div>
        <h1 style="font-size:2.8rem; font-weight:800; background:linear-gradient(135deg,#FFD700,#FFA500); -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin:0;">2026 World Cup Bracket Predictor</h1>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"### ¡Bienvenido, {st.session_state.username.capitalize()}! 👋")
    st.markdown("Usa el menú lateral para navegar entre secciones.")

    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.markdown("### 🔮 Predicción")
            st.markdown("Arma tu bracket para la ronda activa y bloquea tu pronóstico antes de que empiece.")
            if st.button("Ir a Predicción", use_container_width=True, type="primary"):
                st.switch_page("pages/1___Predicción.py")
    with col2:
        with st.container(border=True):
            st.markdown("### 📊 Clasificación")
            st.markdown("Consulta el ranking global y ve cómo estás frente a los demás participantes.")
            if st.button("Ver Ranking", use_container_width=True):
                st.switch_page("pages/2___Clasificación.py")

    # Quick stats
    from data_manager import get_results, get_current_window, load_user_prediction, is_prediction_locked
    from config import ROUND_LABELS
    from scoring import calculate_user_score

    st.markdown("---")
    res = get_results()
    window = get_current_window()

    col1, col2, col3 = st.columns(3)
    total_score, _ = calculate_user_score(st.session_state.username)
    locked_window = is_prediction_locked(st.session_state.username, window) if window != "FINISHED" else True

    with col1:
        st.metric("Tus puntos", f"{total_score} pts")
    with col2:
        rounds_played = sum(1 for r, teams in res.items() if teams and r != "dieciseisavos")
        st.metric("Rondas completadas", str(rounds_played))
    with col3:
        status = "✅ Bloqueada" if locked_window else ("🔓 Pendiente" if window != "FINISHED" else "🏁 Terminado")
        st.metric(f"Predicción {window}", status)

else:
    # ── Login / Register page ──
    st.markdown("""
    <div style="text-align:center; padding: 48px 0 32px 0;">
        <div style="font-size:4.5rem; margin-bottom:16px;">⚽</div>
        <h1 style="font-size:3rem; font-weight:800; background:linear-gradient(135deg,#FFD700,#FFA500); -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin:0; line-height:1.1;">2026 World Cup Bracket Predictor</h1>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Iniciar Sesión", "Crear Cuenta"])

    with tab1:
        with st.form("login_form"):
            log_user = st.text_input("Usuario", placeholder="tu_usuario")
            log_pass = st.text_input("Contraseña", type="password", placeholder="••••••••")
            submit_log = st.form_submit_button("Entrar →", use_container_width=True, type="primary")

            if submit_log:
                if not log_user or not log_pass:
                    st.error("Rellena todos los campos.")
                else:
                    success, msg = login_user(log_user, log_pass)
                    if success:
                        st.rerun()
                    else:
                        st.error(msg)

    with tab2:
        with st.form("register_form"):
            reg_user = st.text_input("Nombre de usuario", placeholder="elige_un_nombre")
            reg_pass = st.text_input("Contraseña", type="password", placeholder="••••••••")
            reg_pass2 = st.text_input("Confirmar contraseña", type="password", placeholder="••••••••")
            submit_reg = st.form_submit_button("Crear cuenta →", use_container_width=True, type="primary")

            if submit_reg:
                if not reg_user or not reg_pass:
                    st.error("Rellena todos los campos.")
                elif reg_pass != reg_pass2:
                    st.error("Las contraseñas no coinciden.")
                else:
                    success, msg = register_user(reg_user, reg_pass)
                    if success:
                        st.success(f"{msg} ¡Ahora inicia sesión!")
                    else:
                        st.error(msg)
