# Enhanced Database Schema for PiWardrive War-Driving Analysis

## 1. Core Scanning Tables

### scan_sessions table
```sql
CREATE TABLE scan_sessions (
    id TEXT PRIMARY KEY,
    device_id TEXT NOT NULL,
    scan_type TEXT NOT NULL, -- 'wifi', 'bluetooth', 'cellular', 'combined'
    started_at TIMESTAMP NOT NULL,
    completed_at TIMESTAMP,
    duration_seconds INTEGER,
    location_start_lat REAL,
    location_start_lon REAL,
    location_end_lat REAL,
    location_end_lon REAL,
    interface_used TEXT,
    scan_parameters TEXT, -- JSON configuration
    total_detections INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_scan_sessions_device_time ON scan_sessions(device_id, started_at);
CREATE INDEX idx_scan_sessions_type ON scan_sessions(scan_type);
CREATE INDEX idx_scan_sessions_location ON scan_sessions(location_start_lat, location_start_lon);
```

### wifi_detections table (Enhanced)
```sql
CREATE TABLE wifi_detections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scan_session_id TEXT NOT NULL,
    detection_timestamp TIMESTAMP NOT NULL,
    bssid TEXT NOT NULL,
    ssid TEXT,
    channel INTEGER,
    frequency_mhz INTEGER,
    signal_strength_dbm INTEGER,
    noise_floor_dbm INTEGER,
    snr_db INTEGER,
    encryption_type TEXT,
    cipher_suite TEXT,
    authentication_method TEXT,
    wps_enabled BOOLEAN DEFAULT FALSE,
    vendor_oui TEXT,
    vendor_name TEXT,
    device_type TEXT, -- router, mobile, iot, etc.
    latitude REAL,
    longitude REAL,
    altitude_meters REAL,
    accuracy_meters REAL,
    heading_degrees REAL,
    speed_kmh REAL,
    beacon_interval_ms INTEGER,
    dtim_period INTEGER,
    ht_capabilities TEXT, -- JSON
    vht_capabilities TEXT, -- JSON
    he_capabilities TEXT, -- JSON (WiFi 6)
    country_code TEXT,
    regulatory_domain TEXT,
    tx_power_dbm INTEGER,
    load_percentage INTEGER,
    station_count INTEGER,
    data_rates TEXT, -- JSON array
    first_seen TIMESTAMP NOT NULL,
    last_seen TIMESTAMP NOT NULL,
    detection_count INTEGER DEFAULT 1,
    FOREIGN KEY (scan_session_id) REFERENCES scan_sessions(id)
);

-- Critical indexes for analysis
CREATE INDEX idx_wifi_detections_session ON wifi_detections(scan_session_id);
CREATE INDEX idx_wifi_detections_bssid ON wifi_detections(bssid);
CREATE INDEX idx_wifi_detections_ssid ON wifi_detections(ssid);
CREATE INDEX idx_wifi_detections_time ON wifi_detections(detection_timestamp);
CREATE INDEX idx_wifi_detections_location ON wifi_detections(latitude, longitude);
CREATE INDEX idx_wifi_detections_signal ON wifi_detections(signal_strength_dbm);
CREATE INDEX idx_wifi_detections_channel ON wifi_detections(channel);
CREATE INDEX idx_wifi_detections_encryption ON wifi_detections(encryption_type);
CREATE INDEX idx_wifi_detections_vendor ON wifi_detections(vendor_name);
```

### bluetooth_detections table
```sql
CREATE TABLE bluetooth_detections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scan_session_id TEXT NOT NULL,
    detection_timestamp TIMESTAMP NOT NULL,
    mac_address TEXT NOT NULL,
    device_name TEXT,
    device_class INTEGER,
    device_type TEXT,
    manufacturer_id INTEGER,
    manufacturer_name TEXT,
    rssi_dbm INTEGER,
    tx_power_dbm INTEGER,
    bluetooth_version TEXT,
    supported_services TEXT, -- JSON array
    is_connectable BOOLEAN DEFAULT FALSE,
    is_paired BOOLEAN DEFAULT FALSE,
    latitude REAL,
    longitude REAL,
    altitude_meters REAL,
    accuracy_meters REAL,
    heading_degrees REAL,
    speed_kmh REAL,
    first_seen TIMESTAMP NOT NULL,
    last_seen TIMESTAMP NOT NULL,
    detection_count INTEGER DEFAULT 1,
    FOREIGN KEY (scan_session_id) REFERENCES scan_sessions(id)
);

CREATE INDEX idx_bt_detections_session ON bluetooth_detections(scan_session_id);
CREATE INDEX idx_bt_detections_mac ON bluetooth_detections(mac_address);
CREATE INDEX idx_bt_detections_time ON bluetooth_detections(detection_timestamp);
CREATE INDEX idx_bt_detections_location ON bluetooth_detections(latitude, longitude);
CREATE INDEX idx_bt_detections_rssi ON bluetooth_detections(rssi_dbm);
```

### cellular_detections table
```sql
CREATE TABLE cellular_detections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scan_session_id TEXT NOT NULL,
    detection_timestamp TIMESTAMP NOT NULL,
    cell_id INTEGER,
    lac INTEGER, -- Location Area Code
    mcc INTEGER, -- Mobile Country Code
    mnc INTEGER, -- Mobile Network Code
    network_name TEXT,
    technology TEXT, -- GSM, UMTS, LTE, 5G
    frequency_mhz INTEGER,
    band TEXT,
    channel INTEGER,
    signal_strength_dbm INTEGER,
    signal_quality INTEGER,
    timing_advance INTEGER,
    latitude REAL,
    longitude REAL,
    altitude_meters REAL,
    accuracy_meters REAL,
    heading_degrees REAL,
    speed_kmh REAL,
    first_seen TIMESTAMP NOT NULL,
    last_seen TIMESTAMP NOT NULL,
    detection_count INTEGER DEFAULT 1,
    FOREIGN KEY (scan_session_id) REFERENCES scan_sessions(id)
);

CREATE INDEX idx_cellular_detections_session ON cellular_detections(scan_session_id);
CREATE INDEX idx_cellular_detections_cell ON cellular_detections(cell_id, lac);
CREATE INDEX idx_cellular_detections_time ON cellular_detections(detection_timestamp);
CREATE INDEX idx_cellular_detections_location ON cellular_detections(latitude, longitude);
```

## 2. GPS and Movement Tracking

### gps_tracks table
```sql
CREATE TABLE gps_tracks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scan_session_id TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    altitude_meters REAL,
    accuracy_meters REAL,
    heading_degrees REAL,
    speed_kmh REAL,
    satellite_count INTEGER,
    hdop REAL,
    vdop REAL,
    pdop REAL,
    fix_type TEXT, -- 2D, 3D, DGPS
    FOREIGN KEY (scan_session_id) REFERENCES scan_sessions(id)
);

CREATE INDEX idx_gps_tracks_session ON gps_tracks(scan_session_id);
CREATE INDEX idx_gps_tracks_time ON gps_tracks(timestamp);
CREATE INDEX idx_gps_tracks_location ON gps_tracks(latitude, longitude);
```

## 3. Analysis and Intelligence Tables

### network_fingerprints table
```sql
CREATE TABLE network_fingerprints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bssid TEXT NOT NULL,
    ssid TEXT,
    fingerprint_hash TEXT NOT NULL, -- Hash of characteristics
    confidence_score REAL,
    device_model TEXT,
    firmware_version TEXT,
    characteristics TEXT, -- JSON of technical fingerprint data
    classification TEXT, -- home, business, public, suspicious
    risk_level TEXT, -- low, medium, high, critical
    tags TEXT, -- JSON array of tags
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX idx_fingerprints_bssid ON network_fingerprints(bssid);
CREATE INDEX idx_fingerprints_hash ON network_fingerprints(fingerprint_hash);
CREATE INDEX idx_fingerprints_classification ON network_fingerprints(classification);
```

### suspicious_activities table
```sql
CREATE TABLE suspicious_activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scan_session_id TEXT NOT NULL,
    activity_type TEXT NOT NULL, -- evil_twin, deauth_attack, hidden_ssid, etc.
    severity TEXT NOT NULL, -- low, medium, high, critical
    target_bssid TEXT,
    target_ssid TEXT,
    evidence TEXT, -- JSON evidence data
    description TEXT,
    detected_at TIMESTAMP NOT NULL,
    latitude REAL,
    longitude REAL,
    false_positive BOOLEAN DEFAULT FALSE,
    analyst_notes TEXT,
    FOREIGN KEY (scan_session_id) REFERENCES scan_sessions(id)
);

CREATE INDEX idx_suspicious_session ON suspicious_activities(scan_session_id);
CREATE INDEX idx_suspicious_type ON suspicious_activities(activity_type);
CREATE INDEX idx_suspicious_severity ON suspicious_activities(severity);
CREATE INDEX idx_suspicious_time ON suspicious_activities(detected_at);
```

### network_analytics table
```sql
CREATE TABLE network_analytics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bssid TEXT NOT NULL,
    analysis_date DATE NOT NULL,
    total_detections INTEGER,
    unique_locations INTEGER,
    avg_signal_strength REAL,
    max_signal_strength REAL,
    min_signal_strength REAL,
    signal_variance REAL,
    coverage_radius_meters REAL,
    mobility_score REAL, -- 0-1, how often location changes
    encryption_changes INTEGER,
    ssid_changes INTEGER,
    channel_changes INTEGER,
    suspicious_score REAL, -- 0-1 suspicious rating
    last_analyzed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (bssid, analysis_date)
);

CREATE INDEX idx_analytics_bssid ON network_analytics(bssid);
CREATE INDEX idx_analytics_date ON network_analytics(analysis_date);
CREATE INDEX idx_analytics_suspicious ON network_analytics(suspicious_score);
```

## 4. Performance Optimizations

### Partitioning Strategy (for PostgreSQL migration)
```sql
-- Partition by month for large tables
CREATE TABLE wifi_detections_y2025m01 PARTITION OF wifi_detections
FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');

-- Partition by scan type
CREATE TABLE scan_sessions_wifi PARTITION OF scan_sessions
FOR VALUES IN ('wifi');
```

### Materialized Views for Analysis
```sql
-- Daily summary statistics
CREATE MATERIALIZED VIEW daily_detection_stats AS
SELECT 
    DATE(detection_timestamp) as detection_date,
    scan_session_id,
    COUNT(*) as total_detections,
    COUNT(DISTINCT bssid) as unique_networks,
    AVG(signal_strength_dbm) as avg_signal,
    MIN(signal_strength_dbm) as min_signal,
    MAX(signal_strength_dbm) as max_signal,
    COUNT(DISTINCT channel) as channels_used,
    COUNT(CASE WHEN encryption_type = 'OPEN' THEN 1 END) as open_networks,
    COUNT(CASE WHEN encryption_type LIKE '%WEP%' THEN 1 END) as wep_networks,
    COUNT(CASE WHEN encryption_type LIKE '%WPA%' THEN 1 END) as wpa_networks
FROM wifi_detections
GROUP BY DATE(detection_timestamp), scan_session_id;

-- Network coverage heatmap data
CREATE MATERIALIZED VIEW network_coverage_grid AS
SELECT 
    ROUND(latitude, 4) as lat_grid,
    ROUND(longitude, 4) as lon_grid,
    COUNT(*) as detection_count,
    COUNT(DISTINCT bssid) as unique_networks,
    AVG(signal_strength_dbm) as avg_signal,
    MAX(signal_strength_dbm) as max_signal
FROM wifi_detections
WHERE latitude IS NOT NULL AND longitude IS NOT NULL
GROUP BY ROUND(latitude, 4), ROUND(longitude, 4);
```

## 5. Time-Series Tables (Optional InfluxDB Integration)

### For high-frequency signal measurements
```sql
-- InfluxDB measurement schema
signal_measurements,scan_id=123,bssid=aa:bb:cc:dd:ee:ff
  signal_strength=-45i,
  noise_floor=-95i,
  snr=50i,
  channel=6i,
  latitude=40.7128,
  longitude=-74.0060
  1640995200000000000

system_metrics,device_id=pi4-001,interface=wlan0
  cpu_usage=25.5,
  memory_usage=68.2,
  temperature=42.5,
  packets_captured=1000i,
  packets_processed=950i
  1640995200000000000
```

## 6. Analysis Query Examples

### Find Evil Twin Networks
```sql
SELECT 
    ssid,
    COUNT(DISTINCT bssid) as bssid_count,
    GROUP_CONCAT(DISTINCT bssid) as bssids,
    GROUP_CONCAT(DISTINCT vendor_name) as vendors
FROM wifi_detections 
WHERE ssid IS NOT NULL 
  AND ssid != ''
GROUP BY ssid 
HAVING COUNT(DISTINCT bssid) > 1
ORDER BY bssid_count DESC;
```

### Signal Strength Analysis by Location
```sql
SELECT 
    ROUND(latitude, 3) as lat,
    ROUND(longitude, 3) as lon,
    bssid,
    ssid,
    AVG(signal_strength_dbm) as avg_signal,
    COUNT(*) as detection_count,
    MIN(detection_timestamp) as first_seen,
    MAX(detection_timestamp) as last_seen
FROM wifi_detections 
WHERE latitude IS NOT NULL 
GROUP BY ROUND(latitude, 3), ROUND(longitude, 3), bssid
ORDER BY avg_signal DESC;
```

### Network Security Analysis
```sql
SELECT 
    encryption_type,
    COUNT(*) as network_count,
    COUNT(DISTINCT vendor_name) as vendor_count,
    AVG(signal_strength_dbm) as avg_signal,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentage
FROM wifi_detections 
GROUP BY encryption_type 
ORDER BY network_count DESC;
```

### Temporal Pattern Analysis
```sql
SELECT 
    strftime('%H', detection_timestamp) as hour,
    strftime('%w', detection_timestamp) as day_of_week,
    COUNT(*) as detection_count,
    COUNT(DISTINCT bssid) as unique_networks,
    AVG(signal_strength_dbm) as avg_signal
FROM wifi_detections 
GROUP BY hour, day_of_week 
ORDER BY hour, day_of_week;
```

### Mobile Device Detection
```sql
SELECT 
    bssid,
    ssid,
    vendor_name,
    COUNT(DISTINCT ROUND(latitude,3) || ',' || ROUND(longitude,3)) as unique_locations,
    MAX(speed_kmh) as max_speed,
    AVG(signal_strength_dbm) as avg_signal,
    (MAX(detection_timestamp) - MIN(detection_timestamp)) as time_span_seconds
FROM wifi_detections 
WHERE latitude IS NOT NULL 
  AND longitude IS NOT NULL
GROUP BY bssid 
HAVING unique_locations > 5 
  OR max_speed > 10
ORDER BY unique_locations DESC, max_speed DESC;
```

## 7. Performance Indexes for Analysis

```sql
-- Composite indexes for common analysis queries
CREATE INDEX idx_wifi_time_location ON wifi_detections(detection_timestamp, latitude, longitude);
CREATE INDEX idx_wifi_signal_channel ON wifi_detections(signal_strength_dbm, channel);
CREATE INDEX idx_wifi_vendor_encryption ON wifi_detections(vendor_name, encryption_type);
CREATE INDEX idx_wifi_ssid_bssid ON wifi_detections(ssid, bssid);

-- Full-text search indexes
CREATE INDEX idx_wifi_ssid_fts ON wifi_detections USING gin(to_tsvector('english', ssid));
CREATE INDEX idx_bt_name_fts ON bluetooth_detections USING gin(to_tsvector('english', device_name));

-- Spatial indexes (PostGIS)
CREATE INDEX idx_wifi_location_spatial ON wifi_detections USING gist(ST_Point(longitude, latitude));
CREATE INDEX idx_gps_location_spatial ON gps_tracks USING gist(ST_Point(longitude, latitude));
```
