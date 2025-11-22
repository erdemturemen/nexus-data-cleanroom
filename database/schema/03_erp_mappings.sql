-- M1: ERP Mappings Table
-- ERP kolon → Canonical alan eşleştirmeleri

CREATE TABLE IF NOT EXISTS erp_mappings (
    id SERIAL PRIMARY KEY,
    erp_code VARCHAR(50) REFERENCES erp_systems(erp_code) ON DELETE CASCADE,
    table_name VARCHAR(200) NOT NULL,
    column_name VARCHAR(200) NOT NULL,
    canonical_name VARCHAR(100) REFERENCES canonical_fields(canonical_name),
    transform_expression TEXT,
    confidence_score DECIMAL(3,2) CHECK (confidence_score BETWEEN 0 AND 1),
    mapping_source VARCHAR(50),
    created_by VARCHAR(100),
    approved_by VARCHAR(100),
    approved_at TIMESTAMP,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(erp_code, table_name, column_name)
);

CREATE INDEX idx_erp_mappings_erp ON erp_mappings(erp_code);
CREATE INDEX idx_erp_mappings_canonical ON erp_mappings(canonical_name);
CREATE INDEX idx_erp_mappings_confidence ON erp_mappings(confidence_score);
