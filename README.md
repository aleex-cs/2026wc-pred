# 2026 World Cup Bracket Predictor

Aplicación web de predicciones para el Mundial 2026 con sistema de puntuación dinámico. Los usuarios pueden crear sus brackets antes de cada fase eliminatoria y ganar puntos según la anticipación de sus predicciones.

## 🎯 Características

- **Sistema de puntuación dinámico**: Multiplicadores que varían según la ventana de predicción (P1-P5)
- **Bracket interactivo**: Interfaz visual para seleccionar ganadores de cada partido
- **Panel de administración**: Control de ventanas de predicción y carga de resultados
- **Clasificación en tiempo real**: Ranking de jugadores con desglose de puntos
- **Base de datos en la nube**: Integración con Supabase para persistencia de datos
- **Diseño moderno**: UI oscura con acentos dorados

## 📊 Sistema de Puntuación

### Puntos Base por Ronda
- Dieciseisavos: 10 pts
- Octavos: 20 pts
- Cuartos: 40 pts
- Semifinales: 80 pts
- Finalista: 150 pts
- Campeón: 300 pts

### Multiplicadores de Anticipación
- **P1 (Inicio)**: ×4 - Bracket inicial perfecto
- **P2 (Octavos)**: ×3 - Tras ver la fase de grupos
- **P3 (Cuartos)**: ×2 - Panorama claro
- **P4 (Semis)**: ×1.5 - Fase final de 4 equipos
- **P5 (Final)**: ×1 - Predicción directa a partido único

### Regla Crítica
Los puntos no son acumulables entre ventanas. Solo cuenta la versión más reciente de la predicción. Si modificas tu predicción, pierdes los multiplicadores de ventanas anteriores.

## 🚀 Instalación

### Requisitos previos
- Python 3.8+
- Cuenta en [Supabase](https://supabase.com)

### 1. Clonar el repositorio
```bash
git clone https://github.com/aleex-cs/2026wc-pred.git
cd 2026wc-pred
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar Supabase

1. Crea un proyecto en [supabase.com](https://supabase.com)
2. Ve a Settings → API y copia tu `Project URL` y `anon public key`
3. Crea el archivo `.streamlit/secrets.toml`:
```toml
SUPABASE_URL = "tu_url_del_proyecto"
SUPABASE_KEY = "tu_anon_key"
ADMIN_PASSWORD = "tu_contraseña_admin"
```

### 4. Configurar la base de datos

Ejecuta el siguiente SQL en el SQL Editor de Supabase:

```sql
-- Tabla de resultados del torneo
CREATE TABLE results (
    id SERIAL PRIMARY KEY,
    ronda VARCHAR(50) NOT NULL,
    equipo VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Tabla de predicciones de usuarios
CREATE TABLE predictions (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    prediction_window VARCHAR(10) NOT NULL,
    ronda VARCHAR(50) NOT NULL,
    equipos JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(username, prediction_window)
);

-- Tabla de locks de predicciones
CREATE TABLE prediction_locks (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    prediction_window VARCHAR(10) NOT NULL,
    locked_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(username, prediction_window)
);

-- Tabla de estado de ventanas (control de admin)
CREATE TABLE windows_state (
    prediction_window VARCHAR(10) PRIMARY KEY,
    enabled BOOLEAN DEFAULT TRUE,
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Insertar estado inicial de ventanas
INSERT INTO windows_state (prediction_window, enabled) VALUES
    ('P1', true),
    ('P2', true),
    ('P3', true),
    ('P4', true),
    ('P5', true)
ON CONFLICT (prediction_window) DO NOTHING;

-- Índices para mejor rendimiento
CREATE INDEX idx_results_ronda ON results(ronda);
CREATE INDEX idx_predictions_username ON predictions(username);
CREATE INDEX idx_predictions_window ON predictions(prediction_window);
CREATE INDEX idx_prediction_locks_username ON prediction_locks(username);
```

### 5. Ejecutar la aplicación
```bash
streamlit run app.py
```

## 👥 Uso

### Para jugadores

1. **Crear cuenta**: Regístrate con un nombre de usuario y contraseña
2. **Hacer predicciones**: Ve a "Mi Predicción" y selecciona los ganadores de cada partido
3. **Bloquear predicción**: Una vez completado el bracket, confírmalo para bloquearlo
4. **Ver clasificación**: Consulta el ranking y tus puntos en "Clasificación"
5. **Consultar reglamento**: Revisa el sistema de puntuación en "Reglamento"

### Para administradores

1. **Iniciar sesión como admin**: Usa el usuario "admin" con la contraseña configurada
2. **Cargar resultados**: En el panel de Admin, carga los equipos clasificados de cada ronda
3. **Controlar ventanas**: Activa/desactiva las ventanas de predicción según la fase del torneo
4. **Gestionar usuarios**: Ver todos los usuarios registrados y sus predicciones bloqueadas

## 📁 Estructura del proyecto

```
worldcup_app/
├── app.py                 # Página principal
├── auth.py                # Sistema de autenticación
├── config.py              # Configuración del torneo
├── data_manager.py        # Gestión de datos (Supabase)
├── scoring.py             # Cálculo de puntuaciones
├── styles.py              # Estilos CSS personalizados
├── requirements.txt       # Dependencias de Python
├── pages/
│   ├── 1___Predicción.py  # Página de predicciones
│   ├── 2___Clasificación.py # Página de clasificación
│   ├── 3___Admin.py       # Panel de administración
│   └── 4___Reglamento.py  # Reglamento de puntuación
└── .streamlit/
    └── secrets.toml        # Credenciales de Supabase
```

## 🔧 Configuración

### Ventanas de predicción

Las ventanas se activan automáticamente según los resultados cargados:
- **P1**: Antes de que haya resultados de dieciseisavos
- **P2**: Después de cargar resultados de dieciseisavos
- **P3**: Después de cargar resultados de octavos
- **P4**: Después de cargar resultados de cuartos
- **P5**: Después de cargar resultados de semifinales

El admin puede manualmente activar/desactivar cualquier ventana desde el panel de administración.

## 🏆 Equipos participantes

El torneo incluye 32 equipos divididos en emparejamientos de dieciseisavos:

**Lado izquierdo**: Alemania, Paraguay, Francia, Suecia, Sudáfrica, Canadá, Países Bajos, Marruecos, Portugal, Croacia, España, Austria, Estados Unidos, Bosnia y H., Bélgica, Senegal

**Lado derecho**: Brasil, Japón, Costa de Marfil, Noruega, México, Ecuador, Inglaterra, RD Congo, Argentina, Cabo Verde, Australia, Egipto, Suiza, Argelia, Colombia, Ghana

## 📝 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Si encuentras un bug o tienes una sugerencia, abre un issue en el repositorio.

## 📧 Contacto

Para cualquier pregunta, contacta a través del repositorio de GitHub.
