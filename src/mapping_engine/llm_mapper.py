"""
M3: LLM Mapper - Local LLM (Ollama) ile intelligent mapping
"""
import requests
import json
from typing import Dict

class LLMMapper:
    """Local LLM ile intelligent mapping"""
    
    def __init__(self, model_name: str = "qwen2.5:7b"):
        self.ollama_url = "http://localhost:11434/api/generate"
        self.model_name = model_name
    
    def suggest_mapping(self, profile, timeout: int = 30) -> Dict:
        """LLM ile mapping önerisi"""
        
        prompt = self._build_prompt(profile)
        
        try:
            response = self._call_ollama(prompt, timeout)
            result = self._parse_response(response)
            return result
        except Exception as e:
            return {
                "canonical": None,
                "confidence": 0.0,
                "source": "llm_error",
                "reason": str(e)
            }
    
    def _build_prompt(self, profile) -> str:
        """LLM için prompt"""
        return f"""Sen bir ERP veri mimarısısın. ERP kolonlarını standart alanlara eşleştir.

ERP Bilgileri:
- Sistem: {profile.erp_code}
- Tablo: {profile.table_name}
- Kolon: {profile.column_name}
- Veri Tipi: {profile.data_type}
- Örnek Değerler: {', '.join(profile.sample_values[:5])}

Standart Alanlar: po_id, vendor_id, material_id, quantity, unit_price, 
total_value, currency, timestamp, delivery_date, user_id

SADECE JSON formatında cevap ver:
{{"suggested_canonical": "po_id", "confidence": 0.95, "reason": "EBELN is SAP PO number"}}

JSON:"""
    
    def _call_ollama(self, prompt: str, timeout: int) -> str:
        """Ollama API'ye istek"""
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.1}
        }
        
        response = requests.post(self.ollama_url, json=payload, timeout=timeout)
        return response.json()['response']
    
    def _parse_response(self, response_text: str) -> Dict:
        """LLM çıktısını parse et"""
        response_text = response_text.strip()
        
        # Markdown temizle
        if response_text.startswith('```'):
            response_text = response_text.split('```')[1]
            if response_text.startswith('json'):
                response_text = response_text[4:]
        
        try:
            data = json.loads(response_text.strip())
            return {
                "canonical": data.get("suggested_canonical"),
                "confidence": float(data.get("confidence", 0.0)),
                "source": "llm",
                "reason": data.get("reason", "LLM suggestion")
            }
        except:
            return {"canonical": None, "confidence": 0.0, "source": "llm_parse_error",
                    "reason": "Could not parse LLM response"}
