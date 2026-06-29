# config.py

ROUNDS = ["dieciseisavos", "octavos", "cuartos", "semis", "final", "campeon"]
ROUND_LABELS = {
    "dieciseisavos": "Dieciseisavos",
    "octavos": "Octavos de Final",
    "cuartos": "Cuartos de Final",
    "semis": "Semifinales",
    "final": "Final",
    "campeon": "Campeón"
}
TEAMS_PER_ROUND = {"dieciseisavos": 32, "octavos": 16, "cuartos": 8, "semis": 4, "final": 2, "campeon": 1}

VALID_WINDOWS_FOR_ROUND = {
    "dieciseisavos": ["P1"],
    "octavos": ["P1", "P2"],
    "cuartos": ["P1", "P2", "P3"],
    "semis": ["P1", "P2", "P3", "P4"],
    "final": ["P1", "P2", "P3", "P4", "P5"],
    "campeon": ["P1", "P2", "P3", "P4", "P5"]
}

POINTS = {
    "dieciseisavos": {"P1": 40},
    "octavos": {"P1": 80, "P2": 60},
    "cuartos": {"P1": 160, "P2": 120, "P3": 80},
    "semis": {"P1": 320, "P2": 240, "P3": 160, "P4": 120},
    "final": {"P1": 600, "P2": 450, "P3": 300, "P4": 225, "P5": 150},
    "campeon": {"P1": 1200, "P2": 900, "P3": 600, "P4": 450, "P5": 300}
}

ROUND_OF_32_MATCHUPS = [
    # ---- LADO IZQUIERDO ----
    ("Alemania", "Paraguay"),
    ("Francia", "Suecia"),
    ("Sudáfrica", "Canadá"),
    ("Países Bajos", "Marruecos"),
    ("Portugal", "Croacia"),
    ("España", "Austria"),
    ("Estados Unidos", "Bosnia y H."),
    ("Bélgica", "Senegal"),
    # ---- LADO DERECHO ----
    ("Brasil", "Japón"),
    ("Costa de Marfil", "Noruega"),
    ("México", "Ecuador"),
    ("Inglaterra", "RD Congo"),
    ("Argentina", "Cabo Verde"),
    ("Australia", "Egipto"),
    ("Suiza", "Argelia"),
    ("Colombia", "Ghana")
]

# Emparejamientos dinámicos - se generan según los ganadores de la ronda anterior
# Estos son placeholders, los reales se generan dinámicamente
ROUND_MATCHUPS = {
    "dieciseisavos": ROUND_OF_32_MATCHUPS,
    "octavos": [],  # Se genera dinámicamente
    "cuartos": [],  # Se genera dinámicamente
    "semis": [],    # Se genera dinámicamente
    "final": [],    # Se genera dinámicamente
    "campeon": []   # Se genera dinámicamente
}

FLAGS = {
    "Sudáfrica": "🇿🇦", "Canadá": "🇨🇦",
    "Alemania": "🇩🇪", "Paraguay": "🇵🇾",
    "Países Bajos": "🇳🇱", "Marruecos": "🇲🇦",
    "Brasil": "🇧🇷", "Japón": "🇯🇵",
    "Francia": "🇫🇷", "Suecia": "🇸🇪",
    "Costa de Marfil": "🇨🇮", "Noruega": "🇳🇴",
    "México": "🇲🇽", "Ecuador": "🇪🇨",
    "Inglaterra": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "RD Congo": "🇨🇩",
    "Estados Unidos": "🇺🇸", "Bosnia y H.": "🇧🇦",
    "Bélgica": "🇧🇪", "Senegal": "🇸🇳",
    "Portugal": "🇵🇹", "Croacia": "🇭🇷",
    "España": "🇪🇸", "Austria": "🇦🇹",
    "Suiza": "🇨🇭", "Argelia": "🇩🇿",
    "Argentina": "🇦🇷", "Cabo Verde": "🇨🇻",
    "Colombia": "🇨🇴", "Ghana": "🇬🇭",
    "Australia": "🇦🇺", "Egipto": "🇪🇬"
}

TROPHY_EMOJIS = ["🥇", "🥈", "🥉"]
