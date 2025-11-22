"""
M3: Feature Extraction - Kolon profili veri yapısı
"""
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class ColumnProfile:
    """Bir ERP kolonunun tüm özellikleri"""
    erp_code: str
    table_name: str
    column_name: str
    data_type: str
    inferred_semantic_type: str
    null_ratio: float
    distinct_ratio: float
    sample_values: List[str]
    patterns: List[str]
    min_length: int
    max_length: int
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    mean: Optional[float] = None
    
    def to_text_description(self) -> str:
        """LLM için metin açıklaması"""
        desc = f"ERP: {self.erp_code}, Table: {self.table_name}, Column: {self.column_name}\n"
        desc += f"Data Type: {self.data_type}, Semantic Type: {self.inferred_semantic_type}\n"
        desc += f"Sample Values: {', '.join(self.sample_values[:5])}\n"
        desc += f"Null Ratio: {self.null_ratio:.2%}, Distinct Ratio: {self.distinct_ratio:.2%}\n"
        if self.patterns:
            desc += f"Patterns: {', '.join(self.patterns)}\n"
        return desc
