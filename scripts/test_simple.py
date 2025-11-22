#!/usr/bin/env python3
import sys
import os

# Path ekle
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

print("NEXUS Test Başlıyor...")
print("=" * 60)

try:
    from mapping_engine.features import ColumnProfile
    print("✅ ColumnProfile import edildi")
    
    from mapping_engine.heuristics import HeuristicMapper
    print("✅ HeuristicMapper import edildi")
    
    # Test profili oluştur
    profile = ColumnProfile(
        erp_code='SAP_S4',
        table_name='EKKO',
        column_name='EBELN',
        data_type='string',
        inferred_semantic_type='identifier',
        null_ratio=0.0,
        distinct_ratio=0.98,
        sample_values=['4500009182', '4500009183'],
        patterns=['fixed_length_10'],
        min_length=10,
        max_length=10
    )
    print(f"\n✅ Test profili oluşturuldu: {profile.column_name}")
    
    # Heuristic test
    mapper = HeuristicMapper(db_session=None)
    print("\n✅ HeuristicMapper oluşturuldu")
    
    result = mapper.suggest_mapping(profile)
    print(f"\n📊 SONUÇ:")
    print(f"  Kolon: {profile.column_name}")
    print(f"  Mapping: {result['canonical']}")
    print(f"  Confidence: {result['confidence']}")
    print(f"  Kaynak: {result['source']}")
    print(f"  Açıklama: {result['reason']}")
    
    print("\n" + "=" * 60)
    print("✅ TEST BAŞARILI!")
    
except Exception as e:
    print(f"\n❌ HATA: {e}")
    import traceback
    traceback.print_exc()
