"""
Enhanced Data Processing Module for PiWardrive
Provides real-time stream processing, advanced filtering, data correlation, and statistical analysis
"""

import asyncio
import threading
import queue
import time
import logging
import json
import sqlite3
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Any, Callable, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from collections import defaultdict, deque
from concurrent.futures import ThreadPoolExecutor
import statistics
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
import geojson
import csv
import xml.etree.ElementTree as ET
from pathlib import Path
import hashlib

logger = logging.getLogger(__name__)

@dataclass
class StreamEvent:
    """Data structure for streaming events"""
    timestamp: datetime
    event_type: str
    data: Dict[str, Any]
    source: str
    priority: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'timestamp': self.timestamp.isoformat(),
            'event_type': self.event_type,
            'data': self.data,
            'source': self.source,
            'priority': self.priority
        }

class RealTimeStreamProcessor:
    """Real-time stream processing for continuous data ingestion and analysis"""
    
    def __init__(self, buffer_size: int = 10000, batch_size: int = 100):
        self.buffer_size = buffer_size
        self.batch_size = batch_size
        self.event_buffer = deque(maxlen=buffer_size)
        self.processors = {}
        self.filters = {}
        self.running = False
        self.thread_pool = ThreadPoolExecutor(max_workers=4)
        self.lock = threading.Lock()
        
    def add_processor(self, name: str, processor: Callable[[List[StreamEvent]], None]):
        """Add a stream processor function"""
        self.processors[name] = processor
        
    def add_filter(self, name: str, filter_func: Callable[[StreamEvent], bool]):
        """Add a stream filter function"""
        self.filters[name] = filter_func
        
    def push_event(self, event: StreamEvent):
        """Push a new event to the stream"""
        with self.lock:
            self.event_buffer.append(event)
            
    def start_processing(self):
        """Start the real-time processing loop"""
        self.running = True
        asyncio.create_task(self._process_loop())
        
    def stop_processing(self):
        """Stop the real-time processing"""
        self.running = False
        
    async def _process_loop(self):
        """Main processing loop"""
        while self.running:
            batch = []
            
            # Collect batch of events
            with self.lock:
                batch_size = min(self.batch_size, len(self.event_buffer))
                for _ in range(batch_size):
                    if self.event_buffer:
                        batch.append(self.event_buffer.popleft())
                        
            if batch:
                # Apply filters
                filtered_batch = []
                for event in batch:
                    if all(filter_func(event) for filter_func in self.filters.values()):
                        filtered_batch.append(event)
                        
                # Process filtered batch
                for name, processor in self.processors.items():
                    try:
                        await asyncio.get_event_loop().run_in_executor(
                            self.thread_pool, processor, filtered_batch
                        )
                    except Exception as e:
                        logger.error(f"Error in processor {name}: {e}")
                        
            await asyncio.sleep(0.1)  # Small delay to prevent CPU overload

class AdvancedFilteringEngine:
    """Advanced filtering engine with complex rule support"""
    
    def __init__(self):
        self.rules = {}
        self.rule_cache = {}
        
    def add_rule(self, name: str, rule_config: Dict[str, Any]):
        """Add a filtering rule
        
        Args:
            name: Rule name
            rule_config: Configuration dictionary with rule parameters
        """
        self.rules[name] = rule_config
        
    def compile_rule(self, rule_config: Dict[str, Any]) -> Callable:
        """Compile a rule configuration into a callable function"""
        rule_type = rule_config.get('type', 'simple')
        
        if rule_type == 'simple':
            field = rule_config['field']
            operator = rule_config['operator']
            value = rule_config['value']
            
            def simple_rule(data):
                data_value = data.get(field)
                if data_value is None:
                    return False
                    
                if operator == 'eq':
                    return data_value == value
                elif operator == 'ne':
                    return data_value != value
                elif operator == 'gt':
                    return data_value > value
                elif operator == 'lt':
                    return data_value < value
                elif operator == 'ge':
                    return data_value >= value
                elif operator == 'le':
                    return data_value <= value
                elif operator == 'in':
                    return data_value in value
                elif operator == 'not_in':
                    return data_value not in value
                elif operator == 'contains':
                    return value in str(data_value)
                elif operator == 'regex':
                    import re
                    return bool(re.search(value, str(data_value)))
                    
                return False
            
            return simple_rule
            
        elif rule_type == 'composite':
            logic = rule_config.get('logic', 'and')
            sub_rules = rule_config.get('rules', [])
            compiled_rules = [self.compile_rule(rule) for rule in sub_rules]
            
            def composite_rule(data):
                results = [rule(data) for rule in compiled_rules]
                if logic == 'and':
                    return all(results)
                elif logic == 'or':
                    return any(results)
                elif logic == 'not':
                    return not all(results)
                return False
                
            return composite_rule
            
        elif rule_type == 'geospatial':
            bounds = rule_config.get('bounds', {})
            lat_field = rule_config.get('lat_field', 'latitude')
            lon_field = rule_config.get('lon_field', 'longitude')
            
            def geospatial_rule(data):
                lat = data.get(lat_field)
                lon = data.get(lon_field)
                
                if lat is None or lon is None:
                    return False
                    
                return (bounds.get('min_lat', -90) <= lat <= bounds.get('max_lat', 90) and
                        bounds.get('min_lon', -180) <= lon <= bounds.get('max_lon', 180))
                        
            return geospatial_rule
            
        return lambda data: True
        
    def apply_filters(self, data: List[Dict[str, Any]], rule_names: List[str] = None) -> List[Dict[str, Any]]:
        """Apply filters to data"""
        if rule_names is None:
            rule_names = list(self.rules.keys())
            
        filtered_data = []
        for item in data:
            passes_all = True
            for rule_name in rule_names:
                if rule_name in self.rules:
                    rule_func = self.rule_cache.get(rule_name)
                    if rule_func is None:
                        rule_func = self.compile_rule(self.rules[rule_name])
                        self.rule_cache[rule_name] = rule_func
                        
                    if not rule_func(item):
                        passes_all = False
                        break
                        
            if passes_all:
                filtered_data.append(item)
                
        return filtered_data

class DataCorrelationEngine:
    """Engine for correlating data across different sources and time periods"""
    
    def __init__(self, correlation_window: timedelta = timedelta(minutes=5)):
        self.correlation_window = correlation_window
        self.correlation_rules = {}
        self.data_sources = {}
        
    def add_data_source(self, name: str, data: List[Dict[str, Any]]):
        """Add a data source for correlation"""
        self.data_sources[name] = data
        
    def add_correlation_rule(self, name: str, rule_config: Dict[str, Any]):
        """Add a correlation rule
        
        Args:
            name: Rule name
            rule_config: Configuration with source fields and correlation logic
        """
        self.correlation_rules[name] = rule_config
        
    def correlate_temporal(self, source1: str, source2: str, time_field: str = 'timestamp') -> List[Dict[str, Any]]:
        """Correlate data based on temporal proximity"""
        if source1 not in self.data_sources or source2 not in self.data_sources:
            return []
            
        data1 = self.data_sources[source1]
        data2 = self.data_sources[source2]
        
        correlations = []
        
        for item1 in data1:
            timestamp1 = datetime.fromisoformat(item1[time_field])
            
            for item2 in data2:
                timestamp2 = datetime.fromisoformat(item2[time_field])
                
                if abs(timestamp1 - timestamp2) <= self.correlation_window:
                    correlation = {
                        'source1': source1,
                        'source2': source2,
                        'data1': item1,
                        'data2': item2,
                        'time_diff': abs(timestamp1 - timestamp2).total_seconds(),
                        'correlation_type': 'temporal'
                    }
                    correlations.append(correlation)
                    
        return correlations
        
    def correlate_spatial(self, source1: str, source2: str, max_distance: float = 100.0) -> List[Dict[str, Any]]:
        """Correlate data based on spatial proximity"""
        if source1 not in self.data_sources or source2 not in self.data_sources:
            return []
            
        data1 = self.data_sources[source1]
        data2 = self.data_sources[source2]
        
        correlations = []
        
        for item1 in data1:
            lat1 = item1.get('latitude')
            lon1 = item1.get('longitude')
            
            if lat1 is None or lon1 is None:
                continue
                
            for item2 in data2:
                lat2 = item2.get('latitude')
                lon2 = item2.get('longitude')
                
                if lat2 is None or lon2 is None:
                    continue
                    
                distance = self._haversine_distance(lat1, lon1, lat2, lon2)
                
                if distance <= max_distance:
                    correlation = {
                        'source1': source1,
                        'source2': source2,
                        'data1': item1,
                        'data2': item2,
                        'distance': distance,
                        'correlation_type': 'spatial'
                    }
                    correlations.append(correlation)
                    
        return correlations
        
    def _haversine_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate Haversine distance between two points"""
        R = 6371000  # Earth's radius in meters
        
        lat1_rad = np.radians(lat1)
        lat2_rad = np.radians(lat2)
        delta_lat = np.radians(lat2 - lat1)
        delta_lon = np.radians(lon2 - lon1)
        
        a = np.sin(delta_lat/2)**2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(delta_lon/2)**2
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
        
        return R * c

class StatisticalAnalysisTools:
    """Statistical analysis tools for data insights"""
    
    def __init__(self):
        self.analysis_cache = {}
        
    def descriptive_statistics(self, data: List[Union[int, float]], field_name: str = "data") -> Dict[str, Any]:
        """Calculate descriptive statistics"""
        if not data:
            return {}
            
        stats = {
            'count': len(data),
            'mean': statistics.mean(data),
            'median': statistics.median(data),
            'mode': statistics.mode(data) if len(set(data)) < len(data) else None,
            'std_dev': statistics.stdev(data) if len(data) > 1 else 0,
            'variance': statistics.variance(data) if len(data) > 1 else 0,
            'min': min(data),
            'max': max(data),
            'range': max(data) - min(data),
            'percentiles': {
                '25th': np.percentile(data, 25),
                '50th': np.percentile(data, 50),
                '75th': np.percentile(data, 75),
                '90th': np.percentile(data, 90),
                '95th': np.percentile(data, 95),
                '99th': np.percentile(data, 99)
            }
        }
        
        return stats
        
    def signal_strength_analysis(self, signal_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze signal strength patterns"""
        if not signal_data:
            return {}
            
        strengths = [item.get('signal_strength', 0) for item in signal_data]
        channels = [item.get('channel', 0) for item in signal_data]
        
        analysis = {
            'signal_stats': self.descriptive_statistics(strengths, "signal_strength"),
            'channel_distribution': dict(pd.Series(channels).value_counts()),
            'coverage_analysis': self._analyze_coverage(signal_data),
            'interference_analysis': self._analyze_interference(signal_data),
            'temporal_patterns': self._analyze_temporal_patterns(signal_data)
        }
        
        return analysis
        
    def _analyze_coverage(self, signal_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze signal coverage patterns"""
        coverage_zones = {
            'excellent': 0,  # > -50 dBm
            'good': 0,       # -50 to -60 dBm
            'fair': 0,       # -60 to -70 dBm
            'poor': 0,       # -70 to -80 dBm
            'very_poor': 0   # < -80 dBm
        }
        
        for item in signal_data:
            strength = item.get('signal_strength', -100)
            if strength > -50:
                coverage_zones['excellent'] += 1
            elif strength > -60:
                coverage_zones['good'] += 1
            elif strength > -70:
                coverage_zones['fair'] += 1
            elif strength > -80:
                coverage_zones['poor'] += 1
            else:
                coverage_zones['very_poor'] += 1
                
        total = len(signal_data)
        coverage_percentages = {
            zone: (count / total) * 100 if total > 0 else 0
            for zone, count in coverage_zones.items()
        }
        
        return {
            'zones': coverage_zones,
            'percentages': coverage_percentages,
            'total_points': total
        }
        
    def _analyze_interference(self, signal_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze interference patterns"""
        channel_usage = defaultdict(list)
        
        for item in signal_data:
            channel = item.get('channel', 0)
            strength = item.get('signal_strength', -100)
            channel_usage[channel].append(strength)
            
        interference_analysis = {}
        
        for channel, strengths in channel_usage.items():
            if len(strengths) > 1:
                interference_analysis[channel] = {
                    'count': len(strengths),
                    'max_strength': max(strengths),
                    'avg_strength': statistics.mean(strengths),
                    'interference_score': len(strengths) * (max(strengths) / -30)  # Normalized score
                }
                
        return interference_analysis
        
    def _analyze_temporal_patterns(self, signal_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze temporal patterns in signal data"""
        if not signal_data:
            return {}
            
        # Group by time periods
        hourly_data = defaultdict(list)
        daily_data = defaultdict(list)
        
        for item in signal_data:
            timestamp_str = item.get('timestamp')
            if timestamp_str:
                timestamp = datetime.fromisoformat(timestamp_str)
                hour = timestamp.hour
                day = timestamp.weekday()
                strength = item.get('signal_strength', -100)
                
                hourly_data[hour].append(strength)
                daily_data[day].append(strength)
                
        hourly_patterns = {
            hour: statistics.mean(strengths) for hour, strengths in hourly_data.items()
        }
        
        daily_patterns = {
            day: statistics.mean(strengths) for day, strengths in daily_data.items()
        }
        
        return {
            'hourly_patterns': hourly_patterns,
            'daily_patterns': daily_patterns,
            'peak_hours': max(hourly_patterns.keys(), key=lambda x: hourly_patterns[x]) if hourly_patterns else None,
            'peak_day': max(daily_patterns.keys(), key=lambda x: daily_patterns[x]) if daily_patterns else None
        }

class ExportFormatExpansion:
    """Export data in various formats including KML, GeoJSON, and advanced CSV"""
    
    def __init__(self):
        self.supported_formats = ['csv', 'json', 'kml', 'geojson', 'xml', 'xlsx']
        
    def export_to_csv(self, data: List[Dict[str, Any]], filename: str, advanced_fields: bool = True) -> str:
        """Export data to CSV with advanced fields"""
        if not data:
            return filename
            
        # Determine all possible fields
        all_fields = set()
        for item in data:
            all_fields.update(item.keys())
            
        # Add advanced calculated fields
        if advanced_fields:
            enhanced_data = []
            for item in data:
                enhanced_item = item.copy()
                
                # Add calculated fields
                if 'latitude' in item and 'longitude' in item:
                    enhanced_item['coordinate_string'] = f"{item['latitude']},{item['longitude']}"
                    
                if 'signal_strength' in item:
                    strength = item['signal_strength']
                    enhanced_item['signal_quality'] = self._classify_signal_strength(strength)
                    enhanced_item['signal_dbm_normalized'] = (strength + 100) / 50  # Normalize to 0-1
                    
                if 'timestamp' in item:
                    timestamp = datetime.fromisoformat(item['timestamp'])
                    enhanced_item['hour_of_day'] = timestamp.hour
                    enhanced_item['day_of_week'] = timestamp.weekday()
                    enhanced_item['iso_week'] = timestamp.isocalendar().week
                    
                enhanced_data.append(enhanced_item)
                
            data = enhanced_data
            all_fields.update(['coordinate_string', 'signal_quality', 'signal_dbm_normalized', 
                             'hour_of_day', 'day_of_week', 'iso_week'])
            
        # Write CSV
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=sorted(all_fields))
            writer.writeheader()
            writer.writerows(data)
            
        return filename
        
    def export_to_kml(self, data: List[Dict[str, Any]], filename: str) -> str:
        """Export data to KML format"""
        kml_content = '''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>PiWardrive Survey Data</name>
    <description>Wireless survey data collected by PiWardrive</description>
    <Style id="signal_strong">
      <IconStyle>
        <color>ff00ff00</color>
        <scale>1.2</scale>
        <Icon>
          <href>http://maps.google.com/mapfiles/kml/pushpin/wht-pushpin.png</href>
        </Icon>
      </IconStyle>
    </Style>
    <Style id="signal_weak">
      <IconStyle>
        <color>ff0000ff</color>
        <scale>1.0</scale>
        <Icon>
          <href>http://maps.google.com/mapfiles/kml/pushpin/red-pushpin.png</href>
        </Icon>
      </IconStyle>
    </Style>
'''
        
        for item in data:
            if 'latitude' in item and 'longitude' in item:
                lat = item['latitude']
                lon = item['longitude']
                
                # Determine style based on signal strength
                signal_strength = item.get('signal_strength', -100)
                style = 'signal_strong' if signal_strength > -60 else 'signal_weak'
                
                # Create placemark
                name = item.get('ssid', 'Unknown SSID')
                description = self._create_kml_description(item)
                
                kml_content += f'''
    <Placemark>
      <name>{name}</name>
      <description><![CDATA[{description}]]></description>
      <styleUrl>#{style}</styleUrl>
      <Point>
        <coordinates>{lon},{lat},0</coordinates>
      </Point>
    </Placemark>
'''
                
        kml_content += '''
  </Document>
</kml>
'''
        
        with open(filename, 'w', encoding='utf-8') as kml_file:
            kml_file.write(kml_content)
            
        return filename
        
    def export_to_geojson(self, data: List[Dict[str, Any]], filename: str) -> str:
        """Export data to GeoJSON format"""
        features = []
        
        for item in data:
            if 'latitude' in item and 'longitude' in item:
                feature = geojson.Feature(
                    geometry=geojson.Point((item['longitude'], item['latitude'])),
                    properties={k: v for k, v in item.items() if k not in ['latitude', 'longitude']}
                )
                features.append(feature)
                
        feature_collection = geojson.FeatureCollection(features)
        
        with open(filename, 'w', encoding='utf-8') as geojson_file:
            geojson.dump(feature_collection, geojson_file, indent=2)
            
        return filename
        
    def _classify_signal_strength(self, strength: float) -> str:
        """Classify signal strength into categories"""
        if strength > -50:
            return 'excellent'
        elif strength > -60:
            return 'good'
        elif strength > -70:
            return 'fair'
        elif strength > -80:
            return 'poor'
        else:
            return 'very_poor'
            
    def _create_kml_description(self, item: Dict[str, Any]) -> str:
        """Create KML description from item data"""
        description = "<table>"
        
        key_fields = ['ssid', 'bssid', 'signal_strength', 'channel', 'encryption', 'timestamp']
        
        for field in key_fields:
            if field in item:
                value = item[field]
                if field == 'signal_strength':
                    value = f"{value} dBm ({self._classify_signal_strength(value)})"
                elif field == 'timestamp':
                    value = datetime.fromisoformat(value).strftime('%Y-%m-%d %H:%M:%S')
                    
                description += f"<tr><td><b>{field.replace('_', ' ').title()}:</b></td><td>{value}</td></tr>"
                
        description += "</table>"
        return description

# Example usage and test functions
def example_stream_processing():
    """Example of real-time stream processing"""
    processor = RealTimeStreamProcessor()
    
    # Add signal strength processor
    def signal_processor(events):
        for event in events:
            if event.event_type == 'wifi_scan':
                strength = event.data.get('signal_strength', -100)
                logger.info(f"Processing WiFi scan with strength: {strength} dBm")
                
    processor.add_processor('signal_analyzer', signal_processor)
    
    # Add filter for strong signals only
    def strong_signal_filter(event):
        if event.event_type == 'wifi_scan':
            return event.data.get('signal_strength', -100) > -70
        return True
        
    processor.add_filter('strong_signals', strong_signal_filter)
    
    # Start processing
    processor.start_processing()
    
    # Push some test events
    test_event = StreamEvent(
        timestamp=datetime.now(),
        event_type='wifi_scan',
        data={'signal_strength': -45, 'ssid': 'TestNetwork'},
        source='test_scanner'
    )
    
    processor.push_event(test_event)
    
    return processor

def example_export_formats():
    """Example of export format expansion"""
    # Sample data
    sample_data = [
        {
            'timestamp': '2024-01-01T12:00:00',
            'latitude': 40.7128,
            'longitude': -74.0060,
            'signal_strength': -45,
            'ssid': 'TestNetwork1',
            'bssid': '00:11:22:33:44:55',
            'channel': 6,
            'encryption': 'WPA2'
        },
        {
            'timestamp': '2024-01-01T12:05:00',
            'latitude': 40.7130,
            'longitude': -74.0062,
            'signal_strength': -65,
            'ssid': 'TestNetwork2',
            'bssid': '00:11:22:33:44:66',
            'channel': 11,
            'encryption': 'WPA3'
        }
    ]
    
    exporter = ExportFormatExpansion()
    
    # Export to different formats
    exporter.export_to_csv(sample_data, 'survey_data.csv', advanced_fields=True)
    exporter.export_to_kml(sample_data, 'survey_data.kml')
    exporter.export_to_geojson(sample_data, 'survey_data.geojson')
    
    logger.info("Exported data to multiple formats")

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Run examples
    example_stream_processing()
    example_export_formats()
