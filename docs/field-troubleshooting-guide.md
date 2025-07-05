# Field Troubleshooting Guide - PiWardrive

## 🚨 Emergency Quick Reference

### System Status Indicators

#### LED Status Codes
- **Solid Green**: System running normally
- **Blinking Green**: System starting up
- **Solid Red**: Critical error - system not functional
- **Blinking Red**: Warning - system functional but needs attention
- **Solid Blue**: System in diagnostic mode
- **Blinking Blue**: Network connectivity issues
- **Solid Yellow**: GPS/location services unavailable
- **Blinking Yellow**: Storage space low

#### Audio Alerts
- **Single Beep**: System startup complete
- **Double Beep**: Warning condition
- **Triple Beep**: Error condition
- **Continuous Beeping**: Critical failure

### Quick Fixes - Try These First

#### 1. Power Issues
**Problem**: Device won't turn on or keeps shutting down
**Solutions**:
1. Check power cable connection
2. Try different power adapter (5V, 3A minimum)
3. Check for loose connections
4. Let device cool down if overheating

#### 2. Network Issues
**Problem**: Can't access web interface or no data collection
**Solutions**:
1. Check Wi-Fi connection on your phone/laptop
2. Try accessing via IP address: http://192.168.1.XXX:8000
3. Restart network: Hold reset button for 5 seconds
4. Move closer to Wi-Fi router

#### 3. GPS Issues
**Problem**: No location data or maps not loading
**Solutions**:
1. Move device outdoors or near window
2. Wait 2-5 minutes for GPS lock
3. Check GPS antenna connection
4. Restart GPS service: Hold GPS button for 3 seconds

#### 4. Storage Issues
**Problem**: System slow or not recording data
**Solutions**:
1. Check storage indicator light
2. Insert fresh SD card or USB drive
3. Clear old data via web interface
4. Restart system

## 🔧 Step-by-Step Troubleshooting

### Before You Start
1. **Safety First**: Power off device before checking connections
2. **Have Ready**: Spare SD card, USB cable, network cable
3. **Document**: Note error messages or LED patterns
4. **Backup**: Save important data if possible

### Common Problems and Solutions

#### Problem: Web Interface Not Loading

**Symptoms**:
- Browser shows "Page not found" or "Connection refused"
- LED shows blinking blue
- Can't access http://piwardrive.local

**Step-by-Step Fix**:
1. **Check Power**
   - Ensure solid green LED (system running)
   - If red LED, check power supply and connections

2. **Check Network**
   - Connect device directly to router with Ethernet cable
   - Wait 2 minutes for network setup
   - Try accessing via IP: http://192.168.1.XXX:8000

3. **Find Device IP**
   - On Windows: Open Command Prompt, type `arp -a`
   - On Mac/Linux: Type `arp -a` in Terminal
   - Look for device with name containing "piwardrive"

4. **Reset Network**
   - Hold network reset button for 5 seconds
   - Wait 3 minutes for restart
   - Try accessing again

#### Problem: No GPS Data

**Symptoms**:
- Map shows no location
- Yellow LED (solid or blinking)
- Location shows "Unknown" in interface

**Step-by-Step Fix**:
1. **Check GPS Connection**
   - Ensure GPS antenna is connected
   - Check antenna cable for damage
   - Verify antenna has clear view of sky

2. **Wait for GPS Lock**
   - GPS can take 2-15 minutes for first lock
   - Keep device stationary during initial setup
   - Best results outdoors with clear sky view

3. **Check GPS Service**
   - Access web interface
   - Go to Settings → GPS
   - Ensure GPS is enabled
   - Try "Reset GPS" button

#### Problem: No Data Collection

**Symptoms**:
- Interface loads but shows no scan results
- No wireless networks detected
- Empty data tables

**Step-by-Step Fix**:
1. **Check Wi-Fi Adapter**
   - Ensure external Wi-Fi adapter is connected
   - Try different USB port
   - Check for physical damage

2. **Restart Services**
   - Go to Settings → Services
   - Click "Restart All Services"
   - Wait 2 minutes for restart

3. **Check Storage**
   - Ensure SD card or USB drive is inserted
   - Check storage space in Settings
   - Try different storage device

#### Problem: System Overheating

**Symptoms**:
- Device feels very hot
- Frequent shutdowns
- Performance degradation

**Step-by-Step Fix**:
1. **Immediate Actions**
   - Turn off device and let cool
   - Check for blocked ventilation
   - Ensure fan is working (if equipped)

2. **Environmental Check**
   - Move away from heat sources
   - Ensure adequate airflow
   - Check ambient temperature

3. **Long-term Solutions**
   - Add cooling fan or heat sink
   - Reduce processing load in settings
   - Consider weatherproof enclosure

### Advanced Troubleshooting

#### System Recovery Mode
If system won't start normally:
1. Hold power button for 10 seconds while powering on
2. System will boot into recovery mode (blue LED)
3. Access recovery interface at http://192.168.1.100:8080
4. Follow recovery wizard

#### Factory Reset
**Warning**: This will erase all data and settings
1. Power off device
2. Hold reset button while powering on
3. Keep holding for 15 seconds
4. Release when LED turns solid blue
5. Wait 5 minutes for complete reset

#### Safe Mode
For troubleshooting software issues:
1. Power off device
2. Hold diagnostic button while powering on
3. Release when LED blinks blue rapidly
4. System starts with minimal features
5. Access diagnostic interface for troubleshooting

## 📞 Getting Help

### Before Contacting Support
Gather this information:
- Device model and serial number
- LED status pattern
- Error messages from web interface
- What you were doing when problem occurred
- Steps already tried

### Self-Service Resources
- **Device Status**: Check Settings → System Status
- **Log Files**: Download from Settings → Diagnostics
- **Update Check**: Settings → System Updates
- **Reset Options**: Settings → Factory Reset

### Remote Assistance
If your device is connected to the internet:
1. Go to Settings → Remote Support
2. Generate support code
3. Provide code to technical support
4. Support can diagnose remotely

### Emergency Contacts
- **Technical Support**: support@piwardrive.com
- **Emergency Hotline**: 1-800-PIWAR-HELP
- **Online Chat**: piwardrive.com/support
- **Community Forum**: community.piwardrive.com

## 🔧 Field Serviceable Components

### What You Can Replace in the Field

#### SD Card/Storage
- **Symptom**: Storage full or corrupted
- **Replacement**: Insert new SD card (32GB+ recommended)
- **Location**: Side panel slot
- **Tools**: None required

#### Wi-Fi Adapter
- **Symptom**: No wireless scanning
- **Replacement**: Compatible USB Wi-Fi adapter
- **Location**: USB port
- **Tools**: None required

#### GPS Antenna
- **Symptom**: No GPS signal
- **Replacement**: External GPS antenna
- **Location**: SMA connector
- **Tools**: None required

#### Power Supply
- **Symptom**: Won't power on
- **Replacement**: 5V/3A power adapter
- **Connection**: USB-C or barrel connector
- **Tools**: None required

### What Requires Professional Service

#### Internal Components
- Main board failures
- Internal antenna issues
- Display problems
- Cooling system failures

#### Enclosure Damage
- Cracked housing
- Damaged connectors
- Water damage
- Impact damage

## 📋 Maintenance Schedule

### Daily Checks
- Verify LED status indicators
- Check web interface accessibility
- Monitor storage space
- Verify GPS lock

### Weekly Maintenance
- Clean external surfaces
- Check cable connections
- Review system logs
- Update data backups

### Monthly Maintenance
- Check for system updates
- Clean internal fans/vents
- Verify all services running
- Test emergency procedures

### Quarterly Maintenance
- Full system diagnostic
- Replace air filters
- Check battery backup
- Review configuration settings

### Annual Maintenance
- Professional service inspection
- Replace wearing components
- Update documentation
- Review deployment effectiveness

## 🛠️ Emergency Procedures

### Power Loss Recovery
1. Wait for automatic restart (2-3 minutes)
2. Check LED status upon restart
3. Verify all services running
4. Check data integrity

### Network Outage Recovery
1. System continues local operation
2. Data cached locally
3. Automatic sync when network restored
4. Check sync status in interface

### Storage Failure Recovery
1. System alerts via LED/audio
2. Insert backup storage device
3. System automatically switches
4. Recover data from backup

### Complete System Failure
1. Document failure conditions
2. Power cycle device
3. Try safe mode boot
4. If unsuccessful, contact support
5. Prepare backup device for deployment

## 📱 Mobile Diagnostic App

### Quick Diagnostics
Use the PiWardrive Mobile App for:
- Device discovery and status
- Remote diagnostics
- Log file retrieval
- Emergency shutdown
- Configuration backup

### App Installation
- iOS: Search "PiWardrive Tech" in App Store
- Android: Download from Google Play Store
- Web: diagnostic.piwardrive.com

---

*This guide covers the most common field issues. For complex problems or hardware failures, contact technical support for professional assistance.*
