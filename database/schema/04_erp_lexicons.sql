-- M1: ERP Lexicons Table
-- ERP-specific sözlük (hızlı lookup)

CREATE TABLE IF NOT EXISTS erp_lexicons (
    id SERIAL PRIMARY KEY,
    erp_code VARCHAR(50) REFERENCES erp_systems(erp_code) ON DELETE CASCADE,
    table_name VARCHAR(200) NOT NULL,
    column_name VARCHAR(200) NOT NULL,
    canonical_name VARCHAR(100) NOT NULL,
    confidence DECIMAL(3,2) DEFAULT 0.95,
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(erp_code, table_name, column_name)
);

CREATE INDEX idx_lexicon_lookup ON erp_lexicons(erp_code, table_name, column_name);
