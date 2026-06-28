# styles.py
import streamlit as st

def inject_custom_styles():
    st.markdown("""
    <style>
    /* ── Base & Typography ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Bebas+Neue&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Hide default Streamlit header/footer/menu */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    [data-testid="stHeader"] { background: transparent !important; }
    [data-testid="stSidebarNav"] { display: none !important; }
    .stAppDeployButton { display: none !important; }

    /* ── Background ── */
    .stApp {
        background: linear-gradient(135deg, #0a0e1a 0%, #0d1b2a 50%, #0a1628 100%);
        min-height: 100vh;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: rgba(10, 14, 26, 0.95) !important;
        border-right: 1px solid rgba(255, 215, 0, 0.15);
    }
    [data-testid="stSidebar"] * {
        color: #e8eaf0 !important;
    }

    /* ── Cards / Containers ── */
    [data-testid="stVerticalBlockBorderWrapper"] > div {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,215,0,0.12) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(8px);
        transition: border-color 0.2s ease;
    }
    [data-testid="stVerticalBlockBorderWrapper"] > div:hover {
        border-color: rgba(255,215,0,0.25) !important;
    }

    /* ── Buttons ── */
    .stButton > button {
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        letter-spacing: 0.02em !important;
        transition: all 0.15s ease !important;
        border: none !important;
    }
    .stButton > button[kind="primary"], button[kind="primaryFormSubmit"] {
        background: linear-gradient(135deg, #FFD700, #FFA500) !important;
        color: #0a0e1a !important;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3) !important;
        border: none !important;
    }
    .stButton > button[kind="primary"]:hover, button[kind="primaryFormSubmit"]:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(255, 215, 0, 0.45) !important;
    }
    .stButton > button[kind="primary"] *, button[kind="primaryFormSubmit"] * {
        color: #0a0e1a !important;
    }
    .stButton > button[kind="secondary"] {
        background: rgba(255,255,255,0.06) !important;
        color: #c8cdd8 !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
    }
    .stButton > button[kind="secondary"]:hover {
        background: rgba(255,255,255,0.1) !important;
        color: #ffffff !important;
        border-color: rgba(255,215,0,0.3) !important;
    }

    /* ── Inputs ── */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea,
    [data-baseweb="select"] > div {
        background: #1a1e2e !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        border-radius: 8px !important;
        color: #ffffff !important;
    }
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: rgba(255,215,0,0.5) !important;
        box-shadow: 0 0 0 2px rgba(255,215,0,0.1) !important;
    }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        background: transparent !important;
        gap: 4px;
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border-radius: 8px 8px 0 0 !important;
        color: #8892a4 !important;
        font-weight: 500 !important;
        padding: 8px 20px !important;
        transition: all 0.15s;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(255,215,0,0.1) !important;
        color: #FFD700 !important;
        border-bottom: 2px solid #FFD700 !important;
    }

    /* ── Headings ── */
    h1, h2, h3 {
        color: #ffffff !important;
        font-weight: 700 !important;
    }
    h1 { letter-spacing: -0.02em; }

    /* ── Text ── */
    p, .stMarkdown p, label, span {
        color: #c8cdd8 !important;
    }

    /* ── Alerts ── */
    [data-testid="stAlert"] {
        border-radius: 10px !important;
    }

    /* ── Expander ── */
    [data-testid="stExpander"] {
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 10px !important;
    }
    [data-testid="stExpander"] summary {
        color: #FFD700 !important;
        font-weight: 600 !important;
        background: transparent !important;
    }

    /* ── Multiselect ── */
    [data-baseweb="select"], [data-baseweb="select"] > div {
        background: #1a1e2e !important;
        border-radius: 8px !important;
        color: #ffffff !important;
    }

    /* ── Tables ── */
    .stTable table {
        background: transparent !important;
    }
    .stTable th {
        background: rgba(255,215,0,0.1) !important;
        color: #FFD700 !important;
        font-weight: 700 !important;
        border: none !important;
        padding: 10px 16px !important;
    }
    .stTable td {
        color: #c8cdd8 !important;
        border-color: rgba(255,255,255,0.06) !important;
        padding: 8px 16px !important;
    }
    .stTable tr:hover td {
        background: rgba(255,215,0,0.05) !important;
    }

    /* ── Progress / metric ── */
    [data-testid="metric-container"] {
        background: rgba(255,255,255,0.04);
        border-radius: 12px;
        padding: 12px 16px;
        border: 1px solid rgba(255,255,255,0.08);
    }

    /* ── Bracket specific ── */
    .bracket-match {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 10px;
        padding: 4px;
        margin-bottom: 8px;
    }
    .bracket-winner {
        border-color: rgba(255,215,0,0.4) !important;
        background: rgba(255,215,0,0.06) !important;
    }

    /* ── Podium cards ── */
    .podium-gold {
        background: linear-gradient(135deg, rgba(255,215,0,0.15), rgba(255,165,0,0.08)) !important;
        border: 1px solid rgba(255,215,0,0.4) !important;
    }
    .podium-silver {
        background: linear-gradient(135deg, rgba(192,192,192,0.12), rgba(160,160,160,0.06)) !important;
        border: 1px solid rgba(192,192,192,0.3) !important;
    }
    .podium-bronze {
        background: linear-gradient(135deg, rgba(205,127,50,0.12), rgba(180,100,30,0.06)) !important;
        border: 1px solid rgba(205,127,50,0.3) !important;
    }

    /* Divider */
    hr { border-color: rgba(255,255,255,0.08) !important; }

    </style>
    """, unsafe_allow_html=True)

def render_bracket_view(prediction, results=None):
    """Render a prediction as a visual bracket using pure CSS Flexbox."""
    from config import ROUNDS, ROUND_LABELS, FLAGS, TEAMS_PER_ROUND, ROUND_OF_32_MATCHUPS
    import streamlit as st

    rounds_to_show = [r for r in ROUNDS if r != "campeon"]

    # 1. Build properly ordered teams based on the bracket structure
    ordered_teams_by_round = {}
    ordered_teams_by_round["dieciseisavos"] = [t for match in ROUND_OF_32_MATCHUPS for t in match]

    for i in range(1, len(ROUNDS)):
        prev = ROUNDS[i-1]
        curr = ROUNDS[i]
        candidates = ordered_teams_by_round[prev]
        
        winners = prediction.get(curr, [])
        if not winners:
            winners = (results or {}).get(curr, [])
            
        ordered_curr = [t for t in candidates if t in winners]
        
        # Fallback if any team wasn't in candidates
        for t in winners:
            if t not in ordered_curr:
                ordered_curr.append(t)
                
        ordered_teams_by_round[curr] = ordered_curr

    # 2. Build the HTML Bracket using Flexbox
    html = """
    <div style="display: flex; flex-direction: row; width: 100%; gap: 12px; overflow-x: auto; padding-bottom: 20px;">
    """

    for i, ronda in enumerate(rounds_to_show):
        teams = ordered_teams_by_round.get(ronda, [])
        label = ROUND_LABELS[ronda]

        # Inicia columna
        html += """
        <div style="flex: 1; min-width: 150px; display: flex; flex-direction: column;">
            <div style="text-align:center; font-size:0.7rem; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; color:#FFD700; margin-bottom:12px;">
                {label}
            </div>
            <div style="flex: 1; display: flex; flex-direction: column; justify-content: space-around;">
        """.format(label=label)

        if not teams:
            html += "<p style='text-align:center; font-size:0.75rem; color:#555;'>—</p>"
        else:
            # Agrupar de 2 en 2 para cada partido
            for j in range(0, len(teams), 2):
                html += """
                <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; padding: 6px; margin: 8px 0; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                """
                
                for team in teams[j:j+2]:
                    flag = FLAGS.get(team, "🏳️")
                    
                    next_ronda_idx = ROUNDS.index(ronda) + 1
                    is_predicted_winner = False
                    if next_ronda_idx < len(ROUNDS):
                        next_ronda = ROUNDS[next_ronda_idx]
                        is_predicted_winner = team in prediction.get(next_ronda, [])
                    
                    if is_predicted_winner:
                        bg = "rgba(255,215,0,0.15)"
                        border = "rgba(255,215,0,0.6)"
                        color = "#FFD700"
                    else:
                        bg = "rgba(255,255,255,0.04)"
                        border = "rgba(255,255,255,0.1)"
                        color = "#c8cdd8"

                    html += f"""
                    <div style="
                        background:{bg};
                        border:1px solid {border};
                        border-radius:6px;
                        padding:5px 8px;
                        margin-bottom:4px;
                        font-size:0.78rem;
                        font-weight:500;
                        color:{color};
                        display: flex;
                        align-items: center;
                        gap: 6px;
                        white-space:nowrap;
                        overflow:hidden;
                        text-overflow:ellipsis;
                    ">
                        <span>{flag}</span>
                        <span>{team}</span>
                    </div>
                    """
                
                # Quitar el margen del último equipo dentro de la tarjeta del partido
                html = html.rsplit('margin-bottom:4px;', 1)[0] + 'margin-bottom:0px;' + html.rsplit('margin-bottom:4px;', 1)[1]
                
                html += "</div>" # Fin del partido

        html += """
            </div>
        </div>
        """ # Fin de la columna

    html += "</div>" # Fin del contenedor principal

    # AÑADE ESTA LÍNEA PARA APLANAR EL HTML (Elimina saltos de línea y por ende la indentación)
    html = html.replace('\n', '') 

    # 3. Inyectar todo en Streamlit
    st.markdown(html, unsafe_allow_html=True)