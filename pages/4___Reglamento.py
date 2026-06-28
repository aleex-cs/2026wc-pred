# pages/4___Reglamento.py
import streamlit as st
from styles import inject_custom_styles

st.set_page_config(
    page_title="Reglamento - Mundial 2026",
    layout="wide",
    page_icon="📋",
    initial_sidebar_state="collapsed"
)

inject_custom_styles()

# Header
st.markdown("""
<div style="text-align:center; padding: 40px 0 30px 0;">
    <div style="font-size:4rem; margin-bottom:16px;">📋</div>
    <h1 style="font-size:2.5rem; font-weight:800; background:linear-gradient(135deg,#FFD700,#FFA500); -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin:0;">Sistema de Puntuación</h1>
    <p style="color:#8892a4; margin-top:8px; font-size:1rem;">Bracket Dinámico - Mundial 2026</p>
</div>
""", unsafe_allow_html=True)

# Filosofía
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(255,215,0,0.08), rgba(255,165,0,0.04)); border: 1px solid rgba(255,215,0,0.2); border-radius: 12px; padding: 24px;">
        <h3 style="color:#FFD700; margin-top:0; font-size:1.2rem;">🎯 Visión a Largo Plazo</h3>
        <p style="color:#c8cdd8; margin:0; font-size:0.9rem;">Premia con la máxima puntuación a quienes anticipan los resultados desde el primer día (máximo riesgo).</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(255,215,0,0.08), rgba(255,165,0,0.04)); border: 1px solid rgba(255,215,0,0.2); border-radius: 12px; padding: 24px;">
        <h3 style="color:#FFD700; margin-top:0; font-size:1.2rem;">🔄 Capacidad de Adaptación</h3>
        <p style="color:#c8cdd8; margin:0; font-size:0.9rem;">Permite reengancharse en cada ronda con información actualizada, aunque con menor multiplicador.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Puntos Base
st.markdown("<h2 style='color:#fff; font-size:1.4rem;'>Puntos Base por Ronda</h2>", unsafe_allow_html=True)
st.markdown("""
<div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:12px; margin: 16px 0;">
    <div style="background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.1); border-radius: 10px; padding: 16px; text-align:center;">
        <div style="font-size:1.5rem; font-weight:700; color:#FFD700;">10 pts</div>
        <div style="color:#8892a4; font-size:0.85rem; margin-top:4px;">Dieciseisavos</div>
    </div>
    <div style="background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.1); border-radius: 10px; padding: 16px; text-align:center;">
        <div style="font-size:1.5rem; font-weight:700; color:#FFD700;">20 pts</div>
        <div style="color:#8892a4; font-size:0.85rem; margin-top:4px;">Octavos</div>
    </div>
    <div style="background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.1); border-radius: 10px; padding: 16px; text-align:center;">
        <div style="font-size:1.5rem; font-weight:700; color:#FFD700;">40 pts</div>
        <div style="color:#8892a4; font-size:0.85rem; margin-top:4px;">Cuartos</div>
    </div>
    <div style="background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.1); border-radius: 10px; padding: 16px; text-align:center;">
        <div style="font-size:1.5rem; font-weight:700; color:#FFD700;">80 pts</div>
        <div style="color:#8892a4; font-size:0.85rem; margin-top:4px;">Semifinales</div>
    </div>
    <div style="background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.1); border-radius: 10px; padding: 16px; text-align:center;">
        <div style="font-size:1.5rem; font-weight:700; color:#FFD700;">150 pts</div>
        <div style="color:#8892a4; font-size:0.85rem; margin-top:4px;">Finalista</div>
    </div>
    <div style="background: linear-gradient(135deg, rgba(255,215,0,0.15), rgba(255,165,0,0.08)); border: 1px solid rgba(255,215,0,0.4); border-radius: 10px; padding: 16px; text-align:center;">
        <div style="font-size:1.5rem; font-weight:700; color:#FFD700;">300 pts</div>
        <div style="color:#8892a4; font-size:0.85rem; margin-top:4px;">🏆 Campeón</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Multiplicadores
st.markdown("<h2 style='color:#fff; font-size:1.4rem;'>Multiplicadores de Anticipación</h2>", unsafe_allow_html=True)
st.markdown("""
<div style="display:grid; grid-template-columns: repeat(5, 1fr); gap:10px; margin: 16px 0;">
    <div style="background: linear-gradient(135deg, rgba(255,215,0,0.2), rgba(255,165,0,0.1)); border: 2px solid rgba(255,215,0,0.5); border-radius: 10px; padding: 14px; text-align:center;">
        <div style="font-size:1.8rem; font-weight:800; color:#FFD700;">×4</div>
        <div style="color:#fff; font-size:0.8rem; font-weight:600; margin-top:4px;">P1</div>
        <div style="color:#8892a4; font-size:0.75rem; margin-top:2px;">Inicio</div>
    </div>
    <div style="background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.15); border-radius: 10px; padding: 14px; text-align:center;">
        <div style="font-size:1.8rem; font-weight:800; color:#FFD700;">×3</div>
        <div style="color:#fff; font-size:0.8rem; font-weight:600; margin-top:4px;">P2</div>
        <div style="color:#8892a4; font-size:0.75rem; margin-top:2px;">Octavos</div>
    </div>
    <div style="background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.15); border-radius: 10px; padding: 14px; text-align:center;">
        <div style="font-size:1.8rem; font-weight:800; color:#FFD700;">×2</div>
        <div style="color:#fff; font-size:0.8rem; font-weight:600; margin-top:4px;">P3</div>
        <div style="color:#8892a4; font-size:0.75rem; margin-top:2px;">Cuartos</div>
    </div>
    <div style="background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.15); border-radius: 10px; padding: 14px; text-align:center;">
        <div style="font-size:1.8rem; font-weight:800; color:#FFD700;">×1.5</div>
        <div style="color:#fff; font-size:0.8rem; font-weight:600; margin-top:4px;">P4</div>
        <div style="color:#8892a4; font-size:0.75rem; margin-top:2px;">Semis</div>
    </div>
    <div style="background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.15); border-radius: 10px; padding: 14px; text-align:center;">
        <div style="font-size:1.8rem; font-weight:800; color:#FFD700;">×1</div>
        <div style="color:#fff; font-size:0.8rem; font-weight:600; margin-top:4px;">P5</div>
        <div style="color:#8892a4; font-size:0.75rem; margin-top:2px;">Final</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Matriz
st.markdown("<h2 style='color:#fff; font-size:1.4rem;'>Matriz de Puntuación</h2>", unsafe_allow_html=True)
st.markdown("""
<div style="overflow-x:auto; margin: 16px 0;">
    <table style="width:100%; border-collapse:collapse; background:rgba(255,255,255,0.02); border-radius:12px; overflow:hidden;">
        <thead>
            <tr style="background:rgba(255,215,0,0.15);">
                <th style="padding:12px 16px; text-align:left; color:#FFD700; font-weight:700; font-size:0.85rem; border-bottom:1px solid rgba(255,215,0,0.2);">Logro</th>
                <th style="padding:12px 16px; text-align:center; color:#FFD700; font-weight:700; font-size:0.85rem; border-bottom:1px solid rgba(255,215,0,0.2;">P1 (×4)</th>
                <th style="padding:12px 16px; text-align:center; color:#FFD700; font-weight:700; font-size:0.85rem; border-bottom:1px solid rgba(255,215,0,0.2;">P2 (×3)</th>
                <th style="padding:12px 16px; text-align:center; color:#FFD700; font-weight:700; font-size:0.85rem; border-bottom:1px solid rgba(255,215,0,0.2;">P3 (×2)</th>
                <th style="padding:12px 16px; text-align:center; color:#FFD700; font-weight:700; font-size:0.85rem; border-bottom:1px solid rgba(255,215,0,0.2;">P4 (×1.5)</th>
                <th style="padding:12px 16px; text-align:center; color:#FFD700; font-weight:700; font-size:0.85rem; border-bottom:1px solid rgba(255,215,0,0.2;">P5 (×1)</th>
            </tr>
        </thead>
        <tbody>
            <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
                <td style="padding:12px 16px; color:#c8cdd8; font-size:0.9rem;">1/16</td>
                <td style="padding:12px 16px; text-align:center; color:#FFD700; font-weight:600; font-size:0.95rem;">40</td>
                <td style="padding:12px 16px; text-align:center; color:#555; font-size:0.85rem;">—</td>
                <td style="padding:12px 16px; text-align:center; color:#555; font-size:0.85rem;">—</td>
                <td style="padding:12px 16px; text-align:center; color:#555; font-size:0.85rem;">—</td>
                <td style="padding:12px 16px; text-align:center; color:#555; font-size:0.85rem;">—</td>
            </tr>
            <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
                <td style="padding:12px 16px; color:#c8cdd8; font-size:0.9rem;">1/8</td>
                <td style="padding:12px 16px; text-align:center; color:#FFD700; font-weight:600; font-size:0.95rem;">80</td>
                <td style="padding:12px 16px; text-align:center; color:#FFD700; font-weight:600; font-size:0.95rem;">60</td>
                <td style="padding:12px 16px; text-align:center; color:#555; font-size:0.85rem;">—</td>
                <td style="padding:12px 16px; text-align:center; color:#555; font-size:0.85rem;">—</td>
                <td style="padding:12px 16px; text-align:center; color:#555; font-size:0.85rem;">—</td>
            </tr>
            <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
                <td style="padding:12px 16px; color:#c8cdd8; font-size:0.9rem;">1/4</td>
                <td style="padding:12px 16px; text-align:center; color:#FFD700; font-weight:600; font-size:0.95rem;">160</td>
                <td style="padding:12px 16px; text-align:center; color:#FFD700; font-weight:600; font-size:0.95rem;">120</td>
                <td style="padding:12px 16px; text-align:center; color:#FFD700; font-weight:600; font-size:0.95rem;">80</td>
                <td style="padding:12px 16px; text-align:center; color:#555; font-size:0.85rem;">—</td>
                <td style="padding:12px 16px; text-align:center; color:#555; font-size:0.85rem;">—</td>
            </tr>
            <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
                <td style="padding:12px 16px; color:#c8cdd8; font-size:0.9rem;">Semifinalista</td>
                <td style="padding:12px 16px; text-align:center; color:#FFD700; font-weight:600; font-size:0.95rem;">320</td>
                <td style="padding:12px 16px; text-align:center; color:#FFD700; font-weight:600; font-size:0.95rem;">240</td>
                <td style="padding:12px 16px; text-align:center; color:#FFD700; font-weight:600; font-size:0.95rem;">160</td>
                <td style="padding:12px 16px; text-align:center; color:#FFD700; font-weight:600; font-size:0.95rem;">120</td>
                <td style="padding:12px 16px; text-align:center; color:#555; font-size:0.85rem;">—</td>
            </tr>
            <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
                <td style="padding:12px 16px; color:#c8cdd8; font-size:0.9rem;">Finalista</td>
                <td style="padding:12px 16px; text-align:center; color:#FFD700; font-weight:600; font-size:0.95rem;">600</td>
                <td style="padding:12px 16px; text-align:center; color:#FFD700; font-weight:600; font-size:0.95rem;">450</td>
                <td style="padding:12px 16px; text-align:center; color:#FFD700; font-weight:600; font-size:0.95rem;">300</td>
                <td style="padding:12px 16px; text-align:center; color:#FFD700; font-weight:600; font-size:0.95rem;">225</td>
                <td style="padding:12px 16px; text-align:center; color:#FFD700; font-weight:600; font-size:0.95rem;">150</td>
            </tr>
            <tr style="background:rgba(255,215,0,0.08);">
                <td style="padding:12px 16px; color:#FFD700; font-weight:700; font-size:0.9rem;">🏆 Campeón</td>
                <td style="padding:12px 16px; text-align:center; color:#FFD700; font-weight:700; font-size:1rem;">1200</td>
                <td style="padding:12px 16px; text-align:center; color:#FFD700; font-weight:600; font-size:0.95rem;">900</td>
                <td style="padding:12px 16px; text-align:center; color:#FFD700; font-weight:600; font-size:0.95rem;">600</td>
                <td style="padding:12px 16px; text-align:center; color:#FFD700; font-weight:600; font-size:0.95rem;">450</td>
                <td style="padding:12px 16px; text-align:center; color:#FFD700; font-weight:600; font-size:0.95rem;">300</td>
            </tr>
        </tbody>
    </table>
</div>
""", unsafe_allow_html=True)

# Regla crítica
st.markdown("""
<div style="background: rgba(255,100,100,0.1); border: 1px solid rgba(255,100,100,0.3); border-radius: 12px; padding: 20px; margin: 20px 0;">
    <h3 style="color:#ff6b6b; margin-top:0; font-size:1.1rem;">⚠️ Regla Crítica: No-Duplicidad de Puntos</h3>
    <p style="color:#c8cdd8; margin:8px 0 0 0; font-size:0.9rem;">Los puntos por acertar un equipo en una posición específica no son acumulables entre las diferentes ventanas de predicción. Solo otorga puntuación la versión activa más reciente en la que mantuviste el acierto.</p>
    <p style="color:#8892a4; margin:8px 0 0 0; font-size:0.85rem;"><strong>Ejemplo:</strong> Si seleccionas a un país como Campeón en P1 y mantienes esa selección sin cambios hasta la final, obtendrás 1,200 puntos. Si modificas tu predicción en P3, renuncias al multiplicador de P1 y P2 para dicho logro.</p>
</div>
""", unsafe_allow_html=True)

# Ventajas
st.markdown("<h2 style='color:#fff; font-size:1.4rem;'>Ventajas del Modelo</h2>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div style="background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.1); border-radius: 10px; padding: 20px;">
        <div style="font-size:2rem; margin-bottom:8px;">🎲</div>
        <h4 style="color:#FFD700; margin:0 0 8px 0; font-size:0.95rem;">Riesgo Inicial</h4>
        <p style="color:#8892a4; margin:0; font-size:0.8rem;">Diferencia de 4 a 1 (1200 vs 300 pts) recompensa el análisis a largo plazo.</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div style="background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.1); border-radius: 10px; padding: 20px;">
        <div style="font-size:2rem; margin-bottom:8px;">👥</div>
        <h4 style="color:#FFD700; margin:0 0 8px 0; font-size:0.95rem;">Retención</h4>
        <p style="color:#8892a4; margin:0; font-size:0.8rem;">Evita la deserción temprana permitiendo ajustar estrategias en fases avanzadas.</p>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div style="background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.1); border-radius: 10px; padding: 20px;">
        <div style="font-size:2rem; margin-bottom:8px;">📈</div>
        <h4 style="color:#FFD700; margin:0 0 8px 0; font-size:0.95rem;">Escalabilidad</h4>
        <p style="color:#8892a4; margin:0; font-size:0.8rem;">Progresión geométrica acompaña la dificultad real de cada fase eliminatoria.</p>
    </div>
    """, unsafe_allow_html=True)
