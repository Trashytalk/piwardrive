# Field Service Components Documentation

This document describes the field-serviceable components and maintenance procedures for PiWardrive devices deployed in field environments.

## Overview

PiWardrive is designed for field deployment with minimal maintenance requirements. However, certain components may need replacement or service over time. This guide identifies which components can be serviced in the field versus those requiring factory service.

## Field-Serviceable Components

### 1. Storage Devices

#### SD Card (Primary Storage)
- **Part Number**: Varies (32GB+ Class 10 UHS-I recommended)
- **Service Interval**: Replace when corrupted or every 2 years
- **Replacement Time**: 2 minutes
- **Tools Required**: None
- **Location**: Side panel slot with spring-loaded cover

**Replacement Procedure**:
1. Power down device completely
2. Wait 30 seconds for capacitors to discharge
3. Open side panel cover
4. Gently press SD card to eject
5. Insert new SD card until it clicks
6. Close side panel cover
7. Power on device

**Compatibility**:
- Minimum: 32GB Class 10
- Recommended: 64GB UHS-I U3
- Maximum: 1TB (filesystem limitations)

#### USB Storage (Secondary/Backup)
- **Part Number**: Any USB 3.0 drive
- **Service Interval**: As needed
- **Replacement Time**: 30 seconds
- **Tools Required**: None
- **Location**: Front USB port

**Replacement Procedure**:
1. Safely eject via web interface
2. Remove USB drive
3. Insert new USB drive
4. Format via web interface if needed

### 2. Network Adapters

#### Wi-Fi Adapter (External)
- **Compatible Models**:
  - Alfa AWUS036ACS (recommended)
  - Alfa AWUS036NHA
  - Panda PAU09
  - TP-Link AC600 T2U Plus
- **Service Interval**: Replace if damaged or every 3 years
- **Replacement Time**: 1 minute
- **Tools Required**: None
- **Location**: Rear USB port

**Replacement Procedure**:
1. Power down device
2. Remove old adapter
3. Insert new adapter
4. Power on device
5. Configure via web interface if needed

**Driver Support**:
- Most devices use standard Linux drivers
- Monitor mode capability required
- Check compatibility list before purchasing

### 3. GPS Components

#### GPS Antenna (External)
- **Connector Type**: SMA female
- **Cable Length**: 3m standard, 5m available
- **Service Interval**: Replace if damaged
- **Replacement Time**: 2 minutes
- **Tools Required**: None
- **Location**: Rear panel SMA connector

**Replacement Procedure**:
1. Power down device
2. Unscrew old antenna (hand-tight only)
3. Screw on new antenna (hand-tight only)
4. Route cable to appropriate location
5. Power on device
6. Verify GPS lock via web interface

**Specifications**:
- Frequency: 1575.42 MHz (L1)
- Gain: 28dB typical
- Impedance: 50Ω
- Connector: SMA male (antenna side)

#### GPS Module (Internal - Advanced)
- **Part Number**: u-blox NEO-8M or compatible
- **Service Interval**: Replace if failed (rare)
- **Replacement Time**: 15 minutes
- **Tools Required**: Screwdriver set
- **Location**: Internal PCB connection

**Note**: Internal GPS module replacement requires opening the case and is considered an advanced field service operation.

### 4. Power Components

#### Power Adapter
- **Specifications**: 5V/3A USB-C or barrel connector
- **Service Interval**: Replace if damaged
- **Replacement Time**: 30 seconds
- **Tools Required**: None
- **Location**: External adapter

**Replacement Procedure**:
1. Disconnect old adapter
2. Connect new adapter
3. Verify green power LED

**Compatible Adapters**:
- Official Raspberry Pi 5V/3A USB-C adapter
- Any 5V/3A adapter with appropriate connector
- Minimum 2.5A for reduced functionality

#### Power Cable
- **Type**: USB-C or barrel connector
- **Length**: 1.5m standard
- **Service Interval**: Replace if damaged
- **Replacement Time**: 30 seconds
- **Tools Required**: None

### 5. Cooling Components

#### Cooling Fan (if equipped)
- **Size**: 40mm x 40mm x 10mm
- **Voltage**: 5V DC
- **Service Interval**: Replace every 2 years or if noisy
- **Replacement Time**: 10 minutes
- **Tools Required**: Screwdriver
- **Location**: Top case cover

**Replacement Procedure**:
1. Power down device
2. Remove top case screws (4x)
3. Disconnect fan connector
4. Remove fan mounting screws (4x)
5. Install new fan
6. Connect fan connector
7. Replace top case cover

#### Heat Sink
- **Material**: Aluminum with thermal pad
- **Service Interval**: Clean annually, replace if damaged
- **Replacement Time**: 15 minutes
- **Tools Required**: Screwdriver, thermal paste
- **Location**: CPU area inside case

### 6. Input/Output Components

#### Status LEDs
- **Type**: 5mm through-hole LEDs
- **Colors**: Red, Green, Blue, Yellow
- **Service Interval**: Replace if burned out
- **Replacement Time**: 20 minutes (requires soldering)
- **Tools Required**: Soldering iron, screwdriver
- **Location**: Front panel

**Note**: LED replacement requires basic soldering skills and is considered an advanced field service operation.

#### Reset Button
- **Type**: Momentary push button
- **Service Interval**: Replace if stuck or non-responsive
- **Replacement Time**: 15 minutes
- **Tools Required**: Screwdriver
- **Location**: Side or rear panel

### 7. Protective Components

#### Enclosure Seals
- **Material**: Rubber gaskets
- **IP Rating**: IP65 (when properly sealed)
- **Service Interval**: Replace annually or if damaged
- **Replacement Time**: 30 minutes
- **Tools Required**: Screwdriver
- **Location**: Case seams

**Replacement Procedure**:
1. Power down device
2. Remove case screws
3. Clean old gasket material
4. Install new gaskets
5. Reassemble with proper torque
6. Test water resistance if applicable

#### Antenna Grommets
- **Material**: Rubber
- **Service Interval**: Replace if cracked or loose
- **Replacement Time**: 5 minutes
- **Tools Required**: None
- **Location**: Antenna entry points

## Non-Field-Serviceable Components

### Main Board
- **Service**: Factory only
- **Failure Indicators**: No power, no boot, component damage
- **Action**: Return to manufacturer

### Display (if equipped)
- **Service**: Factory only
- **Failure Indicators**: No display, touch not working, cracks
- **Action**: Return to manufacturer

### Internal Connectors
- **Service**: Factory only unless trained
- **Failure Indicators**: Intermittent connections, physical damage
- **Action**: Return to manufacturer or trained technician

### Power Management
- **Service**: Factory only
- **Failure Indicators**: Incorrect voltages, no charging
- **Action**: Return to manufacturer

## Field Service Tools

### Basic Tool Kit
- Phillips head screwdriver (PH0, PH1)
- Flat head screwdriver (2mm, 4mm)
- Plastic prying tools
- Anti-static wrist strap
- Flashlight or headlamp
- Compressed air canister

### Advanced Tool Kit (for trained technicians)
- Soldering iron (temperature controlled)
- Solder and flux
- Desoldering braid
- Digital multimeter
- Oscilloscope (portable)
- Function generator
- Power supply (variable)

### Spare Parts Kit

#### Basic Spare Parts (per 10 devices)
- SD cards (32GB): 2x
- USB Wi-Fi adapters: 2x
- GPS antennas: 1x
- Power adapters: 2x
- Power cables: 2x
- Enclosure seals: 1 set

#### Advanced Spare Parts (per 50 devices)
- Cooling fans: 5x
- Heat sinks: 2x
- Status LEDs (assorted): 20x
- Reset buttons: 5x
- Antenna grommets: 10x
- Thermal paste: 1 tube

## Service Procedures

### Pre-Service Checklist
1. **Safety**: Ensure device is powered off and disconnected
2. **Data**: Backup configuration and data if possible
3. **Documentation**: Record serial number and issue description
4. **Tools**: Gather appropriate tools and spare parts
5. **Environment**: Work in clean, well-lit area

### Post-Service Checklist
1. **Assembly**: Verify all components are properly installed
2. **Power**: Check power LED status
3. **Network**: Verify network connectivity
4. **GPS**: Confirm GPS lock if applicable
5. **Testing**: Run basic functionality tests
6. **Documentation**: Update service records

### Service Records
Maintain records for each device including:
- Serial number
- Service date
- Components replaced
- Issues addressed
- Technician name
- Test results

### Warranty Considerations
- Field service may void warranty if performed incorrectly
- Use only approved replacement parts
- Follow manufacturer procedures
- Document all service activities

## Troubleshooting Guidelines

### Before Replacing Components
1. **Software Reset**: Try soft reset via web interface
2. **Power Cycle**: Complete power off/on cycle
3. **Safe Mode**: Boot in diagnostic mode
4. **Logs**: Check system logs for error messages
5. **Connections**: Verify all connections are secure

### Component Testing
- **Storage**: Use disk utility to test read/write
- **Network**: Test with known good adapter
- **GPS**: Verify with GPS test utility
- **Power**: Measure voltages with multimeter
- **Cooling**: Check fan operation and temperatures

### When to Escalate
- Multiple component failures
- Intermittent issues that cannot be reproduced
- Power supply problems
- Physical damage to main board
- Software corruption that persists after factory reset

## Training Requirements

### Basic Field Service
- **Training**: 4-hour online course
- **Certification**: Basic Field Service Certificate
- **Valid For**: Storage, network, GPS antenna replacement

### Advanced Field Service
- **Training**: 2-day hands-on course
- **Certification**: Advanced Field Service Certificate
- **Valid For**: All field-serviceable components
- **Prerequisites**: Basic electronics knowledge, soldering experience

### Factory Service
- **Training**: 1-week factory training
- **Certification**: Factory Service Certificate
- **Valid For**: All components including main board
- **Prerequisites**: Advanced Field Service Certificate

---

*This document should be updated as new components are added or service procedures change. Always consult the latest version before performing field service.*
