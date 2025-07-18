#!/usr/bin/env python3
"""
Mobile Diagnostic Tool for PiWardrive Field Technicians
Lightweight diagnostic tool that can be run from a mobile device or laptop
"""

import argparse
import json
import logging
import socket
import subprocess
import sys
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

import requests


class MobileDiagnostics:
    """Mobile diagnostic tool for field technicians"""

    def __init__(self, target_ip: str = None):
        self.target_ip = target_ip or self._discover_device()
        self.base_url = f"http://{self.target_ip}:8000"
        self.device_info = {}

    def _discover_device(self) -> Optional[str]:
        """Auto-discover PiWardrive device on network"""
        print("Searching for PiWardrive devices...")

        # Get local network range
        local_ip = self._get_local_ip()
        if not local_ip:
            return None

        network = ".".join(local_ip.split(".")[:-1]) + "."

        # Scan common IPs
        for i in [1, 100, 101, 150, 200]:
            test_ip = f"{network}{i}"
            if self._test_piwardrive_api(test_ip):
                print(f"Found PiWardrive device at {test_ip}")
                return test_ip

        # Try mDNS resolution
        try:
            import socket

            ip = socket.gethostbyname("piwardrive.local")
            if self._test_piwardrive_api(ip):
                print(f"Found PiWardrive device at {ip} (via mDNS)")
                return ip
        except Exception as e:
            print(f"mDNS discovery failed: {e}")

        print("No PiWardrive devices found automatically")
        return None

    def _get_local_ip(self) -> Optional[str]:
        """Get local IP address"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                return s.getsockname()[0]
        except:
            return None

    def _test_piwardrive_api(self, ip: str) -> bool:
        """Test if IP has PiWardrive API"""
        try:
            response = requests.get(f"http://{ip}:8000/api/v1/system/health", timeout=2)
            return response.status_code == 200
        except:
            return False

    def run_quick_check(self) -> Dict[str, Any]:
        """Run quick diagnostic check"""
        print(f"Running quick diagnostics on {self.target_ip}...")

        results = {
            "timestamp": datetime.now().isoformat(),
            "target_ip": self.target_ip,
            "connectivity": {},
            "api_status": {},
            "system_health": {},
            "services": {},
            "recommendations": [],
        }

        # Test connectivity
        results["connectivity"] = self._test_connectivity()

        # Test API endpoints
        results["api_status"] = self._test_api_endpoints()

        # Get system health
        results["system_health"] = self._get_system_health()

        # Check services
        results["services"] = self._check_services()

        # Generate recommendations
        results["recommendations"] = self._generate_mobile_recommendations(results)

        return results

    def _test_connectivity(self) -> Dict[str, Any]:
        """Test basic connectivity"""
        connectivity = {
            "ping": False,
            "http": False,
            "api": False,
            "response_time": None,
        }

        # Ping test
        try:
            if sys.platform == "win32":
                result = subprocess.run(
                    ["ping", "-n", "1", self.target_ip], capture_output=True, timeout=5
                )
            else:
                result = subprocess.run(
                    ["ping", "-c", "1", self.target_ip], capture_output=True, timeout=5
                )
            connectivity["ping"] = result.returncode == 0
        except:
            pass

        # HTTP test
        try:
            start_time = time.time()
            response = requests.get(f"http://{self.target_ip}:8000", timeout=5)
            connectivity["response_time"] = time.time() - start_time
            connectivity["http"] = response.status_code == 200
        except:
            pass

        # API test
        try:
            response = requests.get(f"{self.base_url}/api/v1/system/health", timeout=5)
            connectivity["api"] = response.status_code == 200
        except:
            pass

        return connectivity

    def _test_api_endpoints(self) -> Dict[str, Any]:
        """Test critical API endpoints"""
        endpoints = {
            "/api/v1/system/health": "System Health",
            "/api/v1/system/status": "System Status",
            "/api/v1/gps/status": "GPS Status",
            "/api/v1/network/status": "Network Status",
            "/api/v1/services/status": "Services Status",
        }

        results = {}
        for endpoint, description in endpoints.items():
            try:
                response = requests.get(f"{self.base_url}{endpoint}", timeout=3)
                results[endpoint] = {
                    "status": response.status_code,
                    "accessible": response.status_code == 200,
                    "description": description,
                }
                if response.status_code == 200:
                    results[endpoint]["data"] = response.json()
            except Exception as e:
                results[endpoint] = {
                    "status": "error",
                    "accessible": False,
                    "description": description,
                    "error": str(e),
                }

        return results

    def _get_system_health(self) -> Dict[str, Any]:
        """Get system health information"""
        try:
            response = requests.get(f"{self.base_url}/api/v1/system/health", timeout=5)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            return {"error": str(e)}

        return {}

    def _check_services(self) -> Dict[str, Any]:
        """Check service status"""
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/services/status", timeout=5
            )
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            return {"error": str(e)}

        return {}

    def _generate_mobile_recommendations(
        self, results: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate recommendations for mobile diagnostics"""
        recommendations = []

        # Connectivity issues
        if not results["connectivity"]["api"]:
            recommendations.append(
                {
                    "priority": "critical",
                    "category": "connectivity",
                    "issue": "API not accessible",
                    "action": "Check network connection and device power",
                    "details": "Cannot communicate with PiWardrive API",
                }
            )

        # Response time issues
        response_time = results["connectivity"].get("response_time")
        if response_time and response_time > 2.0:
            recommendations.append(
                {
                    "priority": "warning",
                    "category": "performance",
                    "issue": "Slow response time",
                    "action": "Check network quality and device load",
                    "details": f"Response time: {response_time:.2f}s (should be < 2s)",
                }
            )

        # API endpoint issues
        failed_endpoints = [
            ep
            for ep, data in results["api_status"].items()
            if not data.get("accessible", False)
        ]
        if failed_endpoints:
            recommendations.append(
                {
                    "priority": "high",
                    "category": "api",
                    "issue": f"{len(failed_endpoints)} API endpoints not accessible",
                    "action": "Check service status and restart if needed",
                    "details": f'Failed endpoints: {", ".join(failed_endpoints)}',
                }
            )

        # System health issues
        health = results["system_health"]
        if isinstance(health, dict):
            cpu_percent = health.get("cpu_usage")
            if cpu_percent and cpu_percent > 90:
                recommendations.append(
                    {
                        "priority": "high",
                        "category": "performance",
                        "issue": "High CPU usage",
                        "action": "Check for runaway processes or restart system",
                        "details": f"CPU usage: {cpu_percent}%",
                    }
                )

            memory_percent = health.get("memory_usage")
            if memory_percent and memory_percent > 95:
                recommendations.append(
                    {
                        "priority": "critical",
                        "category": "performance",
                        "issue": "Critical memory usage",
                        "action": "Restart system immediately",
                        "details": f"Memory usage: {memory_percent}%",
                    }
                )

            temperature = health.get("cpu_temperature")
            if temperature and temperature > 75:
                recommendations.append(
                    {
                        "priority": "critical",
                        "category": "thermal",
                        "issue": "High CPU temperature",
                        "action": "Check cooling and reduce load",
                        "details": f"CPU temperature: {temperature}°C",
                    }
                )

        return recommendations

    def remote_reboot(self) -> bool:
        """Remotely reboot the device"""
        try:
            response = requests.post(
                f"{self.base_url}/api/v1/system/reboot", timeout=10
            )
            return response.status_code in [200, 202]
        except:
            return False

    def remote_restart_services(self) -> bool:
        """Remotely restart PiWardrive services"""
        try:
            response = requests.post(
                f"{self.base_url}/api/v1/services/restart", timeout=30
            )
            return response.status_code in [200, 202]
        except:
            return False

    def get_log_summary(self) -> List[str]:
        """Get recent log entries"""
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/logs/recent?lines=50", timeout=10
            )
            if response.status_code == 200:
                return response.json().get("logs", [])
        except:
            pass
        return []

    def generate_support_bundle(self) -> Optional[str]:
        """Generate support bundle for remote assistance"""
        try:
            response = requests.post(
                f"{self.base_url}/api/v1/support/bundle", timeout=60
            )
            if response.status_code == 200:
                return response.json().get("download_url")
        except:
            pass
        return None

    def run_daemon_mode(self):
        """Run in daemon mode for continuous monitoring"""
        print("🔄 Starting mobile diagnostics daemon mode...")
        logging.info("Starting mobile diagnostics daemon mode")

        # Set up signal handlers for graceful shutdown
        import signal
        import time

        def signal_handler(signum, frame):
            logging.info(f"Received signal {signum}, shutting down daemon")
            print("🛑 Daemon shutting down...")
            sys.exit(0)

        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)

        # Main daemon loop
        scan_interval = 300  # 5 minutes

        while True:
            try:
                print(f"🔍 Scanning for PiWardrive devices...")
                devices = scan_network_for_devices()

                if devices:
                    print(f"📱 Found {len(devices)} devices")

                    for device in devices:
                        try:
                            # Update base URL for this device
                            self.base_url = f"http://{device['ip']}:{device.get('port', 8000)}"

                            # Run quick diagnostics
                            results = self.run_quick_check()

                            # Check for critical issues
                            critical_issues = [
                                r for r in results["recommendations"]
                                if r["priority"] == "critical"
                            ]

                            if critical_issues:
                                self._send_daemon_alert(device, critical_issues)

                            # Save results with timestamp
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            output_file = f"/tmp/mobile_diagnostics_{device['ip']}_{timestamp}.json"

                            with open(output_file, 'w') as f:
                                json.dump(results, f, indent=2)

                            logging.info(f"Diagnostics completed for {device['ip']}")

                        except Exception as e:
                            logging.error(f"Error diagnosing device {device['ip']}: {e}")

                else:
                    print("❌ No PiWardrive devices found")
                    logging.info("No PiWardrive devices found in scan")

                print(f"😴 Sleeping for {scan_interval} seconds...")
                time.sleep(scan_interval)

            except Exception as e:
                logging.error(f"Error in daemon mode: {e}")
                time.sleep(60)  # Wait 1 minute before retrying

    def _send_daemon_alert(self, device: Dict[str, Any], issues: List[Dict[str, Any]]):
        """Send alert for critical issues in daemon mode"""
        try:
            # Write to syslog
            import syslog
            syslog.openlog("piwardrive-mobile-diagnostics")

            device_info = f"{device['ip']} ({device.get('hostname', 'unknown')})"

            for issue in issues:
                message = f"CRITICAL: {device_info} - {issue['issue']}"
                syslog.syslog(syslog.LOG_ERR, message)
                print(f"🚨 ALERT: {message}")

            syslog.closelog()

            # Also write to dedicated alert file
            alert_file = "/tmp/piwardrive_mobile_alerts.log"
            with open(alert_file, 'a') as f:
                timestamp = datetime.now().isoformat()
                issue_summary = ', '.join([i['issue'] for i in issues])
                f.write(f"{timestamp}: CRITICAL ALERT - {device_info} - {issue_summary}\n")

        except Exception as e:
            logging.error(f"Failed to send alert: {e}")


def get_local_ip() -> Optional[str]:
    """Get local IP address"""
    try:
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except:
        return None


def probe_piwardrive_device(ip: str) -> Optional[Dict[str, Any]]:
    """Probe a specific IP for PiWardrive device"""
    try:
        # Try health endpoint first
        response = requests.get(f"http://{ip}:8000/api/v1/system/health", timeout=2)
        if response.status_code == 200:
            health_data = response.json()

            # Get device info
            device_info = {
                "ip": ip,
                "status": "healthy",
                "health": health_data
            }

            # Try to get additional info
            try:
                info_response = requests.get(f"http://{ip}:8000/api/info", timeout=2)
                if info_response.status_code == 200:
                    info_data = info_response.json()
                    device_info.update({
                        "device_id": info_data.get("id"),
                        "version": info_data.get("version"),
                        "capabilities": info_data.get("capabilities", [])
                    })
            except:
                pass

            return device_info
    except Exception:
        pass

    # Try legacy API endpoint
    try:
        response = requests.get(f"http://{ip}:8000/api/status", timeout=2)
        if response.status_code == 200:
            return {
                "ip": ip,
                "status": "responding",
                "api_version": "legacy"
            }
    except Exception:
        pass

    return None


def discover_via_broadcast() -> List[Dict[str, Any]]:
    """Discover devices via UDP broadcast"""
    devices = []

    try:
        import socket

        # Create UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.settimeout(2)

        # Send discovery broadcast
        discovery_msg = b"PIWARDRIVE_DISCOVERY_REQUEST"
        sock.sendto(discovery_msg, ('<broadcast>', 9999))

        # Listen for responses
        start_time = time.time()
        while time.time() - start_time < 3:  # 3 second timeout
            try:
                data, addr = sock.recvfrom(1024)
                if data.startswith(b"PIWARDRIVE_DISCOVERY_RESPONSE"):
                    device_info = {
                        "ip": addr[0],
                        "status": "discovered",
                        "discovery_method": "broadcast"
                    }

                    # Parse response data if available
                    try:
                        response_data = data.decode('utf-8').split(':', 1)
                        if len(response_data) > 1:
                            import json
                            device_data = json.loads(response_data[1])
                            device_info.update(device_data)
                    except:
                        pass

                    devices.append(device_info)
            except socket.timeout:
                break

        sock.close()
    except Exception:
        pass

    return devices


def scan_network_for_devices() -> List[Dict[str, Any]]:
    """Scan network for PiWardrive devices"""
    devices = []

    # Get local network range
    local_ip = get_local_ip()
    if not local_ip:
        return devices

    network = ".".join(local_ip.split(".")[:-1]) + "."

    # Common IP addresses to check
    common_ips = [
        "1", "100", "101", "150", "200", "10", "11", "12", "20", "21", "22",
        "50", "51", "52", "99", "102", "103", "104", "105", "110", "111", "112"
    ]

    print("Scanning network range for PiWardrive devices...")

    # Scan common IPs
    for ip_suffix in common_ips:
        test_ip = f"{network}{ip_suffix}"
        device_info = probe_piwardrive_device(test_ip)
        if device_info:
            devices.append(device_info)
            print(f"  Found device at {test_ip}")

    # Try mDNS resolution
    try:
        import socket
        ip = socket.gethostbyname("piwardrive.local")
        if ip not in [d['ip'] for d in devices]:
            device_info = probe_piwardrive_device(ip)
            if device_info:
                devices.append(device_info)
                print(f"  Found device at {ip} (via mDNS)")
    except Exception:
        pass

    # Try broadcast discovery (if available)
    try:
        broadcast_devices = discover_via_broadcast()
        for device in broadcast_devices:
            if device['ip'] not in [d['ip'] for d in devices]:
                devices.append(device)
                print(f"  Found device at {device['ip']} (via broadcast)")
    except Exception:
        pass

    return devices


def print_results(results: Dict[str, Any]):
    """Print diagnostic results in a readable format"""
    print("\n" + "=" * 60)
    print(f"PiWardrive Mobile Diagnostics - {results['timestamp']}")
    print(f"Target Device: {results['target_ip']}")
    print("=" * 60)

    # Connectivity
    print("\n🌐 Connectivity:")
    conn = results["connectivity"]
    print(f"  Ping: {'✅' if conn['ping'] else '❌'}")
    print(f"  HTTP: {'✅' if conn['http'] else '❌'}")
    print(f"  API: {'✅' if conn['api'] else '❌'}")
    if conn["response_time"]:
        print(f"  Response Time: {conn['response_time']:.2f}s")

    # API Status
    print("\n🔌 API Endpoints:")
    api_status = results["api_status"]
    for endpoint, data in api_status.items():
        status = "✅" if data["accessible"] else "❌"
        print(f"  {data['description']}: {status}")

    # System Health
    print("\n💻 System Health:")
    health = results["system_health"]
    if isinstance(health, dict) and "error" not in health:
        cpu = health.get("cpu_usage", "Unknown")
        memory = health.get("memory_usage", "Unknown")
        temp = health.get("cpu_temperature", "Unknown")
        print(f"  CPU Usage: {cpu}%")
        print(f"  Memory Usage: {memory}%")
        print(f"  CPU Temperature: {temp}°C")
    else:
        print("  ❌ Could not retrieve system health")

    # Services
    print("\n⚙️  Services:")
    services = results["services"]
    if isinstance(services, dict) and "error" not in services:
        for service, status in services.items():
            status_icon = "✅" if status else "❌"
            print(f"  {service}: {status_icon}")
    else:
        print("  ❌ Could not retrieve service status")

    # Recommendations
    print("\n💡 Recommendations:")
    recommendations = results["recommendations"]
    if recommendations:
        for rec in recommendations:
            priority_icon = {
                "critical": "🔴",
                "high": "🟠",
                "warning": "🟡",
                "info": "🔵",
            }.get(rec["priority"], "⚪")

            print(f"  {priority_icon} {rec['issue']}")
            print(f"     Action: {rec['action']}")
            if rec.get("details"):
                print(f"     Details: {rec['details']}")
    else:
        print("  ✅ No issues detected")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="PiWardrive Mobile Diagnostic Tool")
    parser.add_argument("--ip", "-i", help="Target device IP address")
    parser.add_argument("--scan", "-s", action="store_true", help="Scan for devices")
    parser.add_argument("--reboot", action="store_true", help="Remotely reboot device")
    parser.add_argument("--restart", action="store_true", help="Restart services")
    parser.add_argument("--logs", action="store_true", help="Show recent logs")
    parser.add_argument(
        "--support", action="store_true", help="Generate support bundle"
    )
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    parser.add_argument("--daemon", action="store_true", help="Run in daemon mode")

    args = parser.parse_args()

    if args.scan:
        print("Scanning for PiWardrive devices...")

        # Perform network scan
        devices = scan_network_for_devices()

        if not devices:
            print("❌ No PiWardrive devices found on network")
            print("   Make sure devices are powered on and accessible")
            return

        print(f"✅ Found {len(devices)} PiWardrive device(s):")
        for i, device in enumerate(devices, 1):
            print(f"   {i}. {device['ip']} - {device['status']}")
            if device.get("capabilities"):
                print(f"      Capabilities: {', '.join(device['capabilities'])}")
            if device.get("version"):
                print(f"      Version: {device['version']}")
            if device.get("device_id"):
                print(f"      Device ID: {device['device_id']}")
            print()

        if args.json:
            print(json.dumps(devices, indent=2))

        return

    # Create diagnostic tool
    try:
        diagnostics = MobileDiagnostics(args.ip)
        if not diagnostics.target_ip:
            print("❌ Could not find or connect to PiWardrive device")
            print("   Try specifying IP with --ip option")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Error initializing diagnostics: {e}")
        sys.exit(1)

    # Handle special actions
    if args.reboot:
        print("🔄 Rebooting device...")
        if diagnostics.remote_reboot():
            print("✅ Reboot command sent successfully")
        else:
            print("❌ Failed to send reboot command")
        return

    if args.restart:
        print("🔄 Restarting services...")
        if diagnostics.remote_restart_services():
            print("✅ Service restart command sent successfully")
        else:
            print("❌ Failed to send service restart command")
        return

    if args.logs:
        print("📋 Recent logs:")
        logs = diagnostics.get_log_summary()
        for log in logs[-20:]:  # Show last 20 lines
            print(f"  {log}")
        return

    if args.support:
        print("📦 Generating support bundle...")
        url = diagnostics.generate_support_bundle()
        if url:
            print(f"✅ Support bundle available at: {url}")
        else:
            print("❌ Failed to generate support bundle")
        return

    if args.daemon:
        diagnostics.run_daemon_mode()
        return

    # Run diagnostics
    try:
        results = diagnostics.run_quick_check()

        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print_results(results)

        # Exit with error code if critical issues found
        critical_issues = [
            r for r in results["recommendations"] if r["priority"] == "critical"
        ]
        sys.exit(1 if critical_issues else 0)

    except Exception as e:
        print(f"❌ Diagnostic failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
