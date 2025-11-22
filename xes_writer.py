"""
M7: XES Writer - Process mining tools için XES format çıktı
"""
import xml.etree.ElementTree as ET
from xml.dom import minidom
import pandas as pd
from datetime import datetime

class XESWriter:
    """Event log'u XES formatında kaydeder (PM4Py, ProM, Celonis uyumlu)"""
    
    def __init__(self):
        self.xes_namespace = "http://www.xes-standard.org/"
    
    def write_xes(self, event_log: pd.DataFrame, output_path: str, 
                  log_name: str = "NEXUS Event Log") -> str:
        """
        Event log'u XES formatında yaz
        
        Args:
            event_log: Event log DataFrame (case_id, activity, timestamp, resource, ...)
            output_path: Çıktı dosya yolu
            log_name: Log ismi (metadata için)
        
        Returns:
            Yazılan dosya yolu
        """
        
        # Root element
        log = ET.Element('log')
        log.set('xes.version', '1.0')
        log.set('xes.features', 'nested-attributes')
        
        # Extensions
        self._add_extensions(log)
        
        # Classifiers
        self._add_classifiers(log)
        
        # Global trace attributes
        self._add_global_trace_attributes(log)
        
        # Global event attributes
        self._add_global_event_attributes(log)
        
        # Log attributes (metadata)
        self._add_string_attribute(log, 'concept:name', log_name)
        self._add_string_attribute(log, 'lifecycle:model', 'standard')
        self._add_date_attribute(log, 'time:timestamp', datetime.now().isoformat())
        
        # Traces (her case bir trace)
        for case_id in event_log['case_id'].unique():
            case_events = event_log[event_log['case_id'] == case_id].sort_values('timestamp')
            trace = self._create_trace(case_id, case_events)
            log.append(trace)
        
        # XML'i güzelce formatla ve yaz
        xml_str = self._prettify_xml(log)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(xml_str)
        
        return output_path
    
    def _add_extensions(self, log):
        """XES extensions"""
        extensions = [
            ('Concept', 'http://www.xes-standard.org/concept.xesext'),
            ('Time', 'http://www.xes-standard.org/time.xesext'),
            ('Organizational', 'http://www.xes-standard.org/org.xesext'),
            ('Lifecycle', 'http://www.xes-standard.org/lifecycle.xesext'),
        ]
        
        for name, uri in extensions:
            ext = ET.SubElement(log, 'extension')
            ext.set('name', name)
            ext.set('prefix', name.lower())
            ext.set('uri', uri)
    
    def _add_classifiers(self, log):
        """Event classifiers"""
        # Activity classifier
        classifier = ET.SubElement(log, 'classifier')
        classifier.set('name', 'Activity')
        classifier.set('keys', 'concept:name')
        
        # Activity + Resource classifier
        classifier2 = ET.SubElement(log, 'classifier')
        classifier2.set('name', 'Activity and Resource')
        classifier2.set('keys', 'concept:name org:resource')
    
    def _add_global_trace_attributes(self, log):
        """Global trace attributes"""
        global_trace = ET.SubElement(log, 'global')
        global_trace.set('scope', 'trace')
        
        self._add_string_attribute(global_trace, 'concept:name', '__INVALID__')
    
    def _add_global_event_attributes(self, log):
        """Global event attributes"""
        global_event = ET.SubElement(log, 'global')
        global_event.set('scope', 'event')
        
        self._add_string_attribute(global_event, 'concept:name', '__INVALID__')
        self._add_date_attribute(global_event, 'time:timestamp', '1970-01-01T00:00:00.000+00:00')
        self._add_string_attribute(global_event, 'org:resource', '__INVALID__')
        self._add_string_attribute(global_event, 'lifecycle:transition', 'complete')
    
    def _create_trace(self, case_id: str, case_events: pd.DataFrame):
        """Bir case için trace oluştur"""
        
        trace = ET.Element('trace')
        
        # Trace attributes
        self._add_string_attribute(trace, 'concept:name', str(case_id))
        
        # Case attributes (ilk event'ten al)
        first_event = case_events.iloc[0]
        if 'vendor_name' in first_event and pd.notna(first_event['vendor_name']):
            self._add_string_attribute(trace, 'vendor:name', str(first_event['vendor_name']))
        if 'department' in first_event and pd.notna(first_event['department']):
            self._add_string_attribute(trace, 'department', str(first_event['department']))
        if 'total_value' in first_event and pd.notna(first_event['total_value']):
            self._add_float_attribute(trace, 'total:value', float(first_event['total_value']))
        if 'currency' in first_event and pd.notna(first_event['currency']):
            self._add_string_attribute(trace, 'currency', str(first_event['currency']))
        
        # Events
        for idx, event_row in case_events.iterrows():
            event = self._create_event(event_row)
            trace.append(event)
        
        return trace
    
    def _create_event(self, event_row: pd.Series):
        """Bir event oluştur"""
        
        event = ET.Element('event')
        
        # Required attributes
        self._add_string_attribute(event, 'concept:name', str(event_row['activity']))
        
        # Timestamp
        ts = event_row['timestamp']
        if isinstance(ts, str):
            ts_iso = ts
        else:
            ts_iso = ts.isoformat()
        self._add_date_attribute(event, 'time:timestamp', ts_iso)
        
        # Resource
        if 'resource' in event_row and pd.notna(event_row['resource']):
            self._add_string_attribute(event, 'org:resource', str(event_row['resource']))
        
        # Lifecycle
        self._add_string_attribute(event, 'lifecycle:transition', 'complete')
        
        # Additional attributes
        optional_attrs = {
            'vendor_id': 'string',
            'material_id': 'string',
            'material_desc': 'string',
            'quantity': 'int',
            'unit_price': 'float',
            'plant_id': 'string'
        }
        
        for attr, dtype in optional_attrs.items():
            if attr in event_row and pd.notna(event_row[attr]):
                value = event_row[attr]
                if dtype == 'string':
                    self._add_string_attribute(event, attr, str(value))
                elif dtype == 'int':
                    self._add_int_attribute(event, attr, int(value))
                elif dtype == 'float':
                    self._add_float_attribute(event, attr, float(value))
        
        return event
    
    def _add_string_attribute(self, parent, key: str, value: str):
        """String attribute ekle"""
        attr = ET.SubElement(parent, 'string')
        attr.set('key', key)
        attr.set('value', str(value))
        return attr
    
    def _add_date_attribute(self, parent, key: str, value: str):
        """Date attribute ekle"""
        attr = ET.SubElement(parent, 'date')
        attr.set('key', key)
        attr.set('value', str(value))
        return attr
    
    def _add_int_attribute(self, parent, key: str, value: int):
        """Int attribute ekle"""
        attr = ET.SubElement(parent, 'int')
        attr.set('key', key)
        attr.set('value', str(value))
        return attr
    
    def _add_float_attribute(self, parent, key: str, value: float):
        """Float attribute ekle"""
        attr = ET.SubElement(parent, 'float')
        attr.set('key', key)
        attr.set('value', str(value))
        return attr
    
    def _prettify_xml(self, elem):
        """XML'i güzel formatla"""
        rough_string = ET.tostring(elem, encoding='utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ", encoding='utf-8').decode('utf-8')
