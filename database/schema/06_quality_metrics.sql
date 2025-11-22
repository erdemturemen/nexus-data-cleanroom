-- M1: Mapping Quality Metrics Table

CREATE TABLE IF NOT EXISTS mapping_quality_metrics (
    id SERIAL PRIMARY KEY,
    erp_code VARCHAR(50),
    analysis_date DATE DEFAULT CURRENT_DATE,
    total_columns INT NOT NULL,
    auto_mapped INT DEFAULT 0,
    human_reviewed INT DEFAULT 0,
    manual_required INT DEFAULT 0,
    avg_confidence DECIMAL(3,2),
    processing_time_seconds INT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_quality_metrics_erp ON mapping_quality_metrics(erp_code);
CREATE INDEX idx_quality_metrics_date ON mapping_quality_metrics(analysis_date);
