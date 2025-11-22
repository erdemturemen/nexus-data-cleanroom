"""
M3: Embedding Mapper - Semantic similarity ile mapping
"""
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import Dict, List

class EmbeddingMapper:
    """Semantic similarity ile mapping"""
    
    def __init__(self):
        # Türkçe + İngilizce destekli model
        self.model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
        self.canonical_embeddings = self._load_canonical_embeddings()
    
    def _load_canonical_embeddings(self) -> Dict:
        """Canonical field açıklamalarını embed et"""
        descriptions = {
            'po_id': 'Unique identifier for a purchase order document',
            'vendor_id': 'Unique identifier of the supplier or vendor',
            'material_id': 'Product, material or item code',
            'quantity': 'Number of units ordered or delivered',
            'unit_price': 'Price per single unit',
            'total_value': 'Total monetary value of the transaction',
            'currency': 'Currency code such as EUR, USD, TRY',
            'timestamp': 'Date and time of the event or transaction',
            'delivery_date': 'Expected or actual delivery date',
            'user_id': 'User identifier who performed the action',
        }
        
        embeddings = {}
        for field, desc in descriptions.items():
            embeddings[field] = {
                "description": desc,
                "embedding": self.model.encode(desc, convert_to_numpy=True)
            }
        
        return embeddings
    
    def suggest_mapping(self, profile, top_k: int = 3) -> List[Dict]:
        """En benzer canonical field'ları bul"""
        
        profile_text = self._create_profile_text(profile)
        profile_embedding = self.model.encode(profile_text, convert_to_numpy=True)
        
        similarities = []
        for canonical, data in self.canonical_embeddings.items():
            sim = self._cosine_similarity(profile_embedding, data['embedding'])
            similarities.append({
                "canonical": canonical,
                "confidence": float(sim),
                "source": "embedding",
                "reason": f"Semantic similarity: {sim:.3f}"
            })
        
        similarities.sort(key=lambda x: x['confidence'], reverse=True)
        return similarities[:top_k]
    
    def _create_profile_text(self, profile) -> str:
        """Profili embedding için metne çevir"""
        parts = [
            f"Column name: {profile.column_name}",
            f"Table: {profile.table_name}",
            f"Type: {profile.inferred_semantic_type}",
            f"Examples: {', '.join(profile.sample_values[:3])}"
        ]
        return ". ".join(parts)
    
    @staticmethod
    def _cosine_similarity(v1: np.ndarray, v2: np.ndarray) -> float:
        """Cosine similarity hesapla"""
        return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
