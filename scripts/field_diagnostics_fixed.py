#!/usr/bin/env python3
"""
Field Diagnostic Tool for PiWardrive
Comprehensive diagnostic utility for field technicians
"""

import argparse
import json
import logging
import os
import platform
import subprocess
import sys
import time
from datetime import datetime
from typing import Any, Dict

import psutil

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('/tmp/piwardrive_diagnostics.log')
    ]
)
logger = logging.getLogger(__name__)


class FieldDiagnostics:
    """Comprehensive field diagnostic tool"""

    def __init__(self):
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'device_info': {},
            'system_health': {},
            'network_status': {},
            'service_status': {},
            'hardware_status': {},
            'performance_metrics': {},
            'error_analysis': {},
            'recommendations': []
        }

    def run_full_diagnostics(self) -> Dict[str, Any]:
        """Run complete diagnostic suite"""
        logger.info("Starting comprehensive diagnostics")
        
        try:
            self._collect_device_info()
            self._check_system_health()
            self._check_network_status()
            self._check_service_status()
            self._check_hardware_status()
            self._collect_performance_metrics()
            self._analyze_errors()
            self._generate_recommendations()
            
            logger.info("Diagnostics completed successfully")
            
        except Exception as e:
            logger.error(f"Diagnostics failed: {e}")
            self.results['error'] = str(e)
            
        return self.results

    def _collect_device_info(self):
        """Collect basic device information"""
        logger.info("Collecting device information...")
        
        device_info = {
            'hostname': platform.node(),
            'platform': platform.platform(),
            'architecture': platform.architecture()[0],
            'python_version': platform.python_version(),
            'timestamp': datetime.now().isoformat()
        }
        
        # Get CPU information
        try:
            with open('/proc/cpuinfo', 'r') as f:
                for line in f:
                    if line.startswith('model name'):
                        device_info['cpu_model'] = line.split(':')[1].strip()
                        break
        except Exception as e:
            logger.warning(f"Could not read CPU info: {e}")
            
        self.results['device_info'] = device_info

    def _check_system_health(self):
        """Check overall system health"""
        logger.info("Checking system health...")
        
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # Memory usage
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        
        # Disk usage
        disk = psutil.disk_usage('/')
        disk_percent = (disk.used / disk.total) * 100
        
        # CPU temperature (if available)
        cpu_temp = None
        try:
            temps = psutil.sensors_temperatures()
            if 'cpu_thermal' in temps:
                cpu_temp = temps['cpu_thermal'][0].current
        except:
            pass
            
        # Load average
        load_avg = os.getloadavg()
        
        self.results['system_health'] = {
            'cpu_percent': cpu_percent,
            'memory_percent': memory_percent,
            'disk_percent': disk_percent,
            'cpu_temperature': cpu_temp,
            'load_average': load_avg,
            'uptime': datetime.now().timestamp() - psutil.boot_time()
        }

    def _check_network_status(self):
        """Check network connectivity and status"""
        logger.info("Checking network status...")
        
        network_status = {
            'interfaces': {},
            'connectivity': {},
            'dns_resolution': False
        }
        
        # Check network interfaces
        for interface, addresses in psutil.net_if_addrs().items():
            interface_info = {
                'addresses': [],
                'stats': {}
            }
            
            for addr in addresses:
                if addr.family == 2:  # IPv4
                    interface_info['addresses'].append({
                        'family': 'IPv4',
                        'address': addr.address,
                        'netmask': addr.netmask
                    })
                elif addr.family == 10:  # IPv6
                    interface_info['addresses'].append({
                        'family': 'IPv6',
                        'address': addr.address,
                        'netmask': addr.netmask
                    })
            
            # Interface statistics
            try:
                stats = psutil.net_if_stats()[interface]
                interface_info['stats'] = {
                    'is_up': stats.isup,
                    'speed': stats.speed,
                    'mtu': stats.mtu
                }
            except KeyError:
                pass
            
            network_status['interfaces'][interface] = interface_info
        
        # Check connectivity
        connectivity_tests = [
            ('google.com', 'Google DNS'),
            ('8.8.8.8', 'Public DNS'),
            ('1.1.1.1', 'Cloudflare DNS')
        ]
        
        for host, description in connectivity_tests:
            try:
                result = subprocess.run(
                    ['ping', '-c', '1', '-W', '3', host],
                    capture_output=True,
                    timeout=5
                )
                network_status['connectivity'][host] = {
                    'reachable': result.returncode == 0,
                    'description': description
                }
            except subprocess.TimeoutExpired:
                network_status['connectivity'][host] = {
                    'reachable': False,
                    'description': description
                }
        
        # DNS resolution test
        try:
            import socket
            socket.gethostbyname('google.com')
            network_status['dns_resolution'] = True
        except:
            network_status['dns_resolution'] = False
        
        self.results['network_status'] = network_status

    def _check_service_status(self):
        """Check PiWardrive services status"""
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
            service_status[service] = status
            
        # Check for PiWardrive-specific processes
        piwardrive_processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if 'piwardrive' in ' '.join(proc.info['cmdline']).lower():
                    piwardrive_processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'cmdline': proc.info['cmdline']
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        self.results['service_status'] = {
            'services': service_status,
            'piwardrive_processes': piwardrive_processes
        }

    def _get_service_status(self, service_name: str) -> Dict[str, Any]:
        """Get systemd service status"""
        try:
            result = subprocess.run(
                ['systemctl', 'is-active', service_name],
                capture_output=True,
                text=True
            )
            active = result.stdout.strip() == 'active'
            
            # Get detailed status
            result = subprocess.run(
                ['systemctl', 'status', service_name],
                capture_output=True,
                text=True
            )
            
            return {
                'active': active,
                'status_output': result.stdout,
                'enabled': self._is_service_enabled(service_name)
            }
        except Exception as e:
            logger.warning(f"Could not check service {service_name}: {e}")
            return {
                'active': False,
                'error': str(e),
                'enabled': False
            }

    def _is_service_enabled(self, service_name: str) -> bool:
        """Check if service is enabled"""
        try:
            result = subprocess.run(
                ['systemctl', 'is-enabled', service_name],
                capture_output=True,
                text=True
            )
            return result.stdout.strip() == 'enabled'
        except:
            return False

    def _check_hardware_status(self):
        """Check hardware components"""
        logger.info("Checking hardware status...")
        
        hardware_info = {}
        
        # USB devices
        try:
            result = subprocess.run(['lsusb'], capture_output=True, text=True)
            if result.returncode == 0:
                hardware_info['usb_devices'] = result.stdout.strip().split('\n')
        except Exception as e:
            logger.warning(f"Could not list USB devices: {e}")
            
        # Network adapters
        try:
            result = subprocess.run(['lspci'], capture_output=True, text=True)
            if result.returncode == 0:
                hardware_info['network_adapters'] = result.stdout.strip().split('\n')
        except Exception as e:
            logger.warning(f"Could not list network adapters: {e}")
            
        # GPIO status (if available)
        gpio_status = self._check_gpio_status()
        if gpio_status:
            hardware_info['gpio'] = gpio_status
            
        # Camera status
        camera_status = self._check_camera_status()
        if camera_status:
            hardware_info['camera'] = camera_status
            
        # GPS status
        gps_status = self._check_gps_status()
        if gps_status:
            hardware_info['gps'] = gps_status
            
        # Orientation sensors
        orientation_status = self._check_orientation_sensors()
        if orientation_status:
            hardware_info['orientation'] = orientation_status
            
        self.results['hardware_status'] = hardware_info

    def _check_gpio_status(self) -> Dict[str, Any]:
        """Check GPIO status"""
        try:
            result = subprocess.run(['gpio', 'readall'], capture_output=True, text=True)
            if result.returncode == 0:
                return {
                    'available': True,
                    'readall_output': result.stdout
                }
        except FileNotFoundError:
            pass
        return {'available': False}

    def _check_camera_status(self) -> Dict[str, Any]:
        """Check camera status"""
        camera_status = {
            'vcgencmd': False,
            'device_exists': False
        }
        
        # Check with vcgencmd
        try:
            result = subprocess.run(['vcgencmd', 'get_camera'], capture_output=True, text=True)
            if result.returncode == 0:
                camera_status['vcgencmd'] = 'detected=1' in result.stdout
                camera_status['vcgencmd_output'] = result.stdout.strip()
        except FileNotFoundError:
            pass
            
        # Check for camera device
        camera_devices = ['/dev/video0', '/dev/video1']
        for device in camera_devices:
            if os.path.exists(device):
                camera_status['device_exists'] = True
                break
                
        return camera_status

    def _check_gps_status(self) -> Dict[str, Any]:
        """Check GPS status"""
        gps_status = {
            'gpsd_running': False,
            'device_exists': False
        }
        
        # Check if gpsd is running
        try:
            result = subprocess.run(['systemctl', 'is-active', 'gpsd'], capture_output=True, text=True)
            gps_status['gpsd_running'] = result.stdout.strip() == 'active'
        except Exception:
            pass
            
        # Check for GPS devices
        gps_devices = ['/dev/ttyACM0', '/dev/ttyUSB0', '/dev/ttyS0']
        for device in gps_devices:
            if os.path.exists(device):
                gps_status['device_exists'] = True
                break
                
        return gps_status

    def _check_orientation_sensors(self) -> Dict[str, Any]:
        """Check orientation sensors"""
        orientation_status = {
            'iio_sensors': False,
            'mpu6050': False,
            'dbus_proxy': False
        }

        # Check for IIO sensors
        iio_path = '/sys/bus/iio/devices'
        if os.path.exists(iio_path):
            iio_devices = os.listdir(iio_path)
            orientation_status['iio_sensors'] = len(iio_devices) > 0

        # Check for MPU6050
        try:
            result = subprocess.run(['i2cdetect', '-y', '1'], capture_output=True, text=True)
            if result.returncode == 0 and '68' in result.stdout:
                orientation_status['mpu6050'] = True
        except Exception:
            pass

        # Check for D-Bus sensor proxy
        try:
            result = subprocess.run(['systemctl', 'is-active', 'iio-sensor-proxy'], capture_output=True, text=True)
            orientation_status['dbus_proxy'] = result.stdout.strip() == 'active'
        except Exception:
            pass

        return orientation_status

    def _collect_performance_metrics(self):
        """Collect performance metrics"""
        logger.info("Collecting performance metrics...")
        
        # CPU metrics
        cpu_times = psutil.cpu_times()
        cpu_stats = {
            'user': cpu_times.user,
            'system': cpu_times.system,
            'idle': cpu_times.idle,
            'count': psutil.cpu_count()
        }
        
        # Memory metrics
        memory = psutil.virtual_memory()
        memory_stats = {
            'total': memory.total,
            'available': memory.available,
            'used': memory.used,
            'percent': memory.percent
        }
        
        # Disk I/O
        disk_io = psutil.disk_io_counters()
        disk_stats = {
            'read_bytes': disk_io.read_bytes if disk_io else 0,
            'write_bytes': disk_io.write_bytes if disk_io else 0,
            'read_count': disk_io.read_count if disk_io else 0,
            'write_count': disk_io.write_count if disk_io else 0
        }
        
        # Network I/O
        network_io = psutil.net_io_counters()
        network_stats = {
            'bytes_sent': network_io.bytes_sent if network_io else 0,
            'bytes_recv': network_io.bytes_recv if network_io else 0,
            'packets_sent': network_io.packets_sent if network_io else 0,
            'packets_recv': network_io.packets_recv if network_io else 0
        }
        
        self.results['performance_metrics'] = {
            'cpu': cpu_stats,
            'memory': memory_stats,
            'disk': disk_stats,
            'network': network_stats,
            'timestamp': datetime.now().isoformat()
        }

    def _analyze_errors(self):
        """Analyze system logs for errors"""
        logger.info("Analyzing system errors...")
        
        error_analysis = {
            'system_errors': [],
            'application_errors': [],
            'error_counts': {}
        }
        
        # Check system logs
        log_files = [
            '/var/log/syslog',
            '/var/log/kern.log',
            '/var/log/daemon.log'
        ]
        
        for log_file in log_files:
            if os.path.exists(log_file):
                try:
                    result = subprocess.run(
                        ['tail', '-n', '100', log_file],
                        capture_output=True,
                        text=True
                    )
                    if result.returncode == 0:
                        lines = result.stdout.strip().split('\n')
                        for line in lines:
                            if any(keyword in line.lower() for keyword in [
                                'error', 'fail', 'critical', 'warning'
                            ]):
                                error_analysis['system_errors'].append({
                                    'file': log_file,
                                    'line': line.strip()
                                })
                except Exception as e:
                    logger.warning(f"Could not analyze log file {log_file}: {e}")
        
        # Error pattern analysis
        error_patterns = {
            'out_of_memory': 0,
            'disk_full': 0,
            'network_timeout': 0,
            'permission_denied': 0,
            'service_failed': 0
        }
        
        for error in error_analysis['system_errors']:
            line = error['line'].lower()
            if 'out of memory' in line or 'oom' in line:
                error_patterns['out_of_memory'] += 1
            elif 'no space left' in line or 'disk full' in line:
                error_patterns['disk_full'] += 1
            elif 'timeout' in line or 'connection refused' in line:
                error_patterns['network_timeout'] += 1
            elif 'permission denied' in line or 'access denied' in line:
                error_patterns['permission_denied'] += 1
            elif 'failed' in line and 'service' in line:
                error_patterns['service_failed'] += 1
        
        error_analysis['error_counts'] = error_patterns
        self.results['error_analysis'] = error_analysis

    def _generate_recommendations(self):
        """Generate recommendations based on diagnostic results"""
        logger.info("Generating recommendations...")
        
        recommendations = []
        
        # System health recommendations
        health = self.results.get('system_health', {})
        
        # CPU usage
        if health.get('cpu_percent', 0) > 80:
            recommendations.append({
                'priority': 'high',
                'category': 'performance',
                'issue': 'High CPU usage detected',
                'recommendation': 'Investigate high CPU usage processes',
                'action': 'Run "htop" or "top" to identify resource-intensive processes'
            })
        
        # Memory usage
        if health.get('memory_percent', 0) > 85:
            recommendations.append({
                'priority': 'high',
                'category': 'performance',
                'issue': 'High memory usage detected',
                'recommendation': 'Free up memory or add more RAM',
                'action': 'Restart services or reboot system if necessary'
            })
        
        # Disk usage
        if health.get('disk_percent', 0) > 90:
            recommendations.append({
                'priority': 'critical',
                'category': 'storage',
                'issue': 'Disk space critically low',
                'recommendation': 'Free up disk space immediately',
                'action': 'Delete old logs, temporary files, or move data to external storage'
            })
        
        # Temperature
        if health.get('cpu_temperature', 0) > 75:
            recommendations.append({
                'priority': 'medium',
                'category': 'hardware',
                'issue': 'High CPU temperature detected',
                'recommendation': 'Check cooling system',
                'action': 'Clean fans and heat sinks, ensure proper ventilation'
            })
        
        # Service status recommendations
        services = self.results.get('service_status', {}).get('services', {})
        critical_services = ['piwardrive', 'piwardrive-webui']
        
        for service in critical_services:
            if not services.get(service, {}).get('active', False):
                recommendations.append({
                    'priority': 'critical',
                    'category': 'services',
                    'issue': f'Critical service {service} is not running',
                    'recommendation': f'Start {service} service',
                    'action': f'sudo systemctl start {service}'
                })
        
        # Network connectivity recommendations
        network = self.results.get('network_status', {})
        if not network.get('dns_resolution', False):
            recommendations.append({
                'priority': 'high',
                'category': 'network',
                'issue': 'DNS resolution not working',
                'recommendation': 'Check DNS configuration',
                'action': 'Verify /etc/resolv.conf and network settings'
            })
        
        # Error analysis recommendations
        error_counts = self.results.get('error_analysis', {}).get('error_counts', {})
        if error_counts.get('out_of_memory', 0) > 0:
            recommendations.append({
                'priority': 'high',
                'category': 'performance',
                'issue': 'Out of memory errors detected',
                'recommendation': 'Investigate memory leaks or increase available memory',
                'action': 'Review application memory usage and consider adding swap space'
            })
        
        self.results['recommendations'] = recommendations

    def run_daemon_mode(self):
        """Run continuous diagnostics in daemon mode"""
        logger.info("Starting field diagnostics daemon mode")
        
        # Set up signal handlers for graceful shutdown
        import signal
        
        def signal_handler(signum, frame):
            logger.info(f"Received signal {signum}, shutting down daemon")
            sys.exit(0)
        
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)
        
        # Main daemon loop
        while True:
            try:
                # Run periodic diagnostics
                self.run_full_diagnostics()
                
                # Check for critical issues
                critical_issues = self._check_critical_issues()
                if critical_issues:
                    logger.warning(f"Critical issues detected: {critical_issues}")
                    self._send_alert(critical_issues)
                
                # Save results with timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_file = f"/tmp/piwardrive_diagnostics_{timestamp}.json"
                
                with open(output_file, 'w') as f:
                    json.dump(self.results, f, indent=2)
                
                # Sleep for configured interval (default 5 minutes)
                time.sleep(300)
                
            except Exception as e:
                logger.error(f"Error in daemon mode: {e}")
                time.sleep(60)  # Wait 1 minute before retrying
    
    def _check_critical_issues(self):
        """Check for critical issues that require immediate attention"""
        issues = []
        
        # Check system health
        health = self.results.get('system_health', {})
        
        # Critical CPU usage
        if health.get('cpu_percent', 0) > 90:
            issues.append("High CPU usage detected")
        
        # Critical memory usage
        if health.get('memory_percent', 0) > 95:
            issues.append("Critical memory usage detected")
        
        # High temperature
        if health.get('cpu_temperature', 0) > 80:
            issues.append("High CPU temperature detected")
        
        # Low disk space
        if health.get('disk_percent', 0) > 90:
            issues.append("Low disk space detected")
        
        # Check service status
        services = self.results.get('service_status', {}).get('services', {})
        critical_services = ['piwardrive', 'piwardrive-webui']
        
        for service in critical_services:
            if not services.get(service, {}).get('active', False):
                issues.append(f"Critical service {service} is not active")
        
        return issues
    
    def _send_alert(self, issues):
        """Send alert for critical issues"""
        try:
            # Write to syslog
            import syslog
            syslog.openlog("piwardrive-field-diagnostics")
            
            for issue in issues:
                syslog.syslog(syslog.LOG_ERR, f"CRITICAL: {issue}")
            
            syslog.closelog()
            
            # Also write to dedicated alert file
            alert_file = "/tmp/piwardrive_alerts.log"
            with open(alert_file, 'a') as f:
                timestamp = datetime.now().isoformat()
                f.write(f"{timestamp}: CRITICAL ALERT - {', '.join(issues)}\n")
            
        except Exception as e:
            logger.error(f"Failed to send alert: {e}")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='PiWardrive Field Diagnostic Tool')
    parser.add_argument('--output', '-o', 
                       help='Output file for results',
                       default='diagnostics.json')
    parser.add_argument('--format', '-f', 
                       choices=['json', 'text'], 
                       default='json',
                       help='Output format')
    parser.add_argument('--verbose', '-v', 
                       action='store_true', 
                       help='Verbose output')
    parser.add_argument('--quick', '-q', 
                       action='store_true',
                       help='Quick diagnostics only')
    parser.add_argument('--daemon', '-d', 
                       action='store_true',
                       help='Run in daemon mode (continuous monitoring)')
    parser.add_argument('--test', '-t', 
                       action='store_true',
                       help='Run basic functionality test')

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Create diagnostics instance
    diagnostics = FieldDiagnostics()

    # Handle daemon mode
    if args.daemon:
        diagnostics.run_daemon_mode()
        return

    # Handle test mode
    if args.test:
        print("Running PiWardrive Field Diagnostics test...")
        try:
            diagnostics._collect_device_info()
            print("✓ Device info collection: PASS")
            
            diagnostics._check_system_health()
            print("✓ System health check: PASS")
            
            diagnostics._check_service_status()
            print("✓ Service status check: PASS")
            
            print("✓ All tests passed!")
            return
            
        except Exception as e:
            print(f"✗ Test failed: {e}")
            return

    # Run diagnostics
    if args.quick:
        # Quick diagnostics - only essential checks
        diagnostics._collect_device_info()
        diagnostics._check_system_health()
        diagnostics._check_service_status()
        diagnostics._generate_recommendations()
    else:
        # Full diagnostics
        diagnostics.run_full_diagnostics()

    # Output results
    if args.format == 'json':
        with open(args.output, 'w') as f:
            json.dump(diagnostics.results, f, indent=2)
        print(f"Diagnostics results saved to {args.output}")
    else:
        # Text format
        print("=== PiWardrive Field Diagnostics ===")
        print(f"Timestamp: {diagnostics.results['timestamp']}")
        print(f"Device: {diagnostics.results['device_info'].get('hostname', 'Unknown')}")
        print(f"Platform: {diagnostics.results['device_info'].get('platform', 'Unknown')}")
        print()
        
        # System Health
        print("=== System Health ===")
        health = diagnostics.results['system_health']
        print(f"CPU Usage: {health.get('cpu_percent', 'Unknown')}%")
        print(f"Memory Usage: {health.get('memory_percent', 'Unknown')}%")
        if health.get('cpu_temperature'):
            print(f"CPU Temperature: {health['cpu_temperature']:.1f}°C")
        print()
        
        # Service Status
        print("=== Service Status ===")
        services = diagnostics.results.get('service_status', {}).get('services', {})
        for service, status in services.items():
            if isinstance(status, dict):
                state = "ACTIVE" if status.get('active', False) else "INACTIVE"
                print(f"{service}: {state}")
        print()
        
        # Recommendations
        print("=== Recommendations ===")
        recommendations = diagnostics.results.get('recommendations', [])
        if recommendations:
            for rec in recommendations:
                priority = rec['priority'].upper()
                print(f"[{priority}] {rec['issue']}")
                print(f"  Recommendation: {rec['recommendation']}")
                print(f"  Action: {rec['action']}")
                print()
        else:
            print("No issues detected.")

    # Exit with appropriate code
    critical_issues = [r for r in diagnostics.results.get('recommendations', [])
                      if r['priority'] == 'critical']
    if critical_issues:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
