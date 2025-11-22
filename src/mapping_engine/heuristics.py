"""
M3: Heuristic Mapper - ERP lexicon ve kurallar ile hızlı mapping
"""
from typing import Dict, Optional

class HeuristicMapper:
    """ERP lexicon ve kurallar ile hızlı mapping"""
    
    def __init__(self, db_session):
        self.db = db_session
        self.lexicons = self._load_lexicons()
    
    def _load_lexicons(self) -> Dict:
        """Database'den lexicon'ları yükle"""
        # TODO: Database'den yükle
        # Şimdilik hardcoded SAP lexicon
        return {
            ('SAP_S4', 'EKKO', 'EBELN'): {'canonical': 'po_id', 'confidence': 0.99},
            ('SAP_S4', 'EKKO', 'LIFNR'): {'canonical': 'vendor_id', 'confidence': 0.98},
            ('SAP_S4', 'EKKO', 'AEDAT'): {'canonical': 'timestamp', 'confidence': 0.95},
            ('SAP_S4', 'EKKO', 'WAERS'): {'canonical': 'currency', 'confidence': 0.99},
            ('SAP_S4', 'EKPO', 'MENGE'): {'canonical': 'quantity', 'confidence': 0.98},
            ('SAP_S4', 'EKPO', 'NETPR'): {'canonical': 'unit_price', 'confidence': 0.97},
        }
    
    def suggest_mapping(self, profile) -> Dict:
        """Heuristic ile mapping önerisi"""
        
        # 1. Lexicon kontrolü
        lexicon_result = self._check_lexicon(profile)
        if lexicon_result:
            return lexicon_result
        
        # 2. İsim kuralları
        name_result = self._check_name_rules(profile)
        if name_result['confidence'] > 0.6:
            return name_result
        
        # 3. Pattern kuralları
        pattern_result = self._check_pattern_rules(profile)
        if pattern_result['confidence'] > 0.6:
            return pattern_result
        
        return {"canonical": None, "confidence": 0.0, "source": "heuristic", "reason": "No match"}
    
    def _check_lexicon(self, profile) -> Optional[Dict]:
        """ERP lexicon'dan direkt eşleşme"""
        key = (profile.erp_code, profile.table_name, profile.column_name)
        
        if key in self.lexicons:
            return {
                "canonical": self.lexicons[key]["canonical"],
                "confidence": self.lexicons[key]["confidence"],
                "source": "lexicon",
                "reason": f"Found in {profile.erp_code} lexicon"
            }
        return None
    
    def _check_name_rules(self, profile) -> Dict:
        """Kolon adı kuralları"""
        col_lower = profile.column_name.lower()
        
        # ID fields
        if col_lower in ['ebeln', 'belge_no', 'ficheno']:
            return {"canonical": "po_id", "confidence": 0.85, "source": "name_rule", 
                    "reason": "Common PO ID field"}
        
        if col_lower in ['lifnr', 'cari_kod', 'vendor_code']:
            return {"canonical": "vendor_id", "confidence": 0.85, "source": "name_rule",
                    "reason": "Common vendor ID field"}
        
        # Date fields
        if any(x in col_lower for x in ['date', 'dt', 'tarih', 'aedat']):
            return {"canonical": "timestamp", "confidence": 0.75, "source": "name_rule",
                    "reason": "Date field name"}
        
        # Quantity
        if any(x in col_lower for x in ['menge', 'miktar', 'qty', 'quantity']):
            return {"canonical": "quantity", "confidence": 0.80, "source": "name_rule",
                    "reason": "Quantity field"}
        
        # Currency
        if any(x in col_lower for x in ['waers', 'curr', 'currency', 'doviz']):
            return {"canonical": "currency", "confidence": 0.85, "source": "name_rule",
                    "reason": "Currency field"}
        
        return {"canonical": None, "confidence": 0.0, "source": "name_rule", "reason": "No match"}
    
    def _check_pattern_rules(self, profile) -> Dict:
        """Veri pattern'lerine göre"""
        
        # Fixed 10-digit numeric → likely ID
        if 'fixed_length_10' in profile.patterns and profile.distinct_ratio > 0.95:
            return {"canonical": "po_id", "confidence": 0.70, "source": "pattern_rule",
                    "reason": "10-digit unique ID pattern"}
        
        # Currency codes
        sample_upper = [str(v).upper() for v in profile.sample_values]
        if any(curr in sample_upper for curr in ['EUR', 'USD', 'TRY']):
            return {"canonical": "currency", "confidence": 0.90, "source": "pattern_rule",
                    "reason": "Currency code pattern"}
        
        # Date patterns
        if 'date_yyyymmdd' in profile.patterns or 'date_iso' in profile.patterns:
            return {"canonical": "timestamp", "confidence": 0.85, "source": "pattern_rule",
                    "reason": "Date format detected"}
        
        return {"canonical": None, "confidence": 0.0, "source": "pattern_rule", "reason": "No match"}
