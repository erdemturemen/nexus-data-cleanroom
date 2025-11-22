-- M1: Canonical Fields Table
-- NEXUS standart veri alanları

CREATE TABLE IF NOT EXISTS canonical_fields (
    id SERIAL PRIMARY KEY,
    canonical_name VARCHAR(100) UNIQUE NOT NULL,
    data_type VARCHAR(50) NOT NULL,
    description TEXT,
    is_required BOOLEAN DEFAULT false,
    category VARCHAR(50),
    validation_rule JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_canonical_name ON canonical_fields(canonical_name);
CREATE INDEX idx_category ON canonical_fields(category);

COMMENT ON TABLE canonical_fields IS 'NEXUS standart veri şeması';
