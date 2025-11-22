import sys
import pandas as pd
sys.path.append('src/event_builder')
sys.path.append('src/storage/formats')

from event_constructor import EventConstructor
from xes_writer import XESWriter

print("🚀 NEXUS Hızlı Test\n")

# Test verisi
data = {
    'PO_NO': ['PO001', 'PO002', 'PO003'],
    'PO_DATE': ['2024-01-15', '2024-01-16', '2024-01-17'],
    'VENDOR_CODE': ['V001', 'V002', 'V003'],
    'QUANTITY': [100, 200, 150],
    'CREATED_BY': ['ali', 'ayse', 'mehmet'],
    'INTERIM_STATUSES': [
        'Talep|Onay|Sevk',
        'Talep|Onay',
        'Talep|Onay|Sevk|Teslim'
    ]
}

df = pd.DataFrame(data)
print(f"✅ Test verisi: {len(df)} satır\n")

# Event oluştur
constructor = EventConstructor()
events = constructor.construct_events_from_logo_purchase(df)
print(f"✅ Event oluşturuldu: {len(events)} event\n")

# XES export
writer = XESWriter()
writer.write_xes(events, 'test_output.xes', 'NEXUS Test')
print(f"✅ XES dosyası: test_output.xes\n")

print("🎉 TEST BAŞARILI!")
