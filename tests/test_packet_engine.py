"""
Comprehensive test suite for PiWardrive Packet Analysis Engine.

Tests packet analysis core, protocol analysis, topology mapping, and traffic classification.
"""

import struct
import time
from datetime import datetime, timedelta

import pytest

from piwardrive.analysis.packet_engine import (
    AnomalyType,
    FlowInfo,
    NetworkTopology,
    PacketAnalysisEngine,
    PacketDirection,
    PacketInfo,
    ProtocolType,
    TrafficClassifier,
)


class TestProtocolType:
    """Test protocol type enumeration."""

    def test_protocol_type_values(self):
        """Test that all expected protocol types exist."""
        assert ProtocolType.IEEE_802_11.value == "802.11"
        assert ProtocolType.ETHERNET.value == "ethernet"
        assert ProtocolType.IP.value == "ip"
        assert ProtocolType.TCP.value == "tcp"
        assert ProtocolType.UDP.value == "udp"
        assert ProtocolType.ICMP.value == "icmp"
        assert ProtocolType.HTTP.value == "http"
        assert ProtocolType.HTTPS.value == "https"
        assert ProtocolType.DNS.value == "dns"
        assert ProtocolType.DHCP.value == "dhcp"
        assert ProtocolType.ARP.value == "arp"
        assert ProtocolType.UNKNOWN.value == "unknown"

    def test_protocol_hierarchy(self):
        """Test protocol hierarchy relationships."""
        # Test that we can distinguish between protocol types
        assert ProtocolType.TCP != ProtocolType.UDP
        assert ProtocolType.HTTP != ProtocolType.HTTPS
        assert ProtocolType.IEEE_802_11 != ProtocolType.ETHERNET


class TestPacketDirection:
    """Test packet direction enumeration."""

    def test_packet_direction_values(self):
        """Test packet direction values."""
        assert PacketDirection.INBOUND.value == "inbound"
        assert PacketDirection.OUTBOUND.value == "outbound"
        assert PacketDirection.LATERAL.value == "lateral"
        assert PacketDirection.UNKNOWN.value == "unknown"


class TestAnomalyType:
    """Test anomaly type enumeration."""

    def test_anomaly_type_values(self):
        """Test anomaly type values."""
        assert AnomalyType.MALFORMED_PACKET.value == "malformed_packet"
        # Add other anomaly types as they're defined


class TestPacketInfo:
    """Test packet information dataclass."""

    def test_packet_info_creation(self):
        """Test creating a PacketInfo instance."""
        packet = PacketInfo(
            timestamp=datetime.now(),
            protocol=ProtocolType.TCP,
            source_ip="192.168.1.100",
            dest_ip="192.168.1.1",
            source_port=12345,
            dest_port=80,
            payload_size=1024,
            direction=PacketDirection.OUTBOUND,
        )

        assert packet.protocol == ProtocolType.TCP
        assert packet.source_ip == "192.168.1.100"
        assert packet.dest_ip == "192.168.1.1"
        assert packet.source_port == 12345
        assert packet.dest_port == 80
        assert packet.payload_size == 1024
        assert packet.direction == PacketDirection.OUTBOUND

    def test_packet_info_validation(self):
        """Test packet info validation."""
        # Test with minimal required fields
        packet = PacketInfo(
            timestamp=datetime.now(),
            protocol=ProtocolType.ICMP,
            source_ip="10.0.0.1",
            dest_ip="10.0.0.2",
        )

        assert packet.protocol == ProtocolType.ICMP
        assert packet.source_ip == "10.0.0.1"
        assert packet.dest_ip == "10.0.0.2"


class TestFlowInfo:
    """Test flow information tracking."""

    def test_flow_info_creation(self):
        """Test creating a FlowInfo instance."""
        flow = FlowInfo(
            flow_id="192.168.1.100:12345->192.168.1.1:80",
            protocol=ProtocolType.TCP,
            source_ip="192.168.1.100",
            dest_ip="192.168.1.1",
            source_port=12345,
            dest_port=80,
            start_time=datetime.now(),
            packet_count=150,
            byte_count=102400,
        )

        assert flow.flow_id == "192.168.1.100:12345->192.168.1.1:80"
        assert flow.protocol == ProtocolType.TCP
        assert flow.packet_count == 150
        assert flow.byte_count == 102400

    def test_flow_metrics_calculation(self):
        """Test flow metrics calculation."""
        start_time = datetime.now()
        end_time = start_time + timedelta(seconds=60)

        flow = FlowInfo(
            flow_id="test_flow",
            protocol=ProtocolType.TCP,
            source_ip="192.168.1.100",
            dest_ip="192.168.1.1",
            start_time=start_time,
            end_time=end_time,
            packet_count=120,
            byte_count=61440,
        )

        # Calculate packets per second
        duration = (end_time - start_time).total_seconds()
        pps = flow.packet_count / duration
        assert pps == 2.0  # 120 packets / 60 seconds

        # Calculate bits per second
        bps = (flow.byte_count * 8) / duration
        assert bps == 8192.0  # 61440 * 8 / 60


class TestPacketAnalysisEngine:
    """Test packet analysis engine core functionality."""

    @pytest.fixture
    def analysis_engine(self):
        """Create a packet analysis engine for testing."""
        engine = PacketAnalysisEngine()
        return engine

    def test_engine_initialization(self, analysis_engine):
        """Test analysis engine initialization."""
        assert analysis_engine is not None
        assert hasattr(analysis_engine, "protocols")
        assert hasattr(analysis_engine, "flows")
        assert hasattr(analysis_engine, "anomalies")

    def test_packet_parsing_ethernet(self, analysis_engine):
        """Test Ethernet packet parsing."""
        # Create mock Ethernet frame
        eth_header = struct.pack(
            "!6s6sH",
            b"\x00\x11\x22\x33\x44\x55",  # Dest MAC
            b"\x66\x77\x88\x99\xaa\xbb",  # Src MAC
            0x0800,  # IPv4 ethertype
        )

        packet_info = analysis_engine.parse_ethernet_frame(eth_header)

        assert packet_info.protocol == ProtocolType.ETHERNET
        assert packet_info.source_mac == "66:77:88:99:aa:bb"
        assert packet_info.dest_mac == "00:11:22:33:44:55"

    def test_packet_parsing_ipv4(self, analysis_engine):
        """Test IPv4 packet parsing."""
        # Create mock IPv4 header
        ip_header = struct.pack(
            "!BBHHHBBH4s4s",
            0x45,  # Version & IHL
            0x00,  # Type of Service
            40,  # Total Length
            12345,  # Identification
            0x4000,  # Flags & Fragment Offset
            64,  # TTL
            6,  # Protocol (TCP)
            0x0000,  # Header Checksum
            struct.pack("!I", 0xC0A80164),  # Source IP (192.168.1.100)
            struct.pack("!I", 0xC0A80101),  # Dest IP (192.168.1.1)
        )

        packet_info = analysis_engine.parse_ipv4_packet(ip_header)

        assert packet_info.protocol == ProtocolType.IP
        assert packet_info.source_ip == "192.168.1.100"
        assert packet_info.dest_ip == "192.168.1.1"
        assert packet_info.ttl == 64

    def test_packet_parsing_tcp(self, analysis_engine):
        """Test TCP packet parsing."""
        # Create mock TCP header
        tcp_header = struct.pack(
            "!HHLLBBHHH",
            12345,  # Source Port
            80,  # Dest Port
            0x12345678,  # Sequence Number
            0x87654321,  # Acknowledgment Number
            0x50,  # Data Offset
            0x18,  # Flags (PSH, ACK)
            8192,  # Window Size
            0x0000,  # Checksum
            0x0000,  # Urgent Pointer
        )

        packet_info = analysis_engine.parse_tcp_packet(tcp_header)

        assert packet_info.protocol == ProtocolType.TCP
        assert packet_info.source_port == 12345
        assert packet_info.dest_port == 80
        assert packet_info.tcp_flags == 0x18

    def test_packet_parsing_udp(self, analysis_engine):
        """Test UDP packet parsing."""
        # Create mock UDP header
        udp_header = struct.pack(
            "!HHHH",
            53,  # Source Port (DNS)
            12345,  # Dest Port
            8,  # Length
            0x0000,  # Checksum
        )

        packet_info = analysis_engine.parse_udp_packet(udp_header)

        assert packet_info.protocol == ProtocolType.UDP
        assert packet_info.source_port == 53
        assert packet_info.dest_port == 12345

    def test_flow_tracking(self, analysis_engine):
        """Test network flow tracking."""
        # Create test packets for a flow
        packets = []
        for i in range(10):
            packet = PacketInfo(
                timestamp=datetime.now() + timedelta(seconds=i),
                protocol=ProtocolType.TCP,
                source_ip="192.168.1.100",
                dest_ip="192.168.1.1",
                source_port=12345,
                dest_port=80,
                payload_size=1024,
                direction=PacketDirection.OUTBOUND,
            )
            packets.append(packet)

        # Process packets through flow tracker
        for packet in packets:
            analysis_engine.track_flow(packet)

        # Check flow was created and tracked
        flows = analysis_engine.get_active_flows()
        assert len(flows) >= 1

        # Find our flow
        test_flow = None
        for flow in flows:
            if (
                flow.source_ip == "192.168.1.100"
                and flow.dest_ip == "192.168.1.1"
                and flow.source_port == 12345
            ):
                test_flow = flow
                break

        assert test_flow is not None
        assert test_flow.packet_count == 10
        assert test_flow.byte_count == 10240  # 10 * 1024

    def test_protocol_classification(self, analysis_engine):
        """Test protocol classification."""
        # Test HTTP classification
        http_packet = PacketInfo(
            timestamp=datetime.now(),
            protocol=ProtocolType.TCP,
            source_ip="192.168.1.100",
            dest_ip="192.168.1.1",
            source_port=12345,
            dest_port=80,
            payload=b"GET /index.html HTTP/1.1\r\n",
        )

        classified_protocol = analysis_engine.classify_protocol(http_packet)
        assert classified_protocol == ProtocolType.HTTP

        # Test HTTPS classification
        https_packet = PacketInfo(
            timestamp=datetime.now(),
            protocol=ProtocolType.TCP,
            source_ip="192.168.1.100",
            dest_ip="192.168.1.1",
            source_port=12345,
            dest_port=443,
            payload=b"\x16\x03\x01",  # TLS handshake
        )

        classified_protocol = analysis_engine.classify_protocol(https_packet)
        assert classified_protocol == ProtocolType.HTTPS

    def test_anomaly_detection(self, analysis_engine):
        """Test anomaly detection."""
        # Test malformed packet detection
        malformed_packet = PacketInfo(
            timestamp=datetime.now(),
            protocol=ProtocolType.TCP,
            source_ip="192.168.1.100",
            dest_ip="192.168.1.1",
            payload_size=-1,  # Invalid size
        )

        anomalies = analysis_engine.detect_anomalies(malformed_packet)
        assert len(anomalies) > 0
        assert AnomalyType.MALFORMED_PACKET in [a.type for a in anomalies]

    def test_bandwidth_calculation(self, analysis_engine):
        """Test bandwidth calculation."""
        # Create packets over time
        start_time = datetime.now()
        packets = []

        for i in range(100):
            packet = PacketInfo(
                timestamp=start_time + timedelta(milliseconds=i * 10),
                protocol=ProtocolType.TCP,
                source_ip="192.168.1.100",
                dest_ip="192.168.1.1",
                payload_size=1500,  # Standard Ethernet frame
            )
            packets.append(packet)
            analysis_engine.process_packet(packet)

        # Calculate bandwidth over 1 second window
        end_time = start_time + timedelta(seconds=1)
        bandwidth = analysis_engine.calculate_bandwidth(start_time, end_time)

        # 100 packets * 1500 bytes * 8 bits/byte = 1,200,000 bits/second
        assert bandwidth > 0
        assert isinstance(bandwidth, (int, float))


class TestNetworkTopology:
    """Test network topology mapping."""

    @pytest.fixture
    def topology_mapper(self):
        """Create a network topology mapper."""
        mapper = NetworkTopology()
        return mapper

    def test_topology_initialization(self, topology_mapper):
        """Test topology mapper initialization."""
        assert topology_mapper is not None
        assert hasattr(topology_mapper, "nodes")
        assert hasattr(topology_mapper, "edges")

    def test_node_discovery(self, topology_mapper):
        """Test network node discovery."""
        # Add test nodes
        nodes = [
            "192.168.1.1",  # Gateway
            "192.168.1.100",  # Client 1
            "192.168.1.101",  # Client 2
            "192.168.1.200",  # Server
        ]

        for node in nodes:
            topology_mapper.add_node(node)

        discovered_nodes = topology_mapper.get_nodes()
        assert len(discovered_nodes) == 4
        assert "192.168.1.1" in discovered_nodes
        assert "192.168.1.100" in discovered_nodes

    def test_connection_mapping(self, topology_mapper):
        """Test network connection mapping."""
        # Add connections
        connections = [
            ("192.168.1.100", "192.168.1.1"),  # Client to gateway
            ("192.168.1.101", "192.168.1.1"),  # Client to gateway
            ("192.168.1.1", "192.168.1.200"),  # Gateway to server
        ]

        for src, dst in connections:
            topology_mapper.add_connection(src, dst)

        # Test connection existence
        assert topology_mapper.has_connection("192.168.1.100", "192.168.1.1")
        assert topology_mapper.has_connection("192.168.1.1", "192.168.1.200")

        # Test connection metrics
        connection_count = topology_mapper.get_connection_count("192.168.1.1")
        assert connection_count >= 3  # Gateway has multiple connections

    def test_path_finding(self, topology_mapper):
        """Test path finding between nodes."""
        # Build test topology
        topology_mapper.add_connection("192.168.1.100", "192.168.1.1")
        topology_mapper.add_connection("192.168.1.1", "192.168.1.200")
        topology_mapper.add_connection("192.168.1.200", "10.0.0.1")

        # Find path
        path = topology_mapper.find_path("192.168.1.100", "10.0.0.1")

        assert path is not None
        assert len(path) >= 3
        assert path[0] == "192.168.1.100"
        assert path[-1] == "10.0.0.1"

    def test_network_segmentation(self, topology_mapper):
        """Test network segmentation detection."""
        # Create segmented network
        # Segment 1: 192.168.1.x
        topology_mapper.add_connection("192.168.1.100", "192.168.1.1")
        topology_mapper.add_connection("192.168.1.101", "192.168.1.1")

        # Segment 2: 10.0.0.x (isolated)
        topology_mapper.add_connection("10.0.0.100", "10.0.0.1")
        topology_mapper.add_connection("10.0.0.101", "10.0.0.1")

        segments = topology_mapper.detect_segments()
        assert len(segments) >= 2

    def test_topology_visualization_data(self, topology_mapper):
        """Test topology data for visualization."""
        # Add test network
        topology_mapper.add_connection("192.168.1.100", "192.168.1.1")
        topology_mapper.add_connection("192.168.1.101", "192.168.1.1")
        topology_mapper.add_connection("192.168.1.1", "8.8.8.8")

        viz_data = topology_mapper.get_visualization_data()

        assert "nodes" in viz_data
        assert "edges" in viz_data
        assert len(viz_data["nodes"]) >= 4
        assert len(viz_data["edges"]) >= 3


class TestTrafficClassifier:
    """Test traffic classification functionality."""

    @pytest.fixture
    def traffic_classifier(self):
        """Create a traffic classifier."""
        classifier = TrafficClassifier()
        return classifier

    def test_classifier_initialization(self, traffic_classifier):
        """Test traffic classifier initialization."""
        assert traffic_classifier is not None
        assert hasattr(traffic_classifier, "patterns")
        assert hasattr(traffic_classifier, "rules")

    def test_application_detection(self, traffic_classifier):
        """Test application protocol detection."""
        # Test web traffic
        web_packet = PacketInfo(
            timestamp=datetime.now(),
            protocol=ProtocolType.TCP,
            dest_port=80,
            payload=b"GET /index.html HTTP/1.1\r\n",
        )

        app_type = traffic_classifier.classify_application(web_packet)
        assert app_type == "HTTP"

        # Test SSH traffic
        ssh_packet = PacketInfo(
            timestamp=datetime.now(),
            protocol=ProtocolType.TCP,
            dest_port=22,
            payload=b"SSH-2.0-OpenSSH",
        )

        app_type = traffic_classifier.classify_application(ssh_packet)
        assert app_type == "SSH"

    def test_traffic_type_classification(self, traffic_classifier):
        """Test traffic type classification."""
        # Test streaming traffic (large payload, consistent timing)
        streaming_packet = PacketInfo(
            timestamp=datetime.now(),
            protocol=ProtocolType.UDP,
            dest_port=5004,  # RTP port
            payload_size=1500,
        )

        traffic_type = traffic_classifier.classify_traffic_type(streaming_packet)
        assert traffic_type in ["streaming", "media", "video"]

        # Test DNS traffic
        dns_packet = PacketInfo(
            timestamp=datetime.now(),
            protocol=ProtocolType.UDP,
            dest_port=53,
            payload_size=64,
        )

        traffic_type = traffic_classifier.classify_traffic_type(dns_packet)
        assert traffic_type == "DNS"

    def test_malicious_traffic_detection(self, traffic_classifier):
        """Test malicious traffic detection."""
        # Test port scan detection
        scan_packets = []
        for port in range(80, 90):
            packet = PacketInfo(
                timestamp=datetime.now(),
                protocol=ProtocolType.TCP,
                source_ip="192.168.1.100",
                dest_ip="192.168.1.200",
                dest_port=port,
                tcp_flags=0x02,  # SYN flag
            )
            scan_packets.append(packet)

        # Process scan packets
        for packet in scan_packets:
            traffic_classifier.detect_malicious_pattern(packet)

        # Should detect port scan pattern
        scan_detected = traffic_classifier.is_port_scan_detected("192.168.1.100")
        assert scan_detected is True

    def test_bandwidth_classification(self, traffic_classifier):
        """Test bandwidth-based classification."""
        # Test high bandwidth flow
        high_bw_packets = []
        for i in range(1000):
            packet = PacketInfo(
                timestamp=datetime.now() + timedelta(milliseconds=i),
                protocol=ProtocolType.TCP,
                source_ip="192.168.1.100",
                dest_ip="192.168.1.200",
                payload_size=1500,
            )
            high_bw_packets.append(packet)

        # Classify as high bandwidth
        for packet in high_bw_packets:
            traffic_classifier.classify_bandwidth(packet)

        flow_classification = traffic_classifier.get_flow_classification(
            "192.168.1.100", "192.168.1.200"
        )
        assert flow_classification in ["high", "bulk", "streaming"]


class TestPacketAnalysisIntegration:
    """Test integrated packet analysis functionality."""

    @pytest.fixture
    def integrated_analyzer(self):
        """Create integrated packet analyzer."""
        analyzer = PacketAnalysisEngine()
        analyzer.topology = NetworkTopology()
        analyzer.classifier = TrafficClassifier()
        return analyzer

    def test_full_packet_analysis_pipeline(self, integrated_analyzer):
        """Test complete packet analysis pipeline."""
        # Create test packet
        raw_packet = self._create_test_packet()

        # Process through full pipeline
        packet_info = integrated_analyzer.analyze_packet(raw_packet)

        assert packet_info is not None
        assert packet_info.protocol in [p.value for p in ProtocolType]
        assert packet_info.source_ip is not None
        assert packet_info.dest_ip is not None

    def test_real_time_analysis(self, integrated_analyzer):
        """Test real-time packet analysis."""
        # Simulate real-time packet stream
        packet_count = 1000
        processed_count = 0

        for i in range(packet_count):
            raw_packet = self._create_test_packet(sequence=i)

            # Process packet
            start_time = time.time()
            packet_info = integrated_analyzer.analyze_packet(raw_packet)
            processing_time = time.time() - start_time

            if packet_info:
                processed_count += 1

            # Ensure processing is fast enough for real-time
            assert processing_time < 0.001  # Less than 1ms per packet

        # Verify processing rate
        processing_rate = processed_count / packet_count
        assert processing_rate > 0.95  # 95% success rate

    def test_memory_usage_optimization(self, integrated_analyzer):
        """Test memory usage under load."""
        # Process many packets to test memory management
        for i in range(10000):
            raw_packet = self._create_test_packet(sequence=i)
            integrated_analyzer.analyze_packet(raw_packet)

        # Check that old flows are cleaned up
        active_flows = integrated_analyzer.get_active_flows()
        assert len(active_flows) < 1000  # Should cleanup old flows

    def test_concurrent_analysis(self, integrated_analyzer):
        """Test concurrent packet analysis."""
        import threading

        def analyze_packets(thread_id):
            for i in range(100):
                raw_packet = self._create_test_packet(sequence=i, thread_id=thread_id)
                integrated_analyzer.analyze_packet(raw_packet)

        # Create multiple analysis threads
        threads = []
        for thread_id in range(5):
            thread = threading.Thread(target=analyze_packets, args=(thread_id,))
            threads.append(thread)
            thread.start()

        # Wait for completion
        for thread in threads:
            thread.join(timeout=10)

        # Verify analyzer remained stable
        assert integrated_analyzer is not None
        flows = integrated_analyzer.get_active_flows()
        assert len(flows) > 0

    def _create_test_packet(self, sequence=0, thread_id=0):
        """Create a test packet for analysis."""
        # Create mock packet data
        eth_header = struct.pack(
            "!6s6sH",
            b"\x00\x11\x22\x33\x44\x55",  # Dest MAC
            b"\x66\x77\x88\x99\xaa\xbb",  # Src MAC
            0x0800,  # IPv4
        )

        # IPv4 header
        src_ip = 0xC0A80100 + (sequence % 254) + 1  # 192.168.1.x
        dst_ip = 0xC0A80100 + ((sequence + thread_id) % 254) + 1

        ip_header = struct.pack(
            "!BBHHHBBH4s4s",
            0x45,
            0x00,
            40,
            sequence,
            0x4000,
            64,
            6,
            0x0000,
            struct.pack("!I", src_ip),
            struct.pack("!I", dst_ip),
        )

        # TCP header
        tcp_header = struct.pack(
            "!HHLLBBHHH", 12345 + sequence, 80, sequence, 0, 0x50, 0x18, 8192, 0, 0
        )

        return eth_header + ip_header + tcp_header
