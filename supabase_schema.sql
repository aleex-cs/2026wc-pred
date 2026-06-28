-- Tabla de usuarios (ya existe, usada por auth.py)
-- Si no existe, créala manualmente:
-- CREATE TABLE users (
--     id SERIAL PRIMARY KEY,
--     username VARCHAR(100) UNIQUE NOT NULL,
--     password_hash VARCHAR(255) NOT NULL,
--     created_at TIMESTAMP DEFAULT NOW()
-- );

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
    prediction_window VARCHAR(10) NOT NULL, -- P1, P2, P3, P4, P5
    ronda VARCHAR(50) NOT NULL,
    equipos JSONB NOT NULL, -- Array de equipos predichos para esa ronda
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
