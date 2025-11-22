-- M1: Data Quality Rules Table

CREATE TABLE IF NOT EXISTS data_quality_rules (
    id SERIAL PRIMARY KEY,
    rule_name VARCHAR(100) UNIQUE NOT NULL,
    rule_type VARCHAR(50) NOT NULL,
    canonical_field VARCHAR(100),
    condition_json JSONB NOT NULL,
    severity VARCHAR(20) CHECK (severity IN ('error', 'warning', 'info')),
    auto_fix BOOLEAN DEFAULT false,
    fix_expression TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_quality_rules_type ON data_quality_rules(rule_type);
CREATE INDEX idx_quality_rules_active ON data_quality_rules(is_active);
