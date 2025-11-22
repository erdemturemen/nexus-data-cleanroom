"""
M3: Decision Engine - Tüm mapper'ları birleştirip final karar verir
"""
from typing import Dict, List
from .heuristics import HeuristicMapper
from .embeddings import EmbeddingMapper
from .llm_mapper import LLMMapper

class MappingDecisionEngine:
    """Tüm mapper sonuçlarını birleştir ve karar ver"""
    
    def __init__(self, db_session, use_llm: bool = True):
        self.heuristic_mapper = HeuristicMapper(db_session)
        self.embedding_mapper = EmbeddingMapper()
        self.llm_mapper = LLMMapper() if use_llm else None
        
        self.weights = {
            'heuristic': 0.40,
            'embedding': 0.20,
            'llm': 0.40
        }
    
    def decide_mapping(self, profile) -> Dict:
        """Tüm mapper'ları çalıştır ve final kararı ver"""
        
        results = {'profile': profile, 'heuristic': None, 'embedding': None, 
                   'llm': None, 'final': None}
        
        # 1. Heuristic
        heuristic_result = self.heuristic_mapper.suggest_mapping(profile)
        results['heuristic'] = heuristic_result
        
        # Heuristic çok emin ise diğerlerini çalıştırma
        if heuristic_result['confidence'] >= 0.90:
            results['final'] = {
                "canonical": heuristic_result['canonical'],
                "confidence": heuristic_result['confidence'],
                "source": "heuristic_only",
                "reason": heuristic_result['reason']
            }
            return results
        
        # 2. Embedding
        embedding_results = self.embedding_mapper.suggest_mapping(profile, top_k=1)
        embedding_result = embedding_results[0] if embedding_results else {
            "canonical": None, "confidence": 0.0
        }
        results['embedding'] = embedding_result
        
        # 3. LLM
        if self.llm_mapper:
            llm_result = self.llm_mapper.suggest_mapping(profile)
            results['llm'] = llm_result
        else:
            llm_result = {"canonical": None, "confidence": 0.0}
        
        # 4. Final Karar
        final_decision = self._calculate_weighted_decision(
            heuristic_result, embedding_result, llm_result
        )
        results['final'] = final_decision
        
        return results
    
    def _calculate_weighted_decision(self, heuristic, embedding, llm) -> Dict:
        """Ağırlıklı skor hesapla"""
        
        suggestions = {}
        
        # Her yöntemden gelen öneriyi topla
        for result, weight_key in [(heuristic, 'heuristic'), 
                                    (embedding, 'embedding'), 
                                    (llm, 'llm')]:
            if result.get('canonical'):
                canonical = result['canonical']
                if canonical not in suggestions:
                    suggestions[canonical] = {'scores': {}, 'reasons': []}
                suggestions[canonical]['scores'][weight_key] = result['confidence']
                suggestions[canonical]['reasons'].append(f"{weight_key}: {result.get('reason', '')}")
        
        if not suggestions:
            return {"canonical": None, "confidence": 0.0, "source": "no_consensus"}
        
        # En yüksek weighted score'u bul
        best_canonical = None
        best_score = 0.0
        
        for canonical, data in suggestions.items():
            scores = data['scores']
            weighted_score = (
                scores.get('heuristic', 0.0) * self.weights['heuristic'] +
                scores.get('embedding', 0.0) * self.weights['embedding'] +
                scores.get('llm', 0.0) * self.weights['llm']
            )
            
            if weighted_score > best_score:
                best_score = weighted_score
                best_canonical = canonical
        
        return {
            "canonical": best_canonical,
            "confidence": round(best_score, 3),
            "source": "weighted_consensus",
            "reason": f"Combined decision (score: {best_score:.3f})"
        }
