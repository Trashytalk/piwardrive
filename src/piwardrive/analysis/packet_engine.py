"""
Packet Analysis Engine for PiWardrive
Real-time protocol analysis, topology mapping, and traffic classification
"""

import struct
import socket
import time
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict, deque
import hashlib
import ipaddress
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class ProtocolType(Enum):
    """Network protocol types"""
    IEEE_802_11 = "802.11"
    ETHERNET = "ethernet"
    IP = "ip"
    TCP = "tcp"
    UDP = "udp"
    ICMP = "icmp"
    HTTP = "http"
    HTTPS = "https"
    DNS = "dns"
    DHCP = "dhcp"
    ARP = "arp"
    UNKNOWN = "unknown"

class PacketDirection(Enum):
    """Packet direction"""
    INBOUND = "inbound"
    OUTBOUND = "outbound"
    LATERAL = "lateral"
    UNKNOWN = "unknown"

class AnomalyType(Enum):
    """Protocol anomaly types"""
    MALFORMED_PACKET = "malformed_packet"
    PROTOCOL_VIOLATION = "protocol_violation"
    UNUSUAL_TRAFFIC_PATTERN = "unusual_traffic_pattern"
    SUSPICIOUS_PAYLOAD = "suspicious_payload"
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"
    UNEXPECTED_PROTOCOL = "unexpected_protocol"

@dataclass
class PacketHeader:
    """Generic packet header information"""
    timestamp: float
    length: int
    protocol: ProtocolType
    source: str
    destination: str
    direction: PacketDirection
    raw_data: bytes

@dataclass
class IEEE80211Frame:
    """IEEE 802.11 frame structure"""
    frame_control: int
    duration: int
    address1: str
    address2: str
    address3: str
    sequence_control: int
    address4: Optional[str] = None
    frame_type: str = "unknown"
    subtype: str = "unknown"
    payload: bytes = b""

@dataclass
class NetworkTopologyNode:
    """Network topology node"""
    mac_address: str
    ip_address: Optional[str] = None
    hostname: Optional[str] = None
    vendor: Optional[str] = None
    device_type: str = "unknown"
    first_seen: datetime = field(default_factory=datetime.now)
    last_seen: datetime = field(default_factory=datetime.now)
    packet_count: int = 0
    bytes_transferred: int = 0
    connections: Set[str] = field(default_factory=set)
    protocols: Set[ProtocolType] = field(default_factory=set)

@dataclass
class NetworkConnection:
    """Network connection between two nodes"""
    source: str
    destination: str
    protocol: ProtocolType
    port: Optional[int] = None
    connection_type: str = "unknown"
    first_seen: datetime = field(default_factory=datetime.now)
    last_seen: datetime = field(default_factory=datetime.now)
    packet_count: int = 0
    bytes_transferred: int = 0
    flags: Set[str] = field(default_factory=set)

@dataclass
class TrafficFlow:
    """Traffic flow classification"""
    flow_id: str
    source: str
    destination: str
    protocol: ProtocolType
    classification: str
    confidence: float
    bandwidth_usage: float
    duration: float
    packet_count: int
    byte_count: int
    flow_characteristics: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ProtocolAnomaly:
    """Protocol anomaly detection result"""
    anomaly_type: AnomalyType
    protocol: ProtocolType
    source: str
    destination: str
    description: str
    severity: str
    confidence: float
    timestamp: datetime
    packet_data: bytes
    additional_info: Dict[str, Any] = field(default_factory=dict)

class PacketParser:
    """Packet parsing and protocol analysis"""
    
    def __init__(self):
        self.oui_database = self._load_oui_database()
        self.protocol_parsers = {
            ProtocolType.IEEE_802_11: self._parse_802_11,
            ProtocolType.ETHERNET: self._parse_ethernet,
            ProtocolType.IP: self._parse_ip,
            ProtocolType.TCP: self._parse_tcp,
            ProtocolType.UDP: self._parse_udp,
            ProtocolType.HTTP: self._parse_http,
            ProtocolType.DNS: self._parse_dns,
            ProtocolType.DHCP: self._parse_dhcp,
            ProtocolType.ARP: self._parse_arp
        }
    
    def parse_packet(self, raw_data: bytes, timestamp: float = None) -> Optional[PacketHeader]:
        """Parse raw packet data into structured format"""
        if timestamp is None:
            timestamp = time.time()
        
        if len(raw_data) < 14:  # Minimum Ethernet frame size
            return None
        
        try:
            # Determine protocol type from packet structure
            protocol = self._detect_protocol(raw_data)
            
            # Parse packet based on protocol
            if protocol in self.protocol_parsers:
                parsed_data = self.protocol_parsers[protocol](raw_data)
                if parsed_data:
                    return PacketHeader(
                        timestamp=timestamp,
                        length=len(raw_data),
                        protocol=protocol,
                        source=parsed_data.get('source', ''),
                        destination=parsed_data.get('destination', ''),
                        direction=self._determine_direction(parsed_data),
                        raw_data=raw_data
                    )
        except Exception as e:
            logger.error(f"Error parsing packet: {e}")
        
        return None
    
    def _detect_protocol(self, data: bytes) -> ProtocolType:
        """Detect protocol type from packet data"""
        if len(data) < 14:
            return ProtocolType.UNKNOWN
        
        # Check for 802.11 frame (radiotap header)
        if data[:2] == b'\x00\x00':
            return ProtocolType.IEEE_802_11
        
        # Check Ethernet frame
        ethertype = struct.unpack('!H', data[12:14])[0]
        if ethertype == 0x0800:  # IPv4
            return ProtocolType.IP
        elif ethertype == 0x0806:  # ARP
            return ProtocolType.ARP
        
        return ProtocolType.ETHERNET
    
    def _parse_802_11(self, data: bytes) -> Optional[Dict]:
        """Parse IEEE 802.11 frame"""
        if len(data) < 24:  # Minimum 802.11 frame size
            return None
        
        try:
            # Skip radiotap header if present
            if data[:2] == b'\x00\x00':
                radiotap_len = struct.unpack('<H', data[2:4])[0]
                data = data[radiotap_len:]
            
            if len(data) < 24:
                return None
            
            # Parse 802.11 header
            frame_control = struct.unpack('<H', data[0:2])[0]
            duration = struct.unpack('<H', data[2:4])[0]
            
            # Extract addresses
            addr1 = ':'.join(f'{b:02x}' for b in data[4:10])
            addr2 = ':'.join(f'{b:02x}' for b in data[10:16])
            addr3 = ':'.join(f'{b:02x}' for b in data[16:22])
            
            # Frame type and subtype
            frame_type = (frame_control >> 2) & 0x3
            subtype = (frame_control >> 4) & 0xF
            
            return {
                'source': addr2,
                'destination': addr1,
                'frame_control': frame_control,
                'duration': duration,
                'address1': addr1,
                'address2': addr2,
                'address3': addr3,
                'frame_type': frame_type,
                'subtype': subtype,
                'payload': data[24:]
            }
        except Exception as e:
            logger.error(f"Error parsing 802.11 frame: {e}")
            return None
    
    def _parse_ethernet(self, data: bytes) -> Optional[Dict]:
        """Parse Ethernet frame"""
        if len(data) < 14:
            return None
        
        try:
            # Extract MAC addresses
            dst_mac = ':'.join(f'{b:02x}' for b in data[0:6])
            src_mac = ':'.join(f'{b:02x}' for b in data[6:12])
            ethertype = struct.unpack('!H', data[12:14])[0]
            
            return {
                'source': src_mac,
                'destination': dst_mac,
                'ethertype': ethertype,
                'payload': data[14:]
            }
        except Exception as e:
            logger.error(f"Error parsing Ethernet frame: {e}")
            return None
    
    def _parse_ip(self, data: bytes) -> Optional[Dict]:
        """Parse IP packet"""
        if len(data) < 20:
            return None
        
        try:
            # Skip Ethernet header if present
            if len(data) >= 14:
                ethertype = struct.unpack('!H', data[12:14])[0]
                if ethertype == 0x0800:  # IPv4
                    data = data[14:]
            
            if len(data) < 20:
                return None
            
            # Parse IP header
            version_ihl = data[0]
            version = version_ihl >> 4
            ihl = version_ihl & 0xF
            header_length = ihl * 4
            
            if len(data) < header_length:
                return None
            
            protocol = data[9]
            src_ip = socket.inet_ntoa(data[12:16])
            dst_ip = socket.inet_ntoa(data[16:20])
            
            return {
                'source': src_ip,
                'destination': dst_ip,
                'version': version,
                'protocol': protocol,
                'header_length': header_length,
                'payload': data[header_length:]
            }
        except Exception as e:
            logger.error(f"Error parsing IP packet: {e}")
            return None
    
    def _parse_tcp(self, data: bytes) -> Optional[Dict]:
        """Parse TCP segment"""
        if len(data) < 20:
            return None
        
        try:
            # Parse TCP header
            src_port = struct.unpack('!H', data[0:2])[0]
            dst_port = struct.unpack('!H', data[2:4])[0]
            seq_num = struct.unpack('!I', data[4:8])[0]
            ack_num = struct.unpack('!I', data[8:12])[0]
            
            flags = struct.unpack('!H', data[12:14])[0]
            header_length = (flags >> 12) * 4
            
            tcp_flags = {
                'FIN': bool(flags & 0x01),
                'SYN': bool(flags & 0x02),
                'RST': bool(flags & 0x04),
                'PSH': bool(flags & 0x08),
                'ACK': bool(flags & 0x10),
                'URG': bool(flags & 0x20)
            }
            
            return {
                'source_port': src_port,
                'destination_port': dst_port,
                'sequence_number': seq_num,
                'acknowledgment_number': ack_num,
                'header_length': header_length,
                'flags': tcp_flags,
                'payload': data[header_length:]
            }
        except Exception as e:
            logger.error(f"Error parsing TCP segment: {e}")
            return None
    
    def _parse_udp(self, data: bytes) -> Optional[Dict]:
        """Parse UDP datagram"""
        if len(data) < 8:
            return None
        
        try:
            src_port = struct.unpack('!H', data[0:2])[0]
            dst_port = struct.unpack('!H', data[2:4])[0]
            length = struct.unpack('!H', data[4:6])[0]
            checksum = struct.unpack('!H', data[6:8])[0]
            
            return {
                'source_port': src_port,
                'destination_port': dst_port,
                'length': length,
                'checksum': checksum,
                'payload': data[8:]
            }
        except Exception as e:
            logger.error(f"Error parsing UDP datagram: {e}")
            return None
    
    def _parse_http(self, data: bytes) -> Optional[Dict]:
        """Parse HTTP traffic"""
        try:
            # Simple HTTP parsing
            text = data.decode('utf-8', errors='ignore')
            lines = text.split('\r\n')
            
            if not lines:
                return None
            
            # Parse request/response line
            first_line = lines[0]
            headers = {}
            
            # Parse headers
            for line in lines[1:]:
                if ':' in line:
                    key, value = line.split(':', 1)
                    headers[key.strip()] = value.strip()
                elif line == '':
                    break
            
            return {
                'first_line': first_line,
                'headers': headers,
                'is_request': any(method in first_line for method in ['GET', 'POST', 'PUT', 'DELETE']),
                'is_response': first_line.startswith('HTTP/')
            }
        except Exception as e:
            logger.error(f"Error parsing HTTP: {e}")
            return None
    
    def _parse_dns(self, data: bytes) -> Optional[Dict]:
        """Parse DNS query/response"""
        if len(data) < 12:
            return None
        
        try:
            # Parse DNS header
            query_id = struct.unpack('!H', data[0:2])[0]
            flags = struct.unpack('!H', data[2:4])[0]
            
            # Extract flag bits
            qr = (flags >> 15) & 0x1
            opcode = (flags >> 11) & 0xF
            aa = (flags >> 10) & 0x1
            tc = (flags >> 9) & 0x1
            rd = (flags >> 8) & 0x1
            ra = (flags >> 7) & 0x1
            rcode = flags & 0xF
            
            questions = struct.unpack('!H', data[4:6])[0]
            answers = struct.unpack('!H', data[6:8])[0]
            authority = struct.unpack('!H', data[8:10])[0]
            additional = struct.unpack('!H', data[10:12])[0]
            
            return {
                'query_id': query_id,
                'is_response': bool(qr),
                'opcode': opcode,
                'questions': questions,
                'answers': answers,
                'authority': authority,
                'additional': additional,
                'rcode': rcode,
                'payload': data[12:]
            }
        except Exception as e:
            logger.error(f"Error parsing DNS: {e}")
            return None
    
    def _parse_dhcp(self, data: bytes) -> Optional[Dict]:
        """Parse DHCP packet"""
        if len(data) < 236:
            return None
        
        try:
            # Parse DHCP header
            op = data[0]
            htype = data[1]
            hlen = data[2]
            hops = data[3]
            
            xid = struct.unpack('!I', data[4:8])[0]
            secs = struct.unpack('!H', data[8:10])[0]
            flags = struct.unpack('!H', data[10:12])[0]
            
            ciaddr = socket.inet_ntoa(data[12:16])
            yiaddr = socket.inet_ntoa(data[16:20])
            siaddr = socket.inet_ntoa(data[20:24])
            giaddr = socket.inet_ntoa(data[24:28])
            
            chaddr = ':'.join(f'{b:02x}' for b in data[28:28+hlen])
            
            return {
                'operation': 'request' if op == 1 else 'reply',
                'hardware_type': htype,
                'hardware_length': hlen,
                'transaction_id': xid,
                'client_ip': ciaddr,
                'your_ip': yiaddr,
                'server_ip': siaddr,
                'gateway_ip': giaddr,
                'client_hardware': chaddr,
                'options': data[236:]
            }
        except Exception as e:
            logger.error(f"Error parsing DHCP: {e}")
            return None
    
    def _parse_arp(self, data: bytes) -> Optional[Dict]:
        """Parse ARP packet"""
        if len(data) < 28:
            return None
        
        try:
            # Skip Ethernet header
            if len(data) >= 14:
                ethertype = struct.unpack('!H', data[12:14])[0]
                if ethertype == 0x0806:  # ARP
                    data = data[14:]
            
            if len(data) < 28:
                return None
            
            # Parse ARP header
            hardware_type = struct.unpack('!H', data[0:2])[0]
            protocol_type = struct.unpack('!H', data[2:4])[0]
            hardware_length = data[4]
            protocol_length = data[5]
            operation = struct.unpack('!H', data[6:8])[0]
            
            sender_hardware = ':'.join(f'{b:02x}' for b in data[8:14])
            sender_protocol = socket.inet_ntoa(data[14:18])
            target_hardware = ':'.join(f'{b:02x}' for b in data[18:24])
            target_protocol = socket.inet_ntoa(data[24:28])
            
            return {
                'source': sender_hardware,
                'destination': target_hardware,
                'operation': 'request' if operation == 1 else 'reply',
                'sender_hardware': sender_hardware,
                'sender_protocol': sender_protocol,
                'target_hardware': target_hardware,
                'target_protocol': target_protocol
            }
        except Exception as e:
            logger.error(f"Error parsing ARP: {e}")
            return None
    
    def _determine_direction(self, parsed_data: Dict) -> PacketDirection:
        """Determine packet direction based on addresses"""
        # This is a simplified implementation
        # In practice, would need network topology information
        return PacketDirection.UNKNOWN
    
    def _load_oui_database(self) -> Dict[str, str]:
        """Load OUI database for vendor identification"""
        # Simplified OUI database
        return {
            "00:11:22": "Cisco",
            "00:23:45": "Netgear",
            "00:34:56": "Linksys",
            "00:45:67": "D-Link",
            "00:56:78": "TP-Link"
        }

class TopologyMapper:
    """Network topology mapping and analysis"""
    
    def __init__(self):
        self.nodes: Dict[str, NetworkTopologyNode] = {}
        self.connections: Dict[str, NetworkConnection] = {}
        self.packet_parser = PacketParser()
    
    def process_packet(self, packet: PacketHeader):
        """Process packet for topology mapping"""
        # Update source node
        self._update_node(packet.source, packet)
        
        # Update destination node
        self._update_node(packet.destination, packet)
        
        # Update connection
        self._update_connection(packet)
    
    def _update_node(self, address: str, packet: PacketHeader):
        """Update node information"""
        if not address or address == "00:00:00:00:00:00":
            return
        
        if address not in self.nodes:
            self.nodes[address] = NetworkTopologyNode(
                mac_address=address,
                device_type=self._classify_device(address, packet),
                vendor=self._get_vendor(address)
            )
        
        node = self.nodes[address]
        node.last_seen = datetime.now()
        node.packet_count += 1
        node.bytes_transferred += packet.length
        node.protocols.add(packet.protocol)
    
    def _update_connection(self, packet: PacketHeader):
        """Update connection information"""
        if not packet.source or not packet.destination:
            return
        
        connection_id = f"{packet.source}-{packet.destination}"
        
        if connection_id not in self.connections:
            self.connections[connection_id] = NetworkConnection(
                source=packet.source,
                destination=packet.destination,
                protocol=packet.protocol,
                connection_type=self._classify_connection(packet)
            )
        
        connection = self.connections[connection_id]
        connection.last_seen = datetime.now()
        connection.packet_count += 1
        connection.bytes_transferred += packet.length
        
        # Update node connections
        if packet.source in self.nodes:
            self.nodes[packet.source].connections.add(packet.destination)
        if packet.destination in self.nodes:
            self.nodes[packet.destination].connections.add(packet.source)
    
    def _classify_device(self, address: str, packet: PacketHeader) -> str:
        """Classify device type based on traffic patterns"""
        # Simplified device classification
        vendor = self._get_vendor(address)
        
        if "router" in vendor.lower() or "gateway" in vendor.lower():
            return "router"
        elif "phone" in vendor.lower() or "mobile" in vendor.lower():
            return "mobile"
        elif "laptop" in vendor.lower() or "computer" in vendor.lower():
            return "computer"
        else:
            return "unknown"
    
    def _classify_connection(self, packet: PacketHeader) -> str:
        """Classify connection type"""
        if packet.protocol == ProtocolType.TCP:
            return "tcp_connection"
        elif packet.protocol == ProtocolType.UDP:
            return "udp_flow"
        elif packet.protocol == ProtocolType.IEEE_802_11:
            return "wireless_association"
        else:
            return "unknown"
    
    def _get_vendor(self, mac_address: str) -> str:
        """Get vendor from MAC address OUI"""
        if len(mac_address) >= 8:
            oui = mac_address[:8].upper()
            return self.packet_parser.oui_database.get(oui, "Unknown")
        return "Unknown"
    
    def get_topology_graph(self) -> Dict[str, Any]:
        """Get network topology as graph structure"""
        nodes = []
        edges = []
        
        for node in self.nodes.values():
            nodes.append({
                'id': node.mac_address,
                'label': node.hostname or node.mac_address,
                'type': node.device_type,
                'vendor': node.vendor,
                'packet_count': node.packet_count,
                'bytes_transferred': node.bytes_transferred,
                'protocols': list(node.protocols)
            })
        
        for connection in self.connections.values():
            edges.append({
                'source': connection.source,
                'target': connection.destination,
                'protocol': connection.protocol.value,
                'packet_count': connection.packet_count,
                'bytes_transferred': connection.bytes_transferred
            })
        
        return {
            'nodes': nodes,
            'edges': edges,
            'statistics': {
                'total_nodes': len(nodes),
                'total_connections': len(edges),
                'device_types': self._get_device_type_distribution(),
                'protocol_distribution': self._get_protocol_distribution()
            }
        }
    
    def _get_device_type_distribution(self) -> Dict[str, int]:
        """Get device type distribution"""
        distribution = defaultdict(int)
        for node in self.nodes.values():
            distribution[node.device_type] += 1
        return dict(distribution)
    
    def _get_protocol_distribution(self) -> Dict[str, int]:
        """Get protocol distribution"""
        distribution = defaultdict(int)
        for connection in self.connections.values():
            distribution[connection.protocol.value] += 1
        return dict(distribution)

class TrafficClassifier:
    """Traffic flow classification and analysis"""
    
    def __init__(self):
        self.flows: Dict[str, TrafficFlow] = {}
        self.classification_rules = self._load_classification_rules()
        self.flow_timeout = 300  # 5 minutes
    
    def classify_packet(self, packet: PacketHeader) -> Optional[str]:
        """Classify packet and update flow information"""
        flow_id = self._generate_flow_id(packet)
        
        if flow_id not in self.flows:
            self.flows[flow_id] = TrafficFlow(
                flow_id=flow_id,
                source=packet.source,
                destination=packet.destination,
                protocol=packet.protocol,
                classification="unknown",
                confidence=0.0,
                bandwidth_usage=0.0,
                duration=0.0,
                packet_count=0,
                byte_count=0
            )
        
        flow = self.flows[flow_id]
        flow.packet_count += 1
        flow.byte_count += packet.length
        
        # Update classification
        classification = self._classify_flow(flow, packet)
        if classification:
            flow.classification = classification['type']
            flow.confidence = classification['confidence']
        
        # Clean up old flows
        self._cleanup_old_flows()
        
        return flow.classification
    
    def _generate_flow_id(self, packet: PacketHeader) -> str:
        """Generate unique flow identifier"""
        # Create bidirectional flow ID
        addresses = sorted([packet.source, packet.destination])
        flow_key = f"{addresses[0]}-{addresses[1]}-{packet.protocol.value}"
        return hashlib.md5(flow_key.encode()).hexdigest()[:16]
    
    def _classify_flow(self, flow: TrafficFlow, packet: PacketHeader) -> Optional[Dict]:
        """Classify traffic flow based on patterns"""
        # Apply classification rules
        for rule in self.classification_rules:
            if self._matches_rule(flow, packet, rule):
                return {
                    'type': rule['classification'],
                    'confidence': rule['confidence']
                }
        
        # Port-based classification
        if packet.protocol in [ProtocolType.TCP, ProtocolType.UDP]:
            port_class = self._classify_by_port(packet)
            if port_class:
                return port_class
        
        # Pattern-based classification
        pattern_class = self._classify_by_pattern(flow)
        if pattern_class:
            return pattern_class
        
        return None
    
    def _matches_rule(self, flow: TrafficFlow, packet: PacketHeader, rule: Dict) -> bool:
        """Check if flow matches classification rule"""
        # Check protocol
        if 'protocol' in rule and packet.protocol != rule['protocol']:
            return False
        
        # Check packet size patterns
        if 'packet_size_range' in rule:
            min_size, max_size = rule['packet_size_range']
            if not (min_size <= packet.length <= max_size):
                return False
        
        # Check flow characteristics
        if 'min_packets' in rule and flow.packet_count < rule['min_packets']:
            return False
        
        return True
    
    def _classify_by_port(self, packet: PacketHeader) -> Optional[Dict]:
        """Classify traffic based on port numbers"""
        well_known_ports = {
            80: {'type': 'HTTP', 'confidence': 0.9},
            443: {'type': 'HTTPS', 'confidence': 0.9},
            53: {'type': 'DNS', 'confidence': 0.95},
            67: {'type': 'DHCP', 'confidence': 0.9},
            68: {'type': 'DHCP', 'confidence': 0.9},
            22: {'type': 'SSH', 'confidence': 0.9},
            23: {'type': 'Telnet', 'confidence': 0.9},
            25: {'type': 'SMTP', 'confidence': 0.9},
            110: {'type': 'POP3', 'confidence': 0.9},
            143: {'type': 'IMAP', 'confidence': 0.9},
            993: {'type': 'IMAPS', 'confidence': 0.9},
            995: {'type': 'POP3S', 'confidence': 0.9}
        }
        
        # Extract port information from packet
        # This would need to be implemented based on actual packet structure
        return None
    
    def _classify_by_pattern(self, flow: TrafficFlow) -> Optional[Dict]:
        """Classify traffic based on behavioral patterns"""
        # Video streaming patterns
        if flow.byte_count > 1000000 and flow.packet_count > 100:
            avg_packet_size = flow.byte_count / flow.packet_count
            if avg_packet_size > 1000:
                return {'type': 'Video Streaming', 'confidence': 0.7}
        
        # File transfer patterns
        if flow.byte_count > 10000000:  # 10MB
            return {'type': 'File Transfer', 'confidence': 0.6}
        
        # Web browsing patterns
        if flow.packet_count > 20 and flow.byte_count < 1000000:
            return {'type': 'Web Browsing', 'confidence': 0.5}
        
        return None
    
    def _load_classification_rules(self) -> List[Dict]:
        """Load traffic classification rules"""
        return [
            {
                'name': 'DNS Traffic',
                'protocol': ProtocolType.UDP,
                'packet_size_range': (50, 512),
                'classification': 'DNS',
                'confidence': 0.9
            },
            {
                'name': 'DHCP Traffic',
                'protocol': ProtocolType.UDP,
                'packet_size_range': (300, 600),
                'classification': 'DHCP',
                'confidence': 0.8
            },
            {
                'name': 'Streaming Media',
                'protocol': ProtocolType.UDP,
                'min_packets': 100,
                'classification': 'Media Streaming',
                'confidence': 0.7
            }
        ]
    
    def _cleanup_old_flows(self):
        """Clean up old inactive flows"""
        current_time = time.time()
        expired_flows = []
        
        for flow_id, flow in self.flows.items():
            # Calculate flow age based on last packet
            # This is simplified - would need actual timestamp tracking
            if current_time - flow.duration > self.flow_timeout:
                expired_flows.append(flow_id)
        
        for flow_id in expired_flows:
            del self.flows[flow_id]
    
    def get_traffic_statistics(self) -> Dict[str, Any]:
        """Get traffic classification statistics"""
        classification_counts = defaultdict(int)
        total_bytes = 0
        total_packets = 0
        
        for flow in self.flows.values():
            classification_counts[flow.classification] += 1
            total_bytes += flow.byte_count
            total_packets += flow.packet_count
        
        return {
            'total_flows': len(self.flows),
            'total_bytes': total_bytes,
            'total_packets': total_packets,
            'classification_distribution': dict(classification_counts),
            'top_flows': self._get_top_flows(5)
        }
    
    def _get_top_flows(self, count: int) -> List[Dict]:
        """Get top flows by byte count"""
        sorted_flows = sorted(
            self.flows.values(),
            key=lambda f: f.byte_count,
            reverse=True
        )
        
        return [
            {
                'flow_id': flow.flow_id,
                'source': flow.source,
                'destination': flow.destination,
                'classification': flow.classification,
                'byte_count': flow.byte_count,
                'packet_count': flow.packet_count
            }
            for flow in sorted_flows[:count]
        ]

class ProtocolAnomalyDetector:
    """Protocol anomaly detection engine"""
    
    def __init__(self):
        self.baseline_stats = defaultdict(dict)
        self.anomaly_thresholds = {
            'packet_rate': 1000,  # packets per second
            'byte_rate': 10000000,  # bytes per second
            'connection_rate': 100,  # connections per second
            'protocol_deviation': 0.3  # 30% deviation from baseline
        }
        self.detection_window = 60  # 1 minute
        self.packet_buffer = deque(maxlen=10000)
    
    def detect_anomalies(self, packet: PacketHeader) -> List[ProtocolAnomaly]:
        """Detect protocol anomalies in packet stream"""
        anomalies = []
        
        # Add packet to buffer
        self.packet_buffer.append(packet)
        
        # Check for various anomaly types
        anomalies.extend(self._detect_malformed_packets(packet))
        anomalies.extend(self._detect_protocol_violations(packet))
        anomalies.extend(self._detect_rate_anomalies())
        anomalies.extend(self._detect_pattern_anomalies())
        
        return anomalies
    
    def _detect_malformed_packets(self, packet: PacketHeader) -> List[ProtocolAnomaly]:
        """Detect malformed packets"""
        anomalies = []
        
        # Check packet structure
        if len(packet.raw_data) < 14:  # Minimum Ethernet frame
            anomalies.append(ProtocolAnomaly(
                anomaly_type=AnomalyType.MALFORMED_PACKET,
                protocol=packet.protocol,
                source=packet.source,
                destination=packet.destination,
                description="Packet too short",
                severity="medium",
                confidence=0.9,
                timestamp=datetime.now(),
                packet_data=packet.raw_data
            ))
        
        # Check for protocol-specific malformations
        if packet.protocol == ProtocolType.IP:
            anomalies.extend(self._check_ip_malformation(packet))
        elif packet.protocol == ProtocolType.TCP:
            anomalies.extend(self._check_tcp_malformation(packet))
        
        return anomalies
    
    def _detect_protocol_violations(self, packet: PacketHeader) -> List[ProtocolAnomaly]:
        """Detect protocol violations"""
        anomalies = []
        
        # Check for protocol layering violations
        if packet.protocol == ProtocolType.TCP:
            # Check TCP state violations
            violations = self._check_tcp_state_violations(packet)
            anomalies.extend(violations)
        
        return anomalies
    
    def _detect_rate_anomalies(self) -> List[ProtocolAnomaly]:
        """Detect rate-based anomalies"""
        anomalies = []
        
        if len(self.packet_buffer) < 100:  # Need sufficient data
            return anomalies
        
        # Calculate recent packet rate
        recent_packets = [p for p in self.packet_buffer 
                         if time.time() - p.timestamp < self.detection_window]
        
        if not recent_packets:
            return anomalies
        
        packet_rate = len(recent_packets) / self.detection_window
        
        # Check for rate anomalies
        if packet_rate > self.anomaly_thresholds['packet_rate']:
            anomalies.append(ProtocolAnomaly(
                anomaly_type=AnomalyType.RATE_LIMIT_EXCEEDED,
                protocol=ProtocolType.UNKNOWN,
                source="network",
                destination="network",
                description=f"High packet rate detected: {packet_rate:.1f} pps",
                severity="high",
                confidence=0.8,
                timestamp=datetime.now(),
                packet_data=b"",
                additional_info={'packet_rate': packet_rate}
            ))
        
        return anomalies
    
    def _detect_pattern_anomalies(self) -> List[ProtocolAnomaly]:
        """Detect unusual traffic patterns"""
        anomalies = []
        
        # Check for unusual protocol combinations
        recent_protocols = [p.protocol for p in self.packet_buffer 
                          if time.time() - p.timestamp < self.detection_window]
        
        if recent_protocols:
            protocol_counts = defaultdict(int)
            for protocol in recent_protocols:
                protocol_counts[protocol] += 1
            
            # Check for unexpected protocols
            total_packets = len(recent_protocols)
            for protocol, count in protocol_counts.items():
                ratio = count / total_packets
                
                # If a protocol suddenly appears with high frequency
                if protocol == ProtocolType.UNKNOWN and ratio > 0.1:
                    anomalies.append(ProtocolAnomaly(
                        anomaly_type=AnomalyType.UNEXPECTED_PROTOCOL,
                        protocol=protocol,
                        source="network",
                        destination="network",
                        description=f"Unexpected protocol frequency: {ratio:.1%}",
                        severity="medium",
                        confidence=0.6,
                        timestamp=datetime.now(),
                        packet_data=b"",
                        additional_info={'protocol_ratio': ratio}
                    ))
        
        return anomalies
    
    def _check_ip_malformation(self, packet: PacketHeader) -> List[ProtocolAnomaly]:
        """Check for IP packet malformations"""
        anomalies = []
        
        # Basic IP header validation would go here
        # This is a simplified implementation
        
        return anomalies
    
    def _check_tcp_malformation(self, packet: PacketHeader) -> List[ProtocolAnomaly]:
        """Check for TCP segment malformations"""
        anomalies = []
        
        # Basic TCP header validation would go here
        # This is a simplified implementation
        
        return anomalies
    
    def _check_tcp_state_violations(self, packet: PacketHeader) -> List[ProtocolAnomaly]:
        """Check for TCP state machine violations"""
        anomalies = []
        
        # TCP state tracking would go here
        # This is a simplified implementation
        
        return anomalies

class PacketAnalysisEngine:
    """Main packet analysis engine"""
    
    def __init__(self):
        self.packet_parser = PacketParser()
        self.topology_mapper = TopologyMapper()
        self.traffic_classifier = TrafficClassifier()
        self.anomaly_detector = ProtocolAnomalyDetector()
        self.packet_count = 0
        self.byte_count = 0
        self.start_time = time.time()
    
    def analyze_packet(self, raw_data: bytes, timestamp: float = None) -> Dict[str, Any]:
        """Analyze a single packet"""
        if timestamp is None:
            timestamp = time.time()
        
        # Parse packet
        packet = self.packet_parser.parse_packet(raw_data, timestamp)
        if not packet:
            return {'error': 'Failed to parse packet'}
        
        # Update statistics
        self.packet_count += 1
        self.byte_count += len(raw_data)
        
        # Process packet through analysis components
        results = {}
        
        # Topology mapping
        self.topology_mapper.process_packet(packet)
        
        # Traffic classification
        classification = self.traffic_classifier.classify_packet(packet)
        results['classification'] = classification
        
        # Anomaly detection
        anomalies = self.anomaly_detector.detect_anomalies(packet)
        results['anomalies'] = [
            {
                'type': a.anomaly_type.value,
                'protocol': a.protocol.value,
                'source': a.source,
                'destination': a.destination,
                'description': a.description,
                'severity': a.severity,
                'confidence': a.confidence
            }
            for a in anomalies
        ]
        
        # Packet details
        results['packet'] = {
            'timestamp': packet.timestamp,
            'length': packet.length,
            'protocol': packet.protocol.value,
            'source': packet.source,
            'destination': packet.destination,
            'direction': packet.direction.value
        }
        
        return results
    
    def get_analysis_summary(self) -> Dict[str, Any]:
        """Get comprehensive analysis summary"""
        runtime = time.time() - self.start_time
        
        return {
            'runtime_seconds': runtime,
            'total_packets': self.packet_count,
            'total_bytes': self.byte_count,
            'packets_per_second': self.packet_count / runtime if runtime > 0 else 0,
            'bytes_per_second': self.byte_count / runtime if runtime > 0 else 0,
            'topology': self.topology_mapper.get_topology_graph(),
            'traffic_statistics': self.traffic_classifier.get_traffic_statistics(),
            'protocols_detected': len(set(p.protocol for p in self.topology_mapper.nodes.values()))
        }

# Example usage and testing
def test_packet_analysis_engine():
    """Test packet analysis engine functionality"""
    print("Testing Packet Analysis Engine...")
    
    # Create analysis engine
    engine = PacketAnalysisEngine()
    
    # Generate sample packet data
    sample_packets = [
        # Sample Ethernet frame with IP packet
        bytes.fromhex('001122334455006677889900080045000028000040004006f38ac0a80001c0a800020050005000000000000000005002000000000000'),
        # Sample ARP packet
        bytes.fromhex('ffffffffffff001122334455080600010800060400010011223344550c0a80010000000000000c0a8001'),
        # Sample smaller packet
        bytes.fromhex('001122334455006677889900080045000014000040004006f38ac0a80001c0a80002')
    ]
    
    # Analyze packets
    results = []
    for i, packet_data in enumerate(sample_packets):
        print(f"\nAnalyzing packet {i+1}...")
        result = engine.analyze_packet(packet_data)
        results.append(result)
        
        if 'error' in result:
            print(f"  Error: {result['error']}")
        else:
            print(f"  Protocol: {result['packet']['protocol']}")
            print(f"  Source: {result['packet']['source']}")
            print(f"  Destination: {result['packet']['destination']}")
            print(f"  Classification: {result.get('classification', 'unknown')}")
            print(f"  Anomalies: {len(result.get('anomalies', []))}")
    
    # Get analysis summary
    summary = engine.get_analysis_summary()
    print(f"\nAnalysis Summary:")
    print(f"  Total packets: {summary['total_packets']}")
    print(f"  Total bytes: {summary['total_bytes']}")
    print(f"  Packets per second: {summary['packets_per_second']:.2f}")
    print(f"  Network nodes: {summary['topology']['statistics']['total_nodes']}")
    print(f"  Network connections: {summary['topology']['statistics']['total_connections']}")
    print(f"  Traffic flows: {summary['traffic_statistics']['total_flows']}")
    
    print("Packet Analysis Engine test completed!")

if __name__ == "__main__":
    test_packet_analysis_engine()
