-- Migración para resultados partido por partido

-- Eliminar tabla antigua
DROP TABLE IF EXISTS results;

-- Nueva tabla de resultados por partido
CREATE TABLE match_results (
    id SERIAL PRIMARY KEY,
    ronda VARCHAR(50) NOT NULL,
    equipo_local VARCHAR(100) NOT NULL,
    equipo_visitante VARCHAR(100) NOT NULL,
    ganador VARCHAR(100) NOT NULL,
    partido_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(ronda, partido_id)
);

-- Índices
CREATE INDEX idx_match_results_ronda ON match_results(ronda);
CREATE INDEX idx_match_results_ganador ON match_results(ganador);
