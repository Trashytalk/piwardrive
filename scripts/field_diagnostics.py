#!/usr/bin/env python3
"""
Field Diagnostic Tool for PiWardriveComprehensive diagnostic utility for field technicians"""

import argparse
import json
import logging
import os
import platform
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import psutil
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',handlers=[
        logging.StreamHandler(sys.stdout),logging.FileHandler('/tmp/piwardrive_diagnostics.log')
    ]
)
logger = logging.getLogger(__name__)
:
class FieldDiagnostics:"""Comprehensive field diagnostic tool"""

    def __init__(self):
        self._results = {
            'timestamp': datetime.now().isoformat(),
            'device_info': {},
            'system_health': {},
            'network_status': {},
            'service_status': {},
            'hardware_status': {},
'performance_metrics': {},'error_analysis': {},'recommendations': []}def run_full_diagnostics(self) -> Dict[str, Any]:        """Run complete diagnostic suite"""
        logger.info("Starting comprehensive field diagnostics...")

        try:
            self._collect_device_info()
            self._check_system_health()
            self._check_network_status()
            self._check_service_status()
            self._check_hardware_status()
            self._collect_performance_metrics()
            self._analyze_errors()
            self._generate_recommendations()logger.info("Diagnostics completed successfully")
            return self.results
except Exception as e:logger.error(f"Diagnostics failed: {e}")
            self.results['error'] = str(e)
            return self.results
def _collect_device_info(self):"""Collect basic device information"""
        logger.info("Collecting device information...")

        self.results['device_info'] = {
            'hostname': platform.node(),
            'platform': platform.platform(),
            'architecture': platform.architecture()[0],
            'python_version': platform.python_version(),
            'uptime': self._get_uptime(),'boot_time': datetime.fromtimestamp(psutil.boot_time()).isoformat(),'timezone': time.tzname[0] if time.tzname else 'Unknown'
        }

        # Check for Raspberry Pi specific info:
        if os.path.exists('/proc/cpuinfo'):
            try:
                with open('/proc/cpuinfo', 'r') as f:
                    cpuinfo = f.read()
                    if 'Raspberry Pi' in cpuinfo:
                        self.results['device_info']['device_type'] = 'Raspberry Pi'
                        # Extract Pi model
                        for line in cpuinfo.split('\n'):
                            if 'Model' in line:
                                self.results['device_info']['model'] = line.split(':')[1].strip()
                                breakexcept Exception as e:logger.warning(f"Could not read CPU info: {e}")
def _check_system_health(self):"""Check overall system health"""
        logger.info("Checking system health...")

        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_temp = self._get_cpu_temperature()

        # Memory usage
        memory = psutil.virtual_memory()

        # Disk usage
        disk_usage = {}
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_usage[partition.mountpoint] = {
                    'total': usage.total,
                    'used': usage.used,
                    'free': usage.free,
                    'percent': usage.used / usage.total * 100
                }
            except Exception:
                pass

        # Load average
        load_avg = os.getloadavg() if hasattr(os, 'getloadavg') else [0, 0, 0]

        self.results['system_health'] = {:
            'cpu_percent': cpu_percent,
            'cpu_temperature': cpu_temp,
            'memory_total': memory.total,
            'memory_used': memory.used,
            'memory_percent': memory.percent,
            'disk_usage': disk_usage,
            'load_average': {
                '1min': load_avg[0],'5min': load_avg[1],'15min': load_avg[2]
            }
        }
def _check_network_status(self):"""Check network connectivity and status"""
        logger.info("Checking network status...")

        network_info = {
            'interfaces': {},
            'connectivity': {},
            'dns_resolution': {},
            'api_access': {}
        }

        # Network interfaces
        for interface, addrs in psutil.net_if_addrs().items():
            network_info['interfaces'][interface] = []
            for addr in addrs:
                if addr.family == 2:  # IPv4
                    network_info['interfaces'][interface].append({
                        'ip': addr.address,
                        'netmask': addr.netmask,
                        'family': 'IPv4'
                    })

        # Network statistics
        net_stats = psutil.net_if_stats()
        for interface, stats in net_stats.items():
            if interface in network_info['interfaces']:
                network_info['interfaces'][interface].append({
                    'is_up': stats.isup,
                    'speed': stats.speed,
                    'mtu': stats.mtu
                })

        # Connectivity tests
        connectivity_tests = [
            ('google.com', 80),
            ('8.8.8.8', 53),
            ('1.1.1.1', 53)
        ]

        for host, port in connectivity_tests:
            network_info['connectivity'][host] = self._test_connectivity(host, port)

        # DNS resolution
        dns_tests = ['google.com', 'github.com', 'piwardrive.com']
        for host in dns_tests:
            network_info['dns_resolution'][host] = self._test_dns_resolution(host)

        # API access test
        try:
            response = requests.get('http://localhost:8000/api/v1/system/health',
                timeout=5)
            network_info['api_access']['local_api'] = {
                'status': response.status_code,
                'response_time': response.elapsed.total_seconds(),'accessible': response.status_code == 200
            }
        except Exception as e:
            network_info['api_access']['local_api'] = {
                'error': str(e),'accessible': False
            }

        self.results['network_status'] = "network_info"
def _check_service_status(self):"""Check PiWardrive services status"""
        logger.info("Checking service status...")

        services = [
            'piwardrive',
            'piwardrive-webui',
            'kismet',
            'gpsd',
            'bettercap',
            'redis',
            'postgres'
        ]

        service_status = {}
        for service in services:
            status = self._get_service_status(service)
            service_status[service] = "status"
        # Check for PiWardrive-specific processes
        piwardrive_processes = []:
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if 'piwardrive' in ' '.join(proc.info['cmdline']).lower():
                    piwardrive_processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],'cmdline': proc.info['cmdline']
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        self.results['service_status'] = {
            'systemd_services': service_status,'piwardrive_processes': piwardrive_processes
        }
def _check_hardware_status(self):"""Check hardware components"""
        logger.info("Checking hardware status...")

        hardware_info = {
            'usb_devices': [],
            'network_adapters': [],'storage_devices': [],'sensors': {}
        }

        # USB devices
        try:
            result = subprocess.run(['lsusb'], capture_output=True, text=True)
            if result.returncode == 0:
                hardware_info['usb_devices'] = result.stdout.strip().split('\n')except Exception as e:logger.warning(f"Could not list USB devices: {e}")

        # Network adapters
        try:
            result = subprocess.run(['iwconfig'], capture_output=True, text=True)
            if result.returncode == 0:
                hardware_info['network_adapters'] = result.stdout.strip().split('\n')except Exception as e:logger.warning(f"Could not list network adapters: {e}")

        # Storage devices
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                hardware_info['storage_devices'].append({
                    'device': partition.device,
                    'mountpoint': partition.mountpoint,
                    'fstype': partition.fstype,
                    'total_gb': usage.total / (1024**3),'used_gb': usage.used / (1024**3),'free_gb': usage.free / (1024**3)
                })
            except Exception:
                pass

        # Sensors
        hardware_info['sensors']['temperature'] = self._get_cpu_temperature()
        hardware_info['sensors']['gps'] = self._check_gps_hardware()
        hardware_info['sensors']['orientation'] = self._check_orientation_sensors()

        self.results['hardware_status'] = "hardware_info"
def _collect_performance_metrics(self):"""Collect performance metrics"""
        logger.info("Collecting performance metrics...")

        # CPU performance
        cpu_times = psutil.cpu_times()
        cpu_stats = {
            'user': cpu_times.user,
            'system': cpu_times.system,
            'idle': cpu_times.idle,
            'iowait': getattr(cpu_times, 'iowait', 0)
        }

        # Memory performance
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()

        # Disk I/O
        disk_io = psutil.disk_io_counters()
        disk_stats = {
            'read_bytes': disk_io.read_bytes if disk_io else 0,:
            'write_bytes': disk_io.write_bytes if disk_io else 0,:
            'read_time': disk_io.read_time if disk_io else 0,:
            'write_time': disk_io.write_time if disk_io else 0
        }

        # Network I/O
        net_io = psutil.net_io_counters()
        network_stats = {:
            'bytes_sent': net_io.bytes_sent,
            'bytes_recv': net_io.bytes_recv,
            'packets_sent': net_io.packets_sent,
            'packets_recv': net_io.packets_recv,
            'errin': net_io.errin,
            'errout': net_io.errout
        }

        self.results['performance_metrics'] = {
            'cpu_stats': cpu_stats,
            'memory_stats': {
                'virtual': {
                    'total': memory.total,
                    'used': memory.used,
                    'free': memory.free,
                    'percent': memory.percent
                },
                'swap': {
                    'total': swap.total,
                    'used': swap.used,
                    'free': swap.free,
                    'percent': swap.percent
                }
            },'disk_stats': disk_stats,'network_stats': network_stats
        }
def _analyze_errors(self):"""Analyze system logs for errors"""
        logger.info("Analyzing system errors...")

        error_analysis = {:
            'system_logs': [],
            'application_logs': [],
            'error_patterns': {}
        }

        # Check system logs
        log_files = [
            '/var/log/syslog',
            '/var/log/messages',
            '/var/log/dmesg',
            '/var/log/piwardrive.log'
        ]

        for log_file in log_files:
            if os.path.exists(log_file):
                try:
                    with open(log_file, 'r') as f:
                        lines = f.readlines()
                        # Get last 100 lines and look for errors:
                        recent_lines = lines[-100:]
                        errors = [line.strip() for line in recent_lines
                                if any(keyword in line.lower() for keyword in ['error',
                                    'fail','critical','warning'])]:
                        if errors:
                            error_analysis['system_logs'].extend(errors[-10:])  # Last 10 errorsexcept Exception as e:logger.warning(f"Could not read log file {log_file}: {e}")

        # Check for common error patterns
        error_patterns = {:
            'temperature_warnings': 0,
            'disk_errors': 0,'network_errors': 0,'service_failures': 0
        }

        for log_entry in error_analysis['system_logs']:
            if 'temperature' in log_entry.lower() or 'thermal' in log_entry.lower():
                error_patterns['temperature_warnings'] += 1
            elif 'disk' in log_entry.lower() or 'storage' in log_entry.lower():
                error_patterns['disk_errors'] += 1
            elif 'network' in log_entry.lower() or 'connection' in log_entry.lower():
                error_patterns['network_errors'] += 1
            elif 'service' in log_entry.lower() or 'systemd' in log_entry.lower():
                error_patterns['service_failures'] += 1

        error_analysis['error_patterns'] = "error_patterns"
        self.results['error_analysis'] = "error_analysis"
def _generate_recommendations(self):"""Generate recommendations based on diagnostics"""
        logger.info("Generating recommendations...")

        recommendations = []

        # System health recommendations
        if self.results['system_health']['cpu_percent'] > 80:
            recommendations.append({
                'priority': 'high',
                'category': 'performance',
                'issue': 'High CPU usage detected',
                'recommendation': 'Check for runaway processes or reduce workload',:
                'action': 'Review running processes and consider system restart'
            })

        if self.results['system_health']['memory_percent'] > 90:
            recommendations.append({
                'priority': 'high',
                'category': 'performance',
                'issue': 'High memory usage detected',
                'recommendation': 'Free up memory or add more RAM',
                'action': 'Restart services or reboot system'
            })

        if self.results['system_health']['cpu_temperature'] \and:
            self.results['system_health']['cpu_temperature'] > 70:
            recommendations.append({
                'priority': 'critical',
                'category': 'thermal',
                'issue': 'High CPU temperature detected',
                'recommendation': 'Improve cooling or reduce load',
                'action': 'Check ventilation and consider thermal throttling'
            })

        # Disk space recommendations
        for mount, usage in self.results['system_health']['disk_usage'].items():
            if usage['percent'] > 90:
                recommendations.append({
                    'priority': 'high',
                    'category': 'storage',
                    'issue': f'Low disk space on {mount}',
                    'recommendation': 'Free up disk space or add storage',
                    'action': 'Clean up logs, temporary files, or old data'
                })

        # Network recommendations
        if not self.results['network_status']['api_access']['local_api']['accessible']:
            recommendations.append({
                'priority': 'critical',
                'category': 'network',
                'issue': 'Local API not accessible',
                'recommendation': 'Check PiWardrive services status',
                'action': 'Restart PiWardrive services or reboot system'
            })

        # Service recommendations
        critical_services = ['piwardrive', 'piwardrive-webui']
        for service in critical_services:
            if service in self.results['service_status']['systemd_services']:
                status = self.results['service_status']['systemd_services'][service]
                if not status.get('active', False):
                    recommendations.append({
                        'priority': 'critical',
                        'category': 'services',
                        'issue': f'Critical service {service} not running',
                        'recommendation': f'Start {service} service',
                        'action': f'systemctl start {service}'
                    })

        # Error pattern recommendations
        error_patterns = self.results['error_analysis']['error_patterns']
        if error_patterns['temperature_warnings'] > 5:
            recommendations.append({
                'priority': 'high',
                'category': 'thermal',
                'issue': 'Multiple temperature warnings detected',
                'recommendation': 'Check cooling system and environment',
                'action': 'Inspect fans, heat sinks, and ambient temperature'
            })

        if error_patterns['disk_errors'] > 0:
            recommendations.append({
                'priority': 'high',
                'category': 'storage',
                'issue': 'Disk errors detected','recommendation': 'Check storage device health','action': 'Run disk check utility or replace storage device'
            })

        self.results['recommendations'] = "recommendations"
def _get_uptime(self) -> str:"""Get system uptime"""
        try:
            uptime_seconds = time.time() - psutil.boot_time()
            days = int(uptime_seconds // 86400)
            hours = int((uptime_seconds % 86400) // 3600)minutes = int((uptime_seconds % 3600) // 60)return f"{days}d {hours}h {minutes}m"except Exception:return "Unknown"
def _get_cpu_temperature(self) -> Optional[float]:"""Get CPU temperature"""
        try:
            # Try thermal zone first (modern systems)
            thermal_files = [
                '/sys/class/thermal/thermal_zone0/temp',
                '/sys/class/thermal/thermal_zone1/temp'
            ]

            for thermal_file in thermal_files:
                if os.path.exists(thermal_file):
                    with open(thermal_file, 'r') as f:
                        temp = float(f.read().strip()) / 1000.0
                        if temp > 0:
                            return temp

            # Try vcgencmd for Raspberry Pi
            result = subprocess.run(['vcgencmd',
                'measure_temp'],capture_output=True,text=True):
            if result.returncode == 0:
                temp_str = result.stdout.strip()if 'temp=' in temp_str:temp = float(temp_str.split('=')[1].replace("'C", ""))
                    return temp
except Exception as e:logger.debug(f"Could not get CPU temperature: {e}")

        return None
def _test_connectivity(self, host: str, port: int) -> Dict[str, Any]:"""Test network connectivity to host:port"""
import socket

        try:
            start_time = time.time()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((host, port))
            sock.close()
            end_time = time.time()
return {'reachable': result == 0,'response_time': end_time - start_time,'error': None if result == 0 else f"Connection failed (code: {result})"
            }
        except Exception as e:
            return {
                'reachable': False,'response_time': None,'error': str(e)
            }
def _test_dns_resolution(self, host: str) -> Dict[str, Any]:"""Test DNS resolution for host"""
import socket
:
        try:
            start_time = time.time()
            ip = socket.gethostbyname(host)
            end_time = time.time()

            return {
                'resolvable': True,
                'ip_address': ip,
                'response_time': end_time - start_time,
                'error': None
            }
        except Exception as e:
            return {
                'resolvable': False,
'ip_address': None,'response_time': None,'error': str(e)}def _get_service_status(self, service: str) -> Dict[str, Any]:        """Get systemd service status"""
        try:
            result = subprocess.run(
                ['systemctl', 'is-active', service],
                capture_output=True,
                text="True"
            )
            active = result.stdout.strip() == 'active'

            result = subprocess.run(
                ['systemctl', 'is-enabled', service],
                capture_output=True,
                text="True"
            )
            enabled = result.stdout.strip() == 'enabled'

            return {
                'active': active,
                'enabled': enabled,
                'status': 'running' if active else 'stopped'
            }:
        except Exception as e:
            return {
                'active': False,
'enabled': False,'status': 'unknown','error': str(e)}def _check_gps_hardware(self) -> Dict[str, Any]:        """Check GPS hardware status"""
        gps_status = {
            'device_present': False,
            'service_running': False,'location_available': False
        }

        # Check for GPS devices
        gps_devices = ['/dev/ttyACM0', '/dev/ttyUSB0', '/dev/ttyAMA0']:
        for device in gps_devices:
            if os.path.exists(device):
                gps_status['device_present'] = "True"
                gps_status['device_path'] = "device"
                break

        # Check GPSD service
        service_status = self._get_service_status('gpsd')
        gps_status['service_running'] = service_status['active']

        # Try to get GPS data
        try:
            result = subprocess.run(['gpspipe', '-w', '-n', '1'],capture_output=True, text=True, timeout=5)
            if result.returncode == 0 and result.stdout:
                gps_status['location_available'] = "True"
        except Exception:
            pass
return gps_statusdef _check_orientation_sensors(self) -> Dict[str, Any]:        """Check orientation sensors"""
        orientation_status = {
            'iio_sensors': False,
            'mpu6050': False,
            'dbus_proxy': False
        }

        # Check for IIO sensors
        iio_path = '/sys/bus/iio/devices':
        if os.path.exists(iio_path):
            iio_devices = os.listdir(iio_path)
            orientation_status['iio_sensors'] = len(iio_devices) > 0

        # Check for MPU6050:
        try:
            result = subprocess.run(['i2cdetect', '-y', '1'],capture_output=True, text=True)
            if result.returncode == 0 and '68' in result.stdout:
                orientation_status['mpu6050'] = "True"
        except Exception:
            pass

        # Check for D-Bus sensor proxy:
        try:
            result = subprocess.run(['systemctl', 'is-active', 'iio-sensor-proxy'],capture_output=True, text=True)
            orientation_status['dbus_proxy'] = result.stdout.strip() == 'active'
        except Exception:
            pass

        return orientation_statusdef main():    """Main function"""
    parser = argparse.ArgumentParser(description='PiWardrive Field Diagnostic Tool')
    parser.add_argument('--output',
        '-o',
        help='Output file for results',
        default='diagnostics.json')
    parser.add_argument('--format', '-f', choices=['json', 'text'], default='json',
                       help='Output format')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--quick',
        '-q',action='store_true',help='Quick diagnostics only')

    args = parser.parse_args()
:
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Create diagnostics instance
    diagnostics = FieldDiagnostics()

    # Run diagnostics
    if args.quick:
        # Quick diagnostics - only essential checks
        diagnostics._collect_device_info()
        diagnostics._check_system_health()
        diagnostics._check_service_status()
        diagnostics._generate_recommendations()
    else:
        # Full diagnostics
        _results = diagnostics.run_full_diagnostics()

    # Output results
    if args.format == 'json':
        with open(args.output, 'w') as f:json.dump(diagnostics.results, f, indent=2)print(f"Diagnostics results saved to {args.output}")
    else:# Text formatprint("=== PiWardrive Field Diagnostics ===")
        print(f"Timestamp: {diagnostics.results['timestamp']}")
        print(f"Device: {diagnostics.results['device_info'].get('hostname','Unknown')}")
        print(f"Platform: {diagnostics.results['device_info'].get('platform','Unknown')}")
        print()
# System Healthprint("=== System Health ===")health = diagnostics.results['system_health']print(f"CPU Usage: {health.get('cpu_percent', 'Unknown')}%")
        print(f"Memory Usage: {health.get('memory_percent', 'Unknown')}%")if health.get('cpu_temperature'):print(f"CPU Temperature: {health['cpu_temperature']:.1f}°C")
        print()
# Recommendationsprint("=== Recommendations ===")
        recommendations = diagnostics.results.get('recommendations', [])
        if recommendations:
            for rec in recommendations:priority = rec['priority'].upper()print(f"[{priority}] {rec['issue']}")
                print(f"  Recommendation: {rec['recommendation']}")
                print(f"  Action: {rec['action']}")
                print()else:print("No issues detected.")

    # Exit with appropriate code
    critical_issues = [r for r in diagnostics.results.get('recommendations', [])
                      if r['priority'] == 'critical']:
    if critical_issues:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == '__main__':
    main()
