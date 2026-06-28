import streamlit as st
import pandas as pd
from auth import get_all_registered_users
from scoring import calculate_user_score, calculate_user_score_by_round
from styles import inject_custom_styles, render_bracket_view
from data_manager import get_results, load_user_prediction, get_all_locked_windows, is_prediction_locked, get_current_window
from config import ROUNDS, ROUND_LABELS, TROPHY_EMOJIS, FLAGS

st.set_page_config(page_title="Clasificación · Mundial 2026", layout="wide", page_icon="📊")
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

# ── Header ──
st.markdown("""
<div style="margin-bottom:24px;">
    <p style="font-size:0.75rem; text-transform:uppercase; letter-spacing:0.12em; color:#FFD700; margin:0;">En directo</p>
    <h1 style="margin:4px 0 0 0; font-size:2.2rem;">📊 Clasificación</h1>
</div>
""", unsafe_allow_html=True)

users = get_all_registered_users()
if "admin" in users:
    users.remove("admin")

if not users:
    st.info("Aún no hay usuarios registrados.")
    st.stop()

# ── Build leaderboard data ──
leaderboard = []
for u in users:
    score, breakdown = calculate_user_score(u)
    round_scores = calculate_user_score_by_round(u)
    leaderboard.append({
        "username": u,
        "display": u.capitalize(),
        "total": score,
        "breakdown": breakdown,
        "round_scores": round_scores
    })

leaderboard.sort(key=lambda x: x["total"], reverse=True)

# ── My rank highlight ──
my_rank = next((i + 1 for i, u in enumerate(leaderboard) if u["username"] == st.session_state.username), None)
my_score = next((u["total"] for u in leaderboard if u["username"] == st.session_state.username), 0)

if my_rank:
    rank_emoji = TROPHY_EMOJIS[my_rank - 1] if my_rank <= 3 else f"#{my_rank}"
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,rgba(255,215,0,0.1),rgba(255,165,0,0.05)); border:1px solid rgba(255,215,0,0.3); border-radius:12px; padding:16px 20px; margin-bottom:20px; display:flex; justify-content:space-between; align-items:center;">
        <div>
            <p style="margin:0; font-size:0.75rem; color:#FFD700 !important; text-transform:uppercase; letter-spacing:0.08em;">Tu posición</p>
            <p style="margin:4px 0 0 0; font-size:1.6rem; font-weight:800; color:#fff !important;">{rank_emoji} {st.session_state.username.capitalize()}</p>
        </div>
        <div style="text-align:right;">
            <p style="margin:0; font-size:0.75rem; color:#FFD700 !important; text-transform:uppercase; letter-spacing:0.08em;">Puntos</p>
            <p style="margin:4px 0 0 0; font-size:2rem; font-weight:800; color:#FFD700 !important;">{my_score}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Tabs: Global / Por ronda / Predicciones / Duelo ──
tab_global, tab_rounds, tab_preds, tab_duel = st.tabs(["🌍 Global", "🔢 Por Ronda", "🔮 Predicciones", "⚔️ Duelo"])

with tab_global:
    # Podium
    if len(leaderboard) >= 1:
        st.markdown("#### 🏆 Podio")
        if len(leaderboard) >= 3:
            col2, col1, col3 = st.columns(3)
            podium_cols = [(col1, leaderboard[0], "🥇", "podium-gold"), (col2, leaderboard[1], "🥈", "podium-silver"), (col3, leaderboard[2], "🥉", "podium-bronze")]
        elif len(leaderboard) == 2:
            col1, col2 = st.columns(2)
            podium_cols = [(col1, leaderboard[0], "🥇", "podium-gold"), (col2, leaderboard[1], "🥈", "podium-silver")]
        else:
            podium_cols = [(st.columns(1)[0], leaderboard[0], "🥇", "podium-gold")]

        for col, user_data, medal, css_class in podium_cols:
            with col:
                with st.container(border=True):
                    st.markdown(f"""
                    <div style="text-align:center; padding:8px 0;">
                        <div style="font-size:2rem;">{medal}</div>
                        <p style="font-size:1.1rem; font-weight:700; color:#fff !important; margin:4px 0;">{user_data['display']}</p>
                        <p style="font-size:1.4rem; font-weight:800; color:#FFD700 !important; margin:0;">{user_data['total']} pts</p>
                    </div>
                    """, unsafe_allow_html=True)

    # Full ranking table
    st.markdown("#### 📋 Ranking completo")

    for i, user_data in enumerate(leaderboard):
        rank_icon = TROPHY_EMOJIS[i] if i < 3 else f"`#{i+1}`"
        is_me = user_data["username"] == st.session_state.username
        label = f"{TROPHY_EMOJIS[i] if i < 3 else f'#{i+1}'} · {user_data['display']}{' (tú)' if is_me else ''} · {user_data['total']} pts"

        with st.expander(label, expanded=is_me):
            if user_data["breakdown"]:
                df = pd.DataFrame(user_data["breakdown"])
                df["Ronda"] = df["Ronda"].map(lambda r: ROUND_LABELS.get(r, r.capitalize()))
                df = df.rename(columns={"Ronda": "Ronda", "Equipo": "Equipo", "Ventana": "Ventana", "Puntos": "Puntos"})
                st.table(df[["Ronda", "Equipo", "Ventana", "Puntos"]])
                st.markdown(f"**Total: {user_data['total']} puntos**")
            else:
                st.markdown("Aún no ha sumado puntos.")

with tab_rounds:
    results = get_results()
    played_rounds = [r for r in ROUNDS if results.get(r) and r != "dieciseisavos"]

    if not played_rounds:
        st.info("Aún no hay rondas completadas.")
    else:
        round_sel = st.selectbox(
            "Selecciona una ronda",
            played_rounds,
            format_func=lambda r: ROUND_LABELS.get(r, r.capitalize())
        )

        # Build round leaderboard
        round_lb = []
        for u_data in leaderboard:
            rs = u_data["round_scores"]
            score = rs[round_sel]["score"] if round_sel in rs else 0
            bd = rs[round_sel]["breakdown"] if round_sel in rs else []
            round_lb.append({"display": u_data["display"], "username": u_data["username"], "score": score, "breakdown": bd})

        round_lb.sort(key=lambda x: x["score"], reverse=True)

        st.markdown(f"#### {ROUND_LABELS.get(round_sel, round_sel)} — Ranking")

        for i, u in enumerate(round_lb):
            medal = TROPHY_EMOJIS[i] if i < 3 else f"#{i+1}"
            is_me = u["username"] == st.session_state.username
            label = f"{medal} {u['display']}{' (tú)' if is_me else ''} · {u['score']} pts"

            with st.expander(label, expanded=False):
                if u["breakdown"]:
                    df = pd.DataFrame(u["breakdown"])
                    st.table(df)
                else:
                    st.markdown("0 puntos en esta ronda.")

with tab_preds:
    st.markdown("#### 🔮 Predicciones bloqueadas")

    window = get_current_window()
    available_windows = ["P1", "P2", "P3", "P4", "P5"]
    results = get_results()

    user_sel = st.selectbox(
        "Ver predicción de:",
        [u["username"] for u in leaderboard],
        format_func=lambda u: u.capitalize()
    )

    user_windows = [w for w in available_windows if is_prediction_locked(user_sel, w)]

    if not user_windows:
        st.info(f"{user_sel.capitalize()} aún no ha bloqueado ninguna predicción.")
    else:
        window_sel = st.selectbox("Ventana:", user_windows)
        pred = load_user_prediction(user_sel, window_sel)
        if pred:
            st.markdown(f"**Bracket de {user_sel.capitalize()} · Ventana {window_sel}**")
            render_bracket_view(pred, results)
        else:
            st.info("No se encontró predicción.")

with tab_duel:
    st.markdown("#### ⚔️ Duelo cabeza a cabeza")
    st.markdown("Compara tus predicciones con las de otro jugador ronda a ronda.")

    other_users = [u["username"] for u in leaderboard if u["username"] != st.session_state.username]
    if not other_users:
        st.info("No hay otros jugadores con los que comparar.")
    else:
        rival = st.selectbox("Elige tu rival:", other_users, format_func=lambda u: u.capitalize())
        results = get_results()
        window = get_current_window()

        my_windows = [w for w in ["P1","P2","P3","P4","P5"] if is_prediction_locked(st.session_state.username, w)]
        rival_windows = [w for w in ["P1","P2","P3","P4","P5"] if is_prediction_locked(rival, w)]
        common_windows = [w for w in my_windows if w in rival_windows]

        if not common_windows:
            st.info("Ninguno de los dos tiene predicciones bloqueadas para comparar.")
        else:
            w_sel = st.selectbox("Ventana a comparar:", common_windows)
            my_pred = load_user_prediction(st.session_state.username, w_sel)
            rival_pred = load_user_prediction(rival, w_sel)

            if my_pred and rival_pred:
                my_score, _ = calculate_user_score(st.session_state.username)
                rival_score, _ = calculate_user_score(rival)

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"<h4 style='text-align:center; color:#FFD700 !important;'>👤 {st.session_state.username.capitalize()}<br><span style='font-size:1.4rem;'>{my_score} pts</span></h4>", unsafe_allow_html=True)
                    render_bracket_view(my_pred, results)
                with col2:
                    st.markdown(f"<h4 style='text-align:center; color:#FFD700 !important;'>👤 {rival.capitalize()}<br><span style='font-size:1.4rem;'>{rival_score} pts</span></h4>", unsafe_allow_html=True)
                    render_bracket_view(rival_pred, results)

                # Coincidences
                st.markdown("---")
                st.markdown("#### 🤝 Coincidencias")
                total_matches = 0
                total_agree = 0
                for ronda in ROUNDS:
                    my_teams = set(my_pred.get(ronda, []))
                    rival_teams = set(rival_pred.get(ronda, []))
                    if my_teams or rival_teams:
                        agree = my_teams & rival_teams
                        total_matches += max(len(my_teams), len(rival_teams))
                        total_agree += len(agree)
                        if agree:
                            teams_str = " · ".join([f"{FLAGS.get(t,'🏳️')} {t}" for t in sorted(agree)])
                            st.markdown(f"**{ROUND_LABELS.get(ronda,ronda)}:** {teams_str}")

                if total_matches > 0:
                    pct = round(100 * total_agree / total_matches)
                    st.metric("Coincidencia total", f"{pct}%", f"{total_agree} equipos en común")
