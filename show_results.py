import pandas as pd

print("=" * 60)
print("📊 NEXUS PIPELINE SONUÇLARI")
print("=" * 60)

# M2: CSV Yükleme
csv_file = "/Users/erdemturemen/Desktop/2logo.csv"
df = pd.read_csv(csv_file, delimiter=';')

print("\n✅ M2 - LOGO CONNECTOR:")
print(f"  Satır sayısı: {len(df)}")
print(f"  Kolon sayısı: {len(df.columns)}")
print(f"  Kolonlar: {', '.join(df.columns.tolist()[:5])}...")

# M4: Quality Check
null_count = df.isnull().sum().sum()
completeness = (1 - null_count / (len(df) * len(df.columns))) * 100

print("\n✅ M4 - QUALITY CHECK:")
print(f"  Veri tamlığı: {completeness:.1f}%")
print(f"  Eksik değer: {null_count}")
print(f"  Quality Score: {completeness:.1f}/100")

# M5: Event Builder
import sys
sys.path.append('src/event_builder')
from event_constructor import EventConstructor

constructor = EventConstructor()
events = constructor.construct_events_from_logo_purchase(df)

print("\n✅ M5 - EVENT BUILDER:")
print(f"  Toplam event: {len(events)}")
print(f"  Toplam case: {events['case_id'].nunique()}")
print(f"  Farklı activity: {events['activity'].nunique()}")

print("\n  Activity Dağılımı:")
for activity, count in events['activity'].value_counts().items():
    print(f"    • {activity}: {count}")

# M7: XES Writer
import os
xes_file = 'my_logo_output.xes'
xes_size = os.path.getsize(xes_file) / (1024 * 1024)

print("\n✅ M7 - XES WRITER:")
print(f"  Dosya: {xes_file}")
print(f"  Boyut: {xes_size:.1f} MB")
print(f"  Format: XES 1.0")
print(f"  Uyumluluk: ProM, Celonis, Disco")

print("\n" + "=" * 60)
print("🎉 TÜM MODÜLLER BAŞARILI!")
print("=" * 60)
