# PiWardrive User Manual

## Table of Contents
- [Getting Started](#getting-started)
- [Dashboard Overview](#dashboard-overview)
- [Wi-Fi Scanning](#wi-fi-scanning)
- [Network Analysis](#network-analysis)
- [Device Detection](#device-detection)
- [Real-Time Monitoring](#real-time-monitoring)
- [Data Export](#data-export)
- [System Management](#system-management)
- [Settings & Configuration](#settings--configuration)
- [Troubleshooting](#troubleshooting)
- [Keyboard Shortcuts](#keyboard-shortcuts)
- [Mobile Interface](#mobile-interface)

## Getting Started

### First Login

1. **Access the Dashboard**
   - Open your web browser
   - Navigate to `http://your-pi-ip:8000`
   - Default address: `http://localhost:8000` (if accessing locally)

2. **Login Credentials**
   - **Username**: `admin`
   - **Password**: `piwardrive123`
   - ⚠️ **Change the default password immediately** after first login

3. **Initial Setup Wizard**
   - Select your Wi-Fi adapter for scanning
   - Configure GPS settings (if available)
   - Set your timezone and location
   - Choose default scan parameters

### Dashboard Layout

The PiWardrive interface consists of several main sections:

- **Navigation Bar** - Access main features and system status
- **Real-Time Panel** - Live scanning data and current activity
- **Data Visualization** - Charts, graphs, and network maps
- **Control Panel** - Start/stop scans and configure settings
- **Status Bar** - System health and connection information

## Dashboard Overview

### Main Navigation

#### 🏠 Home
- **Live Dashboard** - Real-time scanning overview
- **Quick Stats** - Network count, device count, signal strength
- **Recent Activity** - Latest detected networks and devices
- **System Status** - Hardware health and service status

#### 📡 Wi-Fi Scanner
- **Active Scanning** - Start and control Wi-Fi scans
- **Scan Results** - View detected networks and access points
- **Channel Analysis** - Frequency usage and interference
- **Signal Strength** - RSSI measurements and coverage maps

#### 🔍 Network Analysis
- **Network Details** - In-depth information about detected networks
- **Security Analysis** - Encryption types and security assessment
- **Vendor Information** - Device manufacturer identification
- **Historical Data** - Network presence over time

#### 📱 Device Detection
- **Connected Devices** - Clients associated with access points
- **Device Tracking** - MAC address monitoring and tracking
- **Probe Requests** - Device search behavior analysis
- **Device Fingerprinting** - OS and device type identification

#### 📊 Analytics
- **Data Visualization** - Interactive charts and graphs
- **Trend Analysis** - Network activity patterns over time
- **Heatmaps** - Signal strength and coverage visualization
- **Reports** - Automated analysis and summaries

#### ⚙️ System
- **Settings** - Configuration and preferences
- **System Status** - Hardware monitoring and diagnostics
- **Log Viewer** - System and application logs
- **User Management** - Account settings and permissions

### Status Indicators

#### Connection Status
- 🟢 **Connected** - System operational and scanning
- 🟡 **Connecting** - Initializing hardware or services
- 🔴 **Disconnected** - Hardware issues or service offline
- ⚪ **Disabled** - Scanning stopped by user

#### Scan Status
- ▶️ **Active** - Currently scanning for networks
- ⏸️ **Paused** - Scanning temporarily stopped
- ⏹️ **Stopped** - No active scanning
- 🔄 **Initializing** - Preparing hardware for scanning

#### System Health
- 💚 **Healthy** - All systems operating normally
- 💛 **Warning** - Minor issues detected
- ❤️ **Critical** - Serious problems requiring attention
- 💔 **Error** - System malfunction or failure

## Wi-Fi Scanning

### Starting a Scan

1. **Navigate to Wi-Fi Scanner**
   - Click the 📡 Wi-Fi Scanner tab in the navigation

2. **Choose Scan Type**
   - **Quick Scan** - Fast overview of nearby networks (30 seconds)
   - **Standard Scan** - Comprehensive scan with detailed analysis (5 minutes)
   - **Deep Scan** - Extended monitoring for intermittent networks (30 minutes)
   - **Custom Scan** - User-defined parameters and duration

3. **Configure Scan Parameters**
   ```
   Scan Duration: 5 minutes
   Channel Range: All channels (1-165)
   Scan Interval: 1 second
   Monitor Mode: Enabled
   ```

4. **Start Scanning**
   - Click the ▶️ **Start Scan** button
   - Monitor progress in the real-time panel
   - View results as they appear

### Scan Configuration

#### Channel Selection
- **2.4 GHz Channels**: 1-14 (availability varies by region)
- **5 GHz Channels**: 36, 40, 44, 48, 52, 56, 60, 64, 100-165
- **6 GHz Channels**: 1, 5, 9, 13, 17, 21, 25, 29, 33 (Wi-Fi 6E)

#### Scan Modes
- **Passive Scanning** - Listen-only mode (stealth)
- **Active Scanning** - Send probe requests (faster detection)
- **Monitor Mode** - Capture all wireless traffic (most comprehensive)

#### Advanced Options
```yaml
Scan Settings:
  Channel Hopping: Enabled
  Hop Interval: 250ms
  Dwell Time: 100ms per channel
  Retry Attempts: 3
  Signal Threshold: -90 dBm
  Vendor Detection: Enabled
```

### Understanding Scan Results

#### Network Information
- **SSID** - Network name (may be hidden)
- **BSSID** - MAC address of access point
- **Channel** - Operating frequency channel
- **Signal Strength** - RSSI in dBm (-30 to -90 typical)
- **Security** - Encryption type (Open, WEP, WPA/WPA2/WPA3)
- **Vendor** - Access point manufacturer

#### Signal Quality Indicators
- **Excellent**: -30 to -50 dBm (🟢 Green)
- **Good**: -51 to -60 dBm (🟡 Yellow)  
- **Fair**: -61 to -70 dBm (🟠 Orange)
- **Poor**: -71 to -85 dBm (🔴 Red)
- **Weak**: Below -85 dBm (⚫ Gray)

#### Security Assessment
- 🔓 **Open** - No encryption (security risk)
- 🔐 **WEP** - Legacy encryption (easily broken)
- 🛡️ **WPA/WPA2** - Standard security (secure if properly configured)
- 🔒 **WPA3** - Latest security standard (most secure)
- ⚠️ **Unknown** - Unable to determine security type

## Network Analysis

### Network Details View

#### Basic Information
```
Network: MyWiFiNetwork
BSSID: AA:BB:CC:DD:EE:FF
Channel: 6 (2.437 GHz)
Signal: -45 dBm (Excellent)
Security: WPA2-PSK (AES)
Vendor: Cisco Systems
First Seen: 2024-01-15 10:30:25
Last Seen: 2024-01-15 14:22:18
```

#### Advanced Properties
- **Beacon Interval** - Time between beacon frames
- **Supported Rates** - Data transmission speeds
- **Capabilities** - Feature support (802.11n/ac/ax)
- **Country Code** - Regulatory domain
- **Channel Width** - 20/40/80/160 MHz
- **DTIM Period** - Power management settings

### Security Analysis

#### Encryption Assessment
1. **Open Networks**
   - No password required
   - All traffic transmitted in clear text
   - High security risk

2. **WEP Networks**
   - Legacy 64/128-bit encryption
   - Easily crackable within minutes
   - Should be avoided

3. **WPA/WPA2 Networks**
   - Strong encryption when properly configured
   - Vulnerable to dictionary attacks if weak password
   - Look for WPA2-Enterprise for business use

4. **WPA3 Networks**
   - Latest security standard
   - Protection against offline attacks
   - Enhanced security features

#### Vulnerability Indicators
- ⚠️ **Weak Password** - Default or common passwords detected
- 🚨 **WPS Enabled** - PIN-based setup vulnerability
- 🔓 **Guest Network** - Open or weakly secured guest access
- 📡 **Hidden SSID** - Network name not broadcast (false security)

### Vendor Analysis

#### Manufacturer Identification
PiWardrive identifies device manufacturers using:
- **OUI Database** - IEEE organizationally unique identifiers
- **Fingerprinting** - Device-specific characteristics
- **Beacon Analysis** - Vendor-specific information elements

#### Common Vendors
- **Cisco** - Enterprise networking equipment
- **Netgear** - Consumer routers and access points
- **TP-Link** - Budget-friendly networking devices
- **Ubiquiti** - Professional wireless solutions
- **Apple** - Airport and Time Capsule devices
- **ASUS** - Gaming and high-performance routers

## Device Detection

### Connected Devices

#### Device Discovery
PiWardrive detects devices through:
- **Association Frames** - Devices connecting to networks
- **Probe Requests** - Devices searching for known networks
- **Data Frames** - Active communication analysis
- **Management Frames** - Network maintenance traffic

#### Device Information
```
Device: iPhone-John
MAC Address: 12:34:56:78:9A:BC
Vendor: Apple Inc.
Connected to: HomeNetwork_5G
Signal Strength: -38 dBm
First Seen: 2024-01-15 09:15:32
Last Activity: 2024-01-15 14:20:45
Device Type: Mobile Phone
OS Fingerprint: iOS 17.x
```

### Device Tracking

#### Privacy Considerations
Modern devices use **MAC randomization** to protect privacy:
- **Random MAC** - Changes periodically to prevent tracking
- **Local Bit Set** - Indicates randomized address
- **OUI Patterns** - Some vendors use recognizable patterns

#### Tracking Methods
1. **MAC Address Monitoring**
   - Track devices with static MAC addresses
   - Identify patterns in randomized addresses
   - Cross-reference with vendor databases

2. **Probe Request Analysis**
   - Monitor networks devices search for
   - Identify home/work location patterns
   - Track device movement between areas

3. **Timing Analysis**
   - Correlate device appearance patterns
   - Identify regular schedules and routines
   - Associate multiple MAC addresses to same device

### Device Fingerprinting

#### Operating System Detection
- **iOS Devices** - iPhone, iPad characteristics
- **Android Devices** - Various manufacturer signatures
- **Windows** - Laptop and desktop patterns
- **macOS** - MacBook and iMac indicators
- **Linux** - Various distribution signatures

#### Device Type Classification
- 📱 **Mobile Phones** - Smartphones and cellular devices
- 💻 **Laptops** - Portable computers
- 🖥️ **Desktops** - Stationary computers
- 📺 **Smart TVs** - Internet-connected televisions
- 🏠 **IoT Devices** - Smart home and connected devices
- 🎮 **Gaming Consoles** - PlayStation, Xbox, Nintendo
- ⌚ **Wearables** - Smartwatches and fitness trackers

## Real-Time Monitoring

### Live Dashboard

#### Real-Time Updates
The dashboard updates automatically every few seconds with:
- **New Networks** - Recently discovered access points
- **Signal Changes** - RSSI fluctuations and coverage
- **Device Activity** - Connections and disconnections
- **Channel Usage** - Frequency utilization changes

#### Streaming Data
- **WebSocket Connection** - Real-time data streaming
- **Auto-Refresh** - Fallback for compatibility
- **Buffer Management** - Prevents memory overflow
- **Error Recovery** - Automatic reconnection

### Live Visualization

#### Signal Strength Graph
- **Time Series** - Signal levels over time
- **Multiple Networks** - Compare signal strength
- **Threshold Lines** - Quality indicators
- **Zoom and Pan** - Detailed time range analysis

#### Channel Utilization
- **Spectrum View** - Visual frequency usage
- **Interference Detection** - Overlapping channels
- **Congestion Analysis** - High-traffic areas
- **Optimization Suggestions** - Better channel selection

#### Device Count Timeline
- **Connected Devices** - Active associations
- **Total Devices** - All detected devices
- **New Devices** - Recently appeared
- **Device Patterns** - Usage trends

### Alerts and Notifications

#### Notification Types
- 🆕 **New Network** - Previously unseen access point
- 📶 **Signal Change** - Significant RSSI variation
- 🔐 **Security Alert** - Open or vulnerable network
- 👤 **New Device** - Unknown device detected
- ⚠️ **System Warning** - Hardware or software issues

#### Alert Configuration
```yaml
Alerts:
  New Networks: Enabled
  Signal Threshold: -75 dBm
  Device Tracking: Enabled
  Security Warnings: Enabled
  System Health: Enabled
```

## Data Export

### Export Formats

#### CSV (Comma-Separated Values)
```csv
timestamp,ssid,bssid,channel,signal_strength,security,vendor
2024-01-15 14:30:00,HomeNetwork,AA:BB:CC:DD:EE:FF,6,-45,WPA2,Netgear
2024-01-15 14:30:01,OfficeWiFi,11:22:33:44:55:66,11,-52,WPA3,Cisco
```

#### JSON (JavaScript Object Notation)
```json
{
  "export_time": "2024-01-15T14:30:00Z",
  "scan_duration": 300,
  "networks": [
    {
      "ssid": "HomeNetwork",
      "bssid": "AA:BB:CC:DD:EE:FF",
      "channel": 6,
      "signal_strength": -45,
      "security": "WPA2",
      "vendor": "Netgear",
      "first_seen": "2024-01-15T14:25:00Z",
      "last_seen": "2024-01-15T14:30:00Z"
    }
  ]
}
```

#### XML (Extensible Markup Language)
```xml
<?xml version="1.0" encoding="UTF-8"?>
<scan_results>
  <metadata>
    <export_time>2024-01-15T14:30:00Z</export_time>
    <scan_duration>300</scan_duration>
  </metadata>
  <networks>
    <network>
      <ssid>HomeNetwork</ssid>
      <bssid>AA:BB:CC:DD:EE:FF</bssid>
      <channel>6</channel>
      <signal_strength>-45</signal_strength>
      <security>WPA2</security>
      <vendor>Netgear</vendor>
    </network>
  </networks>
</scan_results>
```

#### SQLite Database
- **Complete Schema** - All data with relationships
- **Query Interface** - Direct SQL access
- **Portable Format** - Single file database
- **Tool Compatibility** - Works with many analysis tools

### Export Options

#### Data Selection
- **Time Range** - Specific date/time periods
- **Network Filter** - Include/exclude specific SSIDs
- **Signal Threshold** - Minimum signal strength
- **Security Type** - Filter by encryption type
- **Device Data** - Include associated devices

#### Scheduled Exports
```yaml
Export Schedule:
  Daily Reports: 06:00 UTC
  Weekly Summary: Sunday 00:00 UTC
  Monthly Archive: 1st of month
  Format: JSON + CSV
  Retention: 90 days
```

### Data Analysis Tools

#### Recommended Software
- **Wireshark** - Network protocol analyzer
- **Excel/LibreOffice** - Spreadsheet analysis
- **Python/Pandas** - Data science and analysis
- **R Statistical Software** - Advanced statistics
- **Tableau/Power BI** - Business intelligence visualization
- **QGIS** - Geographic information systems (with GPS data)

#### Analysis Examples
1. **Coverage Mapping** - Signal strength heatmaps
2. **Interference Analysis** - Channel overlap detection
3. **Capacity Planning** - Network utilization trends
4. **Security Assessment** - Vulnerability identification
5. **Device Tracking** - Movement pattern analysis

## System Management

### User Management

#### Account Types
- **Administrator** - Full system access and configuration
- **Operator** - Scanning and viewing permissions
- **Viewer** - Read-only access to data and reports
- **Guest** - Limited access to live dashboard only

#### User Operations
1. **Add New User**
   - Navigate to System → User Management
   - Click "Add User" button
   - Fill in username, password, and role
   - Set permissions and access levels

2. **Modify User Permissions**
   - Select user from list
   - Edit role assignments
   - Configure feature access
   - Save changes

3. **Password Management**
   - Require strong passwords
   - Set expiration policies
   - Enable two-factor authentication (if configured)

### System Monitoring

#### Performance Metrics
- **CPU Usage** - Processor utilization
- **Memory Usage** - RAM consumption
- **Disk Space** - Storage utilization
- **Network Traffic** - Data throughput
- **Temperature** - Hardware thermal status

#### Service Status
- **PiWardrive API** - Main application service
- **Database** - Data storage system
- **Wi-Fi Interface** - Hardware adapter status
- **GPS Service** - Location services (if available)
- **Web Server** - Dashboard interface

#### Log Management
- **Application Logs** - PiWardrive operations
- **System Logs** - Operating system events
- **Error Logs** - Problem diagnosis
- **Access Logs** - User activity tracking
- **Audit Logs** - Security and compliance

### Backup and Restore

#### Automatic Backups
```yaml
Backup Configuration:
  Schedule: Daily at 02:00
  Retention: 30 days
  Include:
    - Database
    - Configuration files
    - User settings
    - Scan data
  Exclude:
    - Temporary files
    - Cache data
    - Log files
```

#### Manual Backup
1. **Navigate to System → Backup**
2. **Select Backup Type**
   - Full Backup (all data)
   - Configuration Only
   - Data Only
3. **Choose Export Format**
   - Compressed archive (.tar.gz)
   - Encrypted backup (.enc)
4. **Download or Save to External Storage**

#### Restore Process
1. **Stop PiWardrive Services**
2. **Upload Backup File**
3. **Select Restore Options**
4. **Verify Data Integrity**
5. **Restart Services**

## Settings & Configuration

### General Settings

#### System Preferences
```yaml
General:
  Timezone: UTC
  Date Format: YYYY-MM-DD
  Time Format: 24-hour
  Language: English
  Theme: Dark
  Auto-refresh: 5 seconds
```

#### Dashboard Layout
- **Panel Arrangement** - Customize widget positions
- **Default Views** - Set startup page and layout
- **Color Scheme** - Choose interface theme
- **Data Density** - Adjust information display

### Wi-Fi Configuration

#### Hardware Settings
```yaml
Wi-Fi Adapter:
  Interface: wlan1
  Driver: rtl8812au
  Monitor Mode: Enabled
  Antenna: External
  Power Level: 20 dBm
```

#### Scanning Parameters
```yaml
Scan Configuration:
  Default Duration: 300 seconds
  Channel Hopping: Enabled
  Hop Interval: 250ms
  Signal Threshold: -90 dBm
  Retry Attempts: 3
  Vendor Detection: Enabled
```

#### Channel Configuration
- **2.4 GHz Channels** - Select specific channels to scan
- **5 GHz Channels** - Configure band preferences
- **6 GHz Channels** - Wi-Fi 6E support (if available)
- **Custom Frequencies** - Advanced frequency selection

### Database Settings

#### Storage Configuration
```yaml
Database:
  Type: SQLite
  Location: /var/lib/piwardrive/piwardrive.db
  Max Size: 10 GB
  Backup: Enabled
  Retention: 90 days
```

#### Performance Tuning
- **Connection Pool** - Optimize database connections
- **Query Timeout** - Set maximum query duration
- **Index Optimization** - Improve search performance
- **Cleanup Schedule** - Automatic data maintenance

### Security Settings

#### Authentication
- **Password Policy** - Minimum length and complexity
- **Session Timeout** - Automatic logout duration
- **Two-Factor Authentication** - Additional security layer
- **API Keys** - Programmatic access tokens

#### Access Control
- **IP Restrictions** - Limit access by source address
- **Role-Based Permissions** - Fine-grained access control
- **Audit Logging** - Track user activities
- **Failed Login Protection** - Prevent brute force attacks

### Network Settings

#### Interface Configuration
```yaml
Network:
  Management Interface: eth0
  IP Address: DHCP
  DNS Servers: 8.8.8.8, 8.8.4.4
  NTP Server: pool.ntp.org
  Proxy: None
```

#### Firewall Rules
- **Allowed Ports** - 8000 (HTTP), 22 (SSH)
- **Blocked Services** - Unnecessary network services
- **Rate Limiting** - Prevent abuse and DoS attacks
- **Geographic Restrictions** - Block by country (optional)

## Troubleshooting

### Common Issues

#### 1. Wi-Fi Adapter Not Detected
**Symptoms:**
- No scanning interface available
- "Hardware not found" error
- Empty adapter dropdown

**Solutions:**
1. **Check Physical Connection**
   ```bash
   lsusb  # Verify USB adapter is detected
   dmesg | grep -i wifi  # Check kernel messages
   ```

2. **Verify Driver Installation**
   ```bash
   lsmod | grep -i wireless  # Check loaded drivers
   iwconfig  # List wireless interfaces
   ```

3. **Test Monitor Mode**
   ```bash
   sudo airmon-ng check kill  # Stop conflicting processes
   sudo airmon-ng start wlan1  # Enable monitor mode
   ```

#### 2. No Networks Detected
**Symptoms:**
- Scan completes with zero results
- Empty network list
- "No data available" message

**Solutions:**
1. **Check Antenna Connection**
   - Ensure external antenna is properly connected
   - Test with different antenna orientation
   - Move to area with known Wi-Fi networks

2. **Verify Channel Configuration**
   - Enable all channels in settings
   - Check regional frequency restrictions
   - Test with specific known channels

3. **Signal Threshold Adjustment**
   - Lower signal threshold in settings
   - Try different scan durations
   - Check for interference sources

#### 3. Poor Performance
**Symptoms:**
- Slow page loading
- Delayed updates
- System freezing

**Solutions:**
1. **Check System Resources**
   ```bash
   htop  # Monitor CPU and memory usage
   df -h  # Check disk space
   iotop  # Monitor disk I/O
   ```

2. **Optimize Database**
   - Run database cleanup
   - Adjust retention policies
   - Consider SSD storage upgrade

3. **Network Optimization**
   - Use wired connection for management
   - Reduce scan frequency
   - Limit concurrent operations

#### 4. Login Issues
**Symptoms:**
- "Invalid credentials" error
- Account locked message
- Authentication failures

**Solutions:**
1. **Reset Password**
   ```bash
   # Access Pi directly via SSH
   python3 -m piwardrive.auth.reset_password admin
   ```

2. **Check Account Status**
   - Verify account is not locked
   - Check password expiration
   - Review failed login attempts

3. **Clear Browser Data**
   - Clear cookies and cache
   - Try incognito/private mode
   - Test with different browser

### Diagnostic Tools

#### System Health Check
Navigate to **System → Diagnostics** for automated checks:
- ✅ **Hardware Detection** - Wi-Fi adapter and GPS
- ✅ **Service Status** - All required services running
- ✅ **Database Connectivity** - Data storage accessible
- ✅ **Network Configuration** - Proper interface setup
- ✅ **Permission Check** - Correct file and directory permissions

#### Log Analysis
**Application Logs:**
```bash
# View recent application logs
tail -f /var/log/piwardrive/application.log

# Search for errors
grep -i error /var/log/piwardrive/*.log

# Check specific time period
journalctl -u piwardrive --since "1 hour ago"
```

**System Logs:**
```bash
# Hardware detection issues
dmesg | grep -i usb
dmesg | grep -i wifi

# Service problems
systemctl status piwardrive
systemctl status gpsd
```

#### Network Diagnostics
```bash
# Test interface configuration
ip link show
iwconfig

# Check monitor mode capability
iw list | grep -A 8 "Supported interface modes"

# Test packet capture
tcpdump -i wlan1mon -c 10
```

## Keyboard Shortcuts

### Global Shortcuts
- **Ctrl + R** - Refresh current page
- **Ctrl + F** - Open search/filter
- **Ctrl + S** - Save current view/export data
- **Ctrl + H** - Return to dashboard home
- **Esc** - Close modal dialogs
- **F11** - Toggle fullscreen mode
- **F5** - Force refresh all data

### Navigation Shortcuts
- **Alt + 1** - Dashboard home
- **Alt + 2** - Wi-Fi scanner
- **Alt + 3** - Network analysis
- **Alt + 4** - Device detection
- **Alt + 5** - Analytics
- **Alt + 6** - System settings

### Scanning Shortcuts
- **Space** - Start/stop current scan
- **Ctrl + N** - New scan configuration
- **Ctrl + P** - Pause/resume scanning
- **Ctrl + E** - Export current results
- **Ctrl + D** - Download scan data

### Table Navigation
- **↑/↓** - Navigate rows
- **Ctrl + ↑/↓** - Jump to first/last row
- **Page Up/Down** - Scroll by page
- **Home/End** - Go to beginning/end
- **Enter** - View details
- **Delete** - Remove selected item (if permitted)

## Mobile Interface

### Responsive Design
The PiWardrive interface automatically adapts to different screen sizes:
- **Desktop** (1920px+) - Full feature layout
- **Tablet** (768-1919px) - Optimized two-column layout
- **Mobile** (320-767px) - Single-column mobile layout

### Touch Gestures
- **Tap** - Select item or activate button
- **Double Tap** - Open detailed view
- **Swipe Left/Right** - Navigate between pages
- **Swipe Up/Down** - Scroll content
- **Pinch Zoom** - Scale charts and maps
- **Long Press** - Context menu (where available)

### Mobile Features
- **Optimized Tables** - Horizontal scrolling for large datasets
- **Touch-Friendly Buttons** - Larger tap targets
- **Simplified Navigation** - Collapsible menu system
- **Reduced Data Usage** - Optimized for mobile connections
- **Offline Indicators** - Clear connection status

### Performance on Mobile
- **Reduced Polling** - Less frequent updates to save battery
- **Lazy Loading** - Load data as needed
- **Image Optimization** - Compressed graphics for faster loading
- **Cached Resources** - Store static files locally

---

**Need More Help?**
- 📖 **Documentation**: [docs/](../docs/)
- 💬 **Community**: [GitHub Discussions](https://github.com/username/piwardrive/discussions)
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/username/piwardrive/issues)
- 📧 **Support**: support@piwardrive.com
