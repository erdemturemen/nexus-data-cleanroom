-- M1: ERP Systems Table

CREATE TABLE IF NOT EXISTS erp_systems (
    id SERIAL PRIMARY KEY,
    erp_code VARCHAR(50) UNIQUE NOT NULL,
    erp_name VARCHAR(200) NOT NULL,
    vendor VARCHAR(100),
    version VARCHAR(50),
    connection_type VARCHAR(50),
    connection_config JSONB,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_erp_code ON erp_systems(erp_code);
CREATE INDEX idx_is_active ON erp_systems(is_active);
