import sys
import pandas as pd
sys.path.append('src/event_builder')
sys.path.append('src/storage/formats')

from event_constructor import EventConstructor
from xes_writer import XESWriter

csv_file = input("CSV dosya yolu: ")

try:
    # Noktalı virgül delimiter ile oku
    df = pd.read_csv(csv_file, delimiter=';')
    print(f"\n✅ Yüklendi: {len(df)} satır, {len(df.columns)} kolon")
    print(f"\nİlk 5 kolon:")
    for col in df.columns[:5]:
        print(f"  - {col}")
    
    # Event oluştur
    constructor = EventConstructor()
    events = constructor.construct_events_from_logo_purchase(df)
    print(f"\n✅ {len(events)} event oluşturuldu!")
    
    # XES kaydet
    writer = XESWriter()
    output = 'my_logo_output.xes'
    writer.write_xes(events, output, 'Logo NEXUS')
    print(f"✅ XES kaydedildi: {output}")
    
    import os
    size = os.path.getsize(output) / 1024
    print(f"📦 Dosya boyutu: {size:.1f} KB")
    print("\n🎉 BAŞARILI!")
    
except Exception as e:
    print(f"\n❌ Hata: {e}")
    import traceback
    traceback.print_exc()
