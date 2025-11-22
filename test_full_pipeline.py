#!/usr/bin/env python3
"""
NEXUS Data Cleanroom - Full Pipeline Test
Logo purchase data ile M5 + M7 test
"""

import sys
import pandas as pd
from datetime import datetime

# Event constructor ve XES writer import
sys.path.insert(0, '/mnt/user-data/outputs')
from event_constructor import EventConstructor
from xes_writer import XESWriter

print("=" * 80)
print("🚀 NEXUS FULL PIPELINE TEST - LOGO PURCHASE DATA")
print("=" * 80)

# 1. Logo CSV'yi oku
print("\n📁 Step 1: Loading Logo Purchase Data...")
df = pd.read_csv('/mnt/user-data/uploads/2logo_purchase_data_with_process_fields.csv', delimiter=';')
print(f"✅ Loaded: {len(df)} rows, {len(df.columns)} columns")

# 2. Event Constructor ile event log oluştur
print("\n🔄 Step 2: Constructing Event Log...")
constructor = EventConstructor()
event_log = constructor.construct_events_from_logo_purchase(df)
print(f"✅ Created: {len(event_log)} events from {df['PO_NO'].nunique()} cases")

# 3. Event log validasyonu
print("\n✅ Step 3: Validating Event Log...")
validation = constructor.validate_event_log(event_log)
if validation['valid']:
    print("✅ Event log is VALID")
else:
    print("⚠️  Event log has issues:")
    for issue in validation['issues']:
        print(f"   - {issue}")

print(f"\n📊 Event Log Summary:")
print(f"   • Total Cases: {validation['total_cases']:,}")
print(f"   • Total Events: {validation['total_events']:,}")
print(f"   • Events per Case: {validation['events_per_case']:.2f}")

# 4. İstatistikler
print("\n📈 Step 4: Event Log Statistics...")
stats = constructor.get_statistics(event_log)
print(f"\n   • Unique Activities: {stats['unique_activities']}")
print(f"   • Unique Resources: {stats['unique_resources']}")
print(f"   • Date Range: {stats['date_range']['start']} → {stats['date_range']['end']}")

print(f"\n   Activity Distribution:")
for activity, count in list(stats['activity_distribution'].items())[:10]:
    pct = (count / stats['total_events']) * 100
    print(f"      {activity:30} : {count:6,} ({pct:5.1f}%)")

print(f"\n   Resource Distribution:")
for resource, count in stats['resource_distribution'].items():
    pct = (count / stats['total_events']) * 100
    print(f"      {resource:15} : {count:6,} ({pct:5.1f}%)")

# 5. İlk case'i göster
print("\n" + "=" * 80)
print("📋 SAMPLE CASE (First PO)")
print("=" * 80)

first_case_id = event_log.iloc[0]['case_id']
first_case_events = event_log[event_log['case_id'] == first_case_id]

print(f"\nCase ID: {first_case_id}")
print(f"Events: {len(first_case_events)}\n")

for idx, event in first_case_events.iterrows():
    print(f"{event['timestamp']} | {event['activity']:30} | Resource: {event['resource']:10} | {event['total_value']:10,.2f} {event['currency']}")

# 6. XES formatında kaydet
print("\n" + "=" * 80)
print("💾 Step 5: Writing XES File...")
print("=" * 80)

xes_writer = XESWriter()
xes_path = '/mnt/user-data/outputs/logo_purchase_event_log.xes'

try:
    xes_writer.write_xes(
        event_log=event_log,
        output_path=xes_path,
        log_name="Logo Purchase Orders - NEXUS Data Cleanroom"
    )
    print(f"✅ XES file created: {xes_path}")
    
    # Dosya boyutunu kontrol et
    import os
    file_size = os.path.getsize(xes_path)
    print(f"   File size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
    
except Exception as e:
    print(f"❌ XES creation failed: {e}")
    import traceback
    traceback.print_exc()

# 7. CSV formatında da kaydet (yedek olarak)
print("\n💾 Step 6: Writing CSV File...")
csv_path = '/mnt/user-data/outputs/logo_purchase_event_log.csv'
event_log.to_csv(csv_path, index=False)
print(f"✅ CSV file created: {csv_path}")

# Final Summary
print("\n" + "=" * 80)
print("🎉 PIPELINE TEST COMPLETE!")
print("=" * 80)

print("\n✅ Generated Files:")
print(f"   1. {xes_path}")
print(f"   2. {csv_path}")

print("\n🎯 Next Steps:")
print("   1. Download XES file")
print("   2. Import to ProM / Celonis / Disco")
print("   3. Run process discovery")
print("   4. Analyze bottlenecks and variants")

print("\n💡 NEXUS Modules Used:")
print("   ✅ M5: Event Builder (EventConstructor)")
print("   ✅ M7: Event Log Storage (XESWriter)")
print("   ⏳ M2: Logo Connector (next session)")
print("   ⏳ M4: Quality Checker (next session)")

print("\n" + "=" * 80)
