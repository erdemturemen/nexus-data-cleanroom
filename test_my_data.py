import sys
import pandas as pd
sys.path.append('src/event_builder')
sys.path.append('src/storage/formats')

from event_constructor import EventConstructor
from xes_writer import XESWriter

# KENDİ CSV'Nİ YÜK
csv_file = input("CSV dosya yolu: ")

try:
    df = pd.read_csv(csv_file)
    print(f"\n✅ Yüklendi: {len(df)} satır, {len(df.columns)} kolon")
    print(f"Kolonlar: {df.columns.tolist()[:5]}...")
    
    # Event oluştur
    constructor = EventConstructor()
    events = constructor.construct_events_from_logo_purchase(df)
    print(f"\n✅ {len(events)} event oluşturuldu!")
    
    # XES kaydet
    writer = XESWriter()
    output = 'my_output.xes'
    writer.write_xes(events, output, 'My NEXUS Test')
    print(f"✅ XES kaydedildi: {output}")
    print("\n🎉 BAŞARILI!")
    
except Exception as e:
    print(f"\n❌ Hata: {e}")
