"""
M5: Event Constructor - Canonical veriyi event log'a dönüştürür
"""
import pandas as pd
from datetime import datetime
from typing import List, Dict

class EventConstructor:
    """Mapped data'yı process mining event log'una dönüştürür"""
    
    def __init__(self):
        self.required_fields = ['case_id', 'activity', 'timestamp']
    
    def construct_events_from_logo_purchase(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Logo purchase data'sından event log oluşturur
        
        Expected columns (canonical names):
        - case_id (PO_NO)
        - timestamp (PO_DATE)
        - approval_timestamp
        - shipment_timestamp
        - delivery_timestamp
        - activity_sequence (INTERIM_STATUSES)
        - user_id (CREATED_BY)
        - approver_id (APPROVED_BY)
        - vendor_id, material_id, quantity, total_value, currency, etc.
        """
        
        events = []
        
        for idx, row in df.iterrows():
            case_id = row.get('case_id') or row.get('PO_NO')
            
            # INTERIM_STATUSES'u parse et
            if 'activity_sequence' in row:
                activities = row['activity_sequence'].split('|')
            elif 'INTERIM_STATUSES' in row:
                activities = row['INTERIM_STATUSES'].split('|')
            else:
                # Fallback: ORDER_STATUS'tan tek event oluştur
                activities = [row.get('final_status', row.get('ORDER_STATUS', 'Unknown'))]
            
            # Timestamp mapping
            timestamp_map = self._get_timestamp_mapping(row)
            
            # Her activity için event oluştur
            for i, activity in enumerate(activities):
                event = {
                    'case_id': case_id,
                    'activity': activity,
                    'timestamp': timestamp_map.get(activity, row.get('timestamp', row.get('PO_DATE'))),
                    'resource': self._get_resource(row, activity, i),
                    
                    # Attributes (zenginleştirme için)
                    'vendor_id': row.get('vendor_id', row.get('VENDOR_CODE')),
                    'vendor_name': row.get('vendor_name', row.get('VENDOR_NAME')),
                    'material_id': row.get('material_id', row.get('MATERIAL_CODE')),
                    'material_desc': row.get('material_desc', row.get('MATERIAL_DESC')),
                    'quantity': row.get('quantity', row.get('QUANTITY')),
                    'unit_price': row.get('unit_price', row.get('UNIT_PRICE')),
                    'total_value': row.get('total_value', row.get('TOTAL_VALUE')),
                    'currency': row.get('currency', row.get('CURRENCY')),
                    'department': row.get('department', row.get('DIVISION_CODE')),
                    'plant_id': row.get('plant_id', row.get('PLANT_CODE')),
                }
                
                events.append(event)
        
        # DataFrame'e çevir ve timestamp'e göre sırala
        event_log = pd.DataFrame(events)
        event_log['timestamp'] = pd.to_datetime(event_log['timestamp'], format='mixed')
        event_log = event_log.sort_values(['case_id', 'timestamp'])
        
        return event_log
    
    def _get_timestamp_mapping(self, row: pd.Series) -> Dict[str, str]:
        """Activity'lere timestamp ata"""
        
        base_ts = row.get('timestamp', row.get('PO_DATE'))
        
        mapping = {
            'Talep Oluşturuldu': base_ts if isinstance(base_ts, str) else str(base_ts),
            'Onay Bekliyor': base_ts if isinstance(base_ts, str) else str(base_ts),
            'Onaylandı': row.get('approval_timestamp', row.get('APPROVAL_DATETIME', base_ts)),
            'Sevk Edildi': row.get('shipment_timestamp', row.get('SHIPMENT_DATETIME', base_ts)),
            'Teslim Edildi': row.get('delivery_timestamp', row.get('DELIVERY_DATETIME', base_ts)),
        }
        
        return mapping
    
    def _get_resource(self, row: pd.Series, activity: str, index: int) -> str:
        """Activity'ye göre resource (kişi) belirle"""
        
        # İlk activity (Talep) → creator
        if index == 0 or activity == 'Talep Oluşturuldu':
            return row.get('user_id', row.get('CREATED_BY', 'system'))
        
        # Onay activity'leri → approver
        if 'Onay' in activity or activity == 'Onaylandı':
            return row.get('approver_id', row.get('APPROVED_BY', 
                          row.get('user_id', row.get('CREATED_BY', 'system'))))
        
        # Diğerleri → creator veya system
        return row.get('user_id', row.get('CREATED_BY', 'system'))
    
    def validate_event_log(self, event_log: pd.DataFrame) -> Dict:
        """Event log'u valide et"""
        
        issues = []
        
        # Required fields kontrolü
        for field in self.required_fields:
            if field not in event_log.columns:
                issues.append(f"Missing required field: {field}")
        
        # Null kontrolü
        for field in self.required_fields:
            if field in event_log.columns:
                null_count = event_log[field].isna().sum()
                if null_count > 0:
                    issues.append(f"{field} has {null_count} null values")
        
        # Timestamp format kontrolü
        try:
            pd.to_datetime(event_log['timestamp'])
        except:
            issues.append("Timestamp format error")
        
        # Case ID kontrolü
        total_cases = event_log['case_id'].nunique()
        total_events = len(event_log)
        
        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'total_cases': total_cases,
            'total_events': total_events,
            'events_per_case': total_events / total_cases if total_cases > 0 else 0
        }
    
    def get_statistics(self, event_log: pd.DataFrame) -> Dict:
        """Event log istatistikleri"""
        
        stats = {
            'total_cases': event_log['case_id'].nunique(),
            'total_events': len(event_log),
            'unique_activities': event_log['activity'].nunique(),
            'unique_resources': event_log['resource'].nunique(),
            'date_range': {
                'start': event_log['timestamp'].min(),
                'end': event_log['timestamp'].max()
            },
            'activity_distribution': event_log['activity'].value_counts().to_dict(),
            'resource_distribution': event_log['resource'].value_counts().to_dict()
        }
        
        return stats
