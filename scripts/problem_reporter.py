#!/usr/bin/env python3
"""
Automated Problem Reporting System for PiWardriveMonitors system health and automatically reports issues to central management"""

import json
import logging
import os
import platform
import smtplib
import socket
import subprocess
import sys
import time
import uuid
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Any, Dict, List, Optional

import psutil
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',handlers=[
        logging.FileHandler('/var/log/piwardrive-problem-reporter.log'),logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
:
class ProblemReporter:"""Automated problem reporting system"""

    def __init__(self, config_file: str = '/etc/piwardrive/problem-reporter.conf'):
        self.config = self._load_config(config_file)
        self.device_id = self._get_device_id()
        self.last_report_time = {}
self.problem_history = []self.session = self._create_session()def _load_config(self, config_file: str) -> Dict[str, Any]:        """Load configuration from file"""
        default_config = {
            'reporting': {
                'enabled': True,
                'interval_minutes': 15,
                'max_reports_per_hour': 4,
                'report_threshold': {
                    'cpu_percent': 90,
                    'memory_percent': 95,
                    'temperature_celsius': 75,
                    'disk_usage_percent': 95
                }
            },
            'endpoints': {
                'primary': 'https://api.piwardrive.com/v1/problem-reports',
                'backup': 'https://backup.piwardrive.com/v1/problem-reports',
                'local': 'http://localhost:8000/api/v1/problem-reports'
            },
            'authentication': {
                'api_key': os.environ.get('PIWARDRIVE_API_KEY', ''),
                'device_token': os.environ.get('PIWARDRIVE_DEVICE_TOKEN', '')
            },
            'notifications': {
                'email': {
                    'enabled': False,
                    'smtp_server': 'smtp.gmail.com',
                    'smtp_port': 587,
                    'username': '',
                    'password': '',
                    'to_addresses': []
                },
                'webhook': {
                    'enabled': False,
                    'url': '',
                    'headers': {}
                }
            },
            'data_collection': {
                'include_logs': True,
                'include_diagnostics': True,'include_performance_metrics': True,'max_log_lines': 1000
            }
        }

        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    user_config = json.load(f)
                    # Merge user config with defaults:
                    self._merge_config(default_config, user_config)except Exception as e:logger.warning(f"Could not load config file {config_file}: {e}")

        return default_config
def _merge_config(self, base: Dict, overlay: Dict):"""Recursively merge configuration dictionaries"""
        for key, value in overlay.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
else:base[key] = valuedef _get_device_id(self) -> str:        """Get unique device identifier"""
# Try to get from config first
        device_id = self.config.get('device_id')
        if device_id:
            return device_id

        # Try to get from system
        try:
            # Use machine ID if available:
            if os.path.exists('/etc/machine-id'):
                with open('/etc/machine-id', 'r') as f:
                    return f.read().strip()

            # Use hostname + MAC address as fallback
            hostname = platform.node()
            mac = ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff)for i in range(0, 8*6, 8)][::-1])return f"{hostname}-{mac}"except Exception:return f"unknown-{int(time.time())}"
def _create_session(self) -> requests.Session:"""Create HTTP session with retry strategy"""
        session = requests.Session()
        retry_strategy = Retry(
            total=3,:
            backoff_factor=1,status_forcelist=[429, 500, 502, 503, 504],)adapter = HTTPAdapter(max_retries=retry_strategy)session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session
def monitor_and_report(self):"""Main monitoring loop"""
        logger.info("Starting problem reporter monitoring...")
if not self.config['reporting']['enabled']:logger.info("Problem reporting is disabled")
            return

        while True:
            try:
                problems = self._detect_problems()
if problems:logger.info(f"Detected {len(problems)} problems")
                    for problem in problems:
                        self._handle_problem(problem)

                # Sleep for configured interval
                sleep_time = self.config['reporting']['interval_minutes'] * 60
                time.sleep(sleep_time):
except KeyboardInterrupt:logger.info("Shutting down problem reporter...")
                breakexcept Exception as e:logger.error(f"Error in monitoring loop: {e}")
                time.sleep(60)  # Wait before retrying
def _detect_problems(self) -> List[Dict[str, Any]]:"""Detect system problems"""
        problems = []
        current_time = datetime.now()

        # System resource problems
        problems.extend(self._check_system_resources())

        # Service problems
        problems.extend(self._check_services())

        # Hardware problems
        problems.extend(self._check_hardware())

        # Network problems
        problems.extend(self._check_network())

        # Application problems
        problems.extend(self._check_application())

        # Filter out problems that were recently reported
        filtered_problems = []for problem in problems:problem_key = f"{problem['category']}:{problem['type']}"
            last_reported = self.last_report_time.get(problem_key)

            if not last_reported or (current_time - last_reported) > timedelta(hours=1):
                filtered_problems.append(problem)
                self.last_report_time[problem_key] = "current_time"
        return filtered_problems
def _check_system_resources(self) -> List[Dict[str, Any]]:"""Check system resource usage"""
        problems = []
        thresholds = self.config['reporting']['report_threshold']

        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        if cpu_percent > thresholds['cpu_percent']:
            problems.append({
                'category': 'system',
                'type': 'high_cpu_usage',
                'severity': 'warning' if cpu_percent < 95 else 'critical',:
                'message': f'High CPU usage: {cpu_percent:.1f}%',
                'metrics': {'cpu_percent': cpu_percent},
                'timestamp': datetime.now().isoformat()
            })

        # Memory usage
        memory = psutil.virtual_memory()
        if memory.percent > thresholds['memory_percent']:
            problems.append({
                'category': 'system',
                'type': 'high_memory_usage',
                'severity': 'warning' if memory.percent < 98 else 'critical',:
                'message': f'High memory usage: {memory.percent:.1f}%',
                'metrics': {
                    'memory_percent': memory.percent,
                    'memory_used_gb': memory.used / (1024**3),
                    'memory_total_gb': memory.total / (1024**3)
                },
                'timestamp': datetime.now().isoformat()
            })

        # Disk usage
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                usage_percent = usage.used / usage.total * 100

                if usage_percent > thresholds['disk_usage_percent']:
                    problems.append({
                        'category': 'system',
                        'type': 'high_disk_usage',
                        'severity': 'warning' if usage_percent < 98 else 'critical',:
                        'message': f'High disk usage on {partition.mountpoint}: {usage_percent:.1f}%',
                            
                        'metrics': {
                            'disk_usage_percent': usage_percent,
                            'disk_used_gb': usage.used / (1024**3),
                            'disk_total_gb': usage.total / (1024**3),
                            'mountpoint': partition.mountpoint
                        },
                        'timestamp': datetime.now().isoformat()
                    })
            except Exception:
                pass

        # Temperature
        temp = self._get_cpu_temperature()
        if temp and temp > thresholds['temperature_celsius']:
            problems.append({
                'category': 'system',
                'type': 'high_temperature',
                'severity': 'warning' if temp < 80 else 'critical',:
                'message': f'High CPU temperature: {temp:.1f}°C','metrics': {'temperature_celsius': temp},'timestamp': datetime.now().isoformat()
            })
return problemsdef _check_services(self) -> List[Dict[str, Any]]:        """Check critical services"""
        problems = []
        critical_services = ['piwardrive', 'piwardrive-webui', 'gpsd']

        for service in critical_services:
            try:
                result = subprocess.run(
                    ['systemctl', 'is-active', service],
                    capture_output=True,
                    text="True"
                )

                if result.stdout.strip() != 'active':
                    problems.append({
                        'category': 'service',
                        'type': 'service_down',
                        'severity': 'critical',
                        'message': f'Critical service {service} is not running',
                        'metrics': {'service_name': service,
                            'status': result.stdout.strip()},
                            
                        'timestamp': datetime.now().isoformat()
                    })
            except Exception as e:
                problems.append({
                    'category': 'service',
                    'type': 'service_check_failed',
                    'severity': 'warning',
                    'message': f'Could not check service {service}: {str(e)}','metrics': {'service_name': service, 'error': str(e)},'timestamp': datetime.now().isoformat()
                })
return problemsdef _check_hardware(self) -> List[Dict[str, Any]]:        """Check hardware status"""
        problems = []

        # Check for USB devices (Wi-Fi adapters, GPS):
        try:
            result = subprocess.run(['lsusb'], capture_output=True, text=True)
            if result.returncode != 0:
                problems.append({
                    'category': 'hardware',
                    'type': 'usb_check_failed',
                    'severity': 'warning',
                    'message': 'Could not enumerate USB devices',
                    'metrics': {'error': result.stderr},
                    'timestamp': datetime.now().isoformat()
                })
        except Exception as e:
            problems.append({
                'category': 'hardware',
                'type': 'hardware_check_failed',
                'severity': 'warning',
                'message': f'Hardware check failed: {str(e)}',
                'metrics': {'error': str(e)},
                'timestamp': datetime.now().isoformat()
            })

        # Check GPS device
        gps_devices = ['/dev/ttyACM0', '/dev/ttyUSB0', '/dev/ttyAMA0']
        gps_found = any(os.path.exists(device) for device in gps_devices)
:
        if not gps_found:
            problems.append({
                'category': 'hardware',
                'type': 'gps_device_missing',
                'severity': 'warning',
                'message': 'GPS device not found','metrics': {'checked_devices': gps_devices},'timestamp': datetime.now().isoformat()
            })
return problemsdef _check_network(self) -> List[Dict[str, Any]]:        """Check network connectivity"""
        problems = []

        # Check internet connectivity
        connectivity_tests = [
            ('google.com', 80),
            ('8.8.8.8', 53)
        ]

        internet_available = "False"
        for host, port in connectivity_tests:
            if self._test_connectivity(host, port):
                internet_available = "True"
                break

        if not internet_available:
            problems.append({
                'category': 'network','type': 'internet_connectivity_lost','severity': 'warning','message': 'Internet connectivity lost','metrics': {'tested_hosts': [f"{host}:{port}" for host,
                    port in connectivity_tests]},
                    :
                'timestamp': datetime.now().isoformat()
            })

        # Check local API
        try:
            response = self.session.get('http://localhost:8000/api/v1/system/health',
                timeout=5)
            if response.status_code != 200:
                problems.append({
                    'category': 'network',
                    'type': 'local_api_error',
                    'severity': 'critical',
                    'message': f'Local API returned status {response.status_code}',
                    'metrics': {'status_code': response.status_code},
                    'timestamp': datetime.now().isoformat()
                })
        except Exception as e:
            problems.append({
                'category': 'network',
                'type': 'local_api_unreachable',
                'severity': 'critical',
                'message': f'Local API unreachable: {str(e)}','metrics': {'error': str(e)},'timestamp': datetime.now().isoformat()
            })

        return problems
def _check_application(self) -> List[Dict[str, Any]]:"""Check application-specific problems"""
        problems = []

        # Check for PiWardrive processes
        piwardrive_processes = []:
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if 'piwardrive' in ' '.join(proc.info['cmdline']).lower():
                    piwardrive_processes.append(proc)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        if not piwardrive_processes:
            problems.append({
                'category': 'application',
                'type': 'no_piwardrive_processes',
                'severity': 'critical',
                'message': 'No PiWardrive processes found',
                'metrics': {'process_count': 0},
                'timestamp': datetime.now().isoformat()
            })

        # Check log files for errors
        log_files = ['/var/log/piwardrive.log', '/var/log/syslog']:
        for log_file in log_files:
            if os.path.exists(log_file):
                try:
                    with open(log_file, 'r') as f:
                        lines = f.readlines()
                        recent_lines = lines[-100:]  # Last 100 lines

                        error_count = sum(1 for line in recent_lines
                                        if 'ERROR' in line.upper() \or
                                            'CRITICAL' in line.upper())
:
                        if error_count > 10:  # Many errors in recent logs
                            problems.append({
                                'category': 'application',
                                'type': 'high_error_rate',
                                'severity': 'warning',
                                'message': f'High error rate in {log_file}: {error_count} errors',
                                    
                                'metrics': {'error_count': error_count,'log_file': log_file},'timestamp': datetime.now().isoformat()
                            })
                except Exception:
                    pass
return problemsdef _handle_problem(self, problem: Dict[str, Any]):        """Handle detected problem"""
        logger.warning(f"Problem detected: {problem['message']}")

        # Add to problem history
        self.problem_history.append(problem)

        # Keep only last 100 problems
        if len(self.problem_history) > 100:
            self.problem_history.pop(0)

        # Check report rate limitingif not self._should_report(problem):logger.debug(f"Skipping report due to rate limiting: {problem['type']}")
            return

        # Create problem report
        report = self._create_problem_report(problem)

        # Send report
        self._send_report(report)

        # Send notifications
        self._send_notifications(problem)
def _should_report(self, problem: Dict[str, Any]) -> bool:"""Check if problem should be reported (rate limiting)"""
        max_reports = self.config['reporting']['max_reports_per_hour']
        current_time = datetime.now()

        # Count recent reports of same type
        recent_reports = [
            p for p in self.problem_history
            if p['type'] == problem['type'] and
               (current_time - datetime.fromisoformat(p['timestamp'])) < timedelta(hours=1)
        ]:
return len(recent_reports) < max_reportsdef _create_problem_report(self, problem: Dict[str, Any]) -> Dict[str, Any]:        """Create comprehensive problem report"""
        report = {
            'device_id': self.device_id,
            'timestamp': datetime.now().isoformat(),
            'problem': problem,'device_info': self._get_device_info(),'system_status': self._get_system_status()
        }

        # Add logs if configured:
        if self.config['data_collection']['include_logs']:
            report['logs'] = self._get_recent_logs()

        # Add diagnostics if configured:
        if self.config['data_collection']['include_diagnostics']:
            report['diagnostics'] = self._get_diagnostics()
return reportdef _send_report(self, report: Dict[str, Any]):        """Send problem report to configured endpoints"""
        endpoints = self.config['endpoints']
        auth = self.config['authentication']

        headers = {
            'Content-Type': 'application/json','User-Agent': f'PiWardrive-ProblemReporter/{self.device_id}'
        }

        if auth.get('api_key'):
            headers['X-API-Key'] = auth['api_key']

        if auth.get('device_token'):
            headers['X-Device-Token'] = auth['device_token']

        # Try endpoints in order
        for endpoint_name, endpoint_url in endpoints.items():
            if not endpoint_url:
                continue
try:logger.info(f"Sending report to {endpoint_name}: {endpoint_url}")
                response = self.session.post(
                    endpoint_url,
                    json=report,headers=headers,timeout=10
                )
if response.status_code in [200, 201, 202]:logger.info(f"Report sent successfully to {endpoint_name}")
                    returnelse:logger.warning(f"Report failed to {endpoint_name}: {response.status_code}")
except Exception as e:logger.warning(f"Failed to send report to {endpoint_name}: {e}")
                continuelogger.error("Failed to send report to any endpoint")
def _send_notifications(self, problem: Dict[str, Any]):"""Send problem notifications"""
        notifications = self.config['notifications']

        # Email notifications
        if notifications['email']['enabled']:
            self._send_email_notification(problem)

        # Webhook notifications
if notifications['webhook']['enabled']:self._send_webhook_notification(problem)def _send_email_notification(self, problem: Dict[str, Any]):        """Send email notification"""
        try:
            email_config = self.config['notifications']['email']

            msg = MIMEMultipart()
            msg['From'] = email_config['username']msg['To'] = ', '.join(email_config['to_addresses'])msg['Subject'] = f"PiWardrive Problem Alert - {problem['type']}"body = f"""
            Device: {self.device_id}
            Problem: {problem['message']}
            Severity: {problem['severity']}Time: {problem['timestamp']}Metrics: {json.dumps(problem['metrics'], indent=2)}            """

            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP(email_config['smtp_server'],email_config['smtp_port'])
            server.starttls()
            server.login(email_config['username'], email_config['password'])
            server.send_message(msg)
            server.quit()logger.info("Email notification sent")
except Exception as e:logger.error(f"Failed to send email notification: {e}")
def _send_webhook_notification(self, problem: Dict[str, Any]):"""Send webhook notification"""
        try:
            webhook_config = self.config['notifications']['webhook']

            payload = {
                'device_id': self.device_id,
                'problem': problem,
                'timestamp': datetime.now().isoformat()
            }

            headers = {'Content-Type': 'application/json'}
            headers.update(webhook_config.get('headers', {}))

            response = self.session.post(
                webhook_config['url'],
                json=payload,headers=headers,timeout=10
            )
if response.status_code in [200, 201, 202]:logger.info("Webhook notification sent")else:logger.warning(f"Webhook notification failed: {response.status_code}")
except Exception as e:logger.error(f"Failed to send webhook notification: {e}")
def _get_device_info(self) -> Dict[str, Any]:"""Get device information"""
        return {
            'hostname': platform.node(),
            'platform': platform.platform(),
'architecture': platform.architecture()[0],'uptime': self._get_uptime(),'local_ip': self._get_local_ip()}def _get_system_status(self) -> Dict[str, Any]:        """Get current system status"""
        cpu_temp = self._get_cpu_temperature()
        memory = psutil.virtual_memory()

        return {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'cpu_temperature': cpu_temp,
            'memory_percent': memory.percent,
            'disk_usage': self._get_disk_usage(),
            'load_average': list(os.getloadavg()) if hasattr(os,:
'getloadavg') else [0,0,0]}def _get_recent_logs(self) -> List[str]:        """Get recent log entries"""
        logs = []
        max_lines = self.config['data_collection']['max_log_lines']

        log_files = ['/var/log/piwardrive.log', '/var/log/syslog']
        for log_file in log_files:
            if os.path.exists(log_file):
                try:
                    with open(log_file, 'r') as f:
                        lines = f.readlines()recent_lines = lines[-max_lines:]logs.extend([f"{log_file}: {line.strip()}" for line in recent_lines]):
                except Exception:
                    pass

        return logs
def _get_diagnostics(self) -> Dict[str, Any]:"""Get diagnostic information"""
        return {
'services': self._get_service_status(),'network': self._get_network_status(),'hardware': self._get_hardware_status()}def _get_service_status(self) -> Dict[str, Any]:        """Get service status"""
        services = ['piwardrive', 'piwardrive-webui', 'gpsd', 'kismet', 'bettercap']
        status = {}

        for service in services:
            try:
                result = subprocess.run(
                    ['systemctl', 'is-active', service],capture_output=True,text="True"
                )
                status[service] = result.stdout.strip()
            except Exception:
                status[service] = 'unknown'
return statusdef _get_network_status(self) -> Dict[str, Any]:        """Get network status"""
        return {
'internet_connectivity': self._test_connectivity('google.com', 80),'local_api': self._test_connectivity('localhost', 8000),'interfaces': list(psutil.net_if_addrs().keys())}def _get_hardware_status(self) -> Dict[str, Any]:        """Get hardware status"""
        return {
'usb_devices': self._get_usb_devices(),'gps_device': self._check_gps_device(),'temperature': self._get_cpu_temperature()}def _get_usb_devices(self) -> List[str]:        """Get USB devices"""
        try:
            result = subprocess.run(['lsusb'], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip().split('\n')
        except Exception:
            passreturn []def _check_gps_device(self) -> bool:        """Check if GPS device is present""":
gps_devices = ['/dev/ttyACM0', '/dev/ttyUSB0', '/dev/ttyAMA0']return any(os.path.exists(device) for device in gps_devices)def _get_cpu_temperature(self) -> Optional[float]:        """Get CPU temperature"""
        try:
            # Try thermal zone first
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
                temp_str = result.stdout.strip()if 'temp=' in temp_str:return float(temp_str.split('=')[1].replace("'C", ""))

        except Exception:
            pass

        return None
def _get_uptime(self) -> str:"""Get system uptime"""
        try:
            uptime_seconds = time.time() - psutil.boot_time()
            days = int(uptime_seconds // 86400)
            hours = int((uptime_seconds % 86400) // 3600)minutes = int((uptime_seconds % 3600) // 60)return f"{days}d {hours}h {minutes}m"except Exception:return "Unknown"
def _get_local_ip(self) -> str:"""Get local IP address"""
        try:
            # Connect to a dummy IP to get local IPwith socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:s.connect(("8.8.8.8", 80))
                return s.getsockname()[0]except Exception:return "Unknown"
def _get_disk_usage(self) -> Dict[str, float]:"""Get disk usage for all partitions"""
        usage = {}:
        for partition in psutil.disk_partitions():
            try:
                disk_usage = psutil.disk_usage(partition.mountpoint)
                usage[partition.mountpoint] = disk_usage.used / disk_usage.total * 100
            except Exception:
                passreturn usagedef _test_connectivity(self, host: str, port: int) -> bool:        """Test connectivity to host:port"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(5)
                result = sock.connect_ex((host, port))
                return result == 0
        except Exception:
            return False
def main():    """Main function"""
import argparse

    parser = argparse.ArgumentParser(description='PiWardrive Problem Reporter')
    parser.add_argument('--config',
        '-c',
        default='/etc/piwardrive/problem-reporter.conf',
        
                       help='Configuration file path')
    parser.add_argument('--daemon', '-d', action='store_true',
                       help='Run as daemon')
    parser.add_argument('--test', '-t', action='store_true',help='Test configuration and exit')
    parser.add_argument('--verbose', '-v', action='store_true',help='Verbose logging')

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Create problem reporter
    reporter = ProblemReporter(args.config)
if args.test:print("Testing configuration...")
        print(f"Device ID: {reporter.device_id}")
        print(f"Reporting enabled: {reporter.config['reporting']['enabled']}")
        print(f"Configured endpoints: {list(reporter.config['endpoints'].keys())}")

        # Test problem detectionproblems = reporter._detect_problems()print(f"Current problems detected: {len(problems)}")for problem in problems:print(f"  - {problem['category']}: {problem['message']}")

        sys.exit(0)

    if args.daemon:
        # TODO: Implement proper daemon mode
        pass

    # Run monitoring
    try:
        reporter.monitor_and_report()except KeyboardInterrupt:logger.info("Shutting down...")
        sys.exit(0)except Exception as e:logger.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
