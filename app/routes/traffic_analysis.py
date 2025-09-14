"""
Network Traffic Analysis Module
Simulates network packet monitoring and analysis
"""
from flask import Blueprint, render_template, request, jsonify
import random
import time
import json
from datetime import datetime, timedelta
from collections import defaultdict

traffic_analysis_bp = Blueprint('traffic_analysis', __name__)

# Simulated network traffic data
traffic_log = []
suspicious_events = []

def generate_normal_traffic():
    """Generate normal network traffic patterns"""
    protocols = ['TCP', 'UDP', 'ICMP']
    common_ports = [80, 443, 53, 22, 25, 110, 143, 993, 995]
    
    traffic = {
        'timestamp': datetime.now(),
        'src_ip': f"192.168.1.{random.randint(10, 254)}",
        'dst_ip': f"10.0.0.{random.randint(1, 254)}",
        'protocol': random.choice(protocols),
        'src_port': random.randint(32768, 65535),
        'dst_port': random.choice(common_ports),
        'packet_size': random.randint(64, 1500),
        'flags': 'ACK' if random.random() > 0.3 else 'SYN',
        'payload_preview': generate_payload_preview(),
        'classification': 'normal'
    }
    
    return traffic

def generate_suspicious_traffic():
    """Generate suspicious network activities"""
    attack_types = [
        {
            'type': 'port_scan',
            'src_ip': '203.0.113.10',
            'dst_ip': '192.168.1.100',
            'pattern': 'Sequential port scanning',
            'ports': list(range(20, 100)),
            'protocol': 'TCP',
            'flags': 'SYN'
        },
        {
            'type': 'data_exfiltration',
            'src_ip': '192.168.1.150',
            'dst_ip': '198.51.100.50',
            'pattern': 'Large data upload',
            'ports': [443],
            'protocol': 'TCP',
            'flags': 'ACK',
            'size_multiplier': 10
        },
        {
            'type': 'ddos',
            'src_ip': f"203.0.113.{random.randint(1, 254)}",
            'dst_ip': '192.168.1.100',
            'pattern': 'High volume requests',
            'ports': [80, 443],
            'protocol': 'TCP',
            'flags': 'SYN'
        },
        {
            'type': 'malware_c2',
            'src_ip': '192.168.1.75',
            'dst_ip': '185.92.220.35',
            'pattern': 'Command and control communication',
            'ports': [8080, 8443],
            'protocol': 'TCP',
            'flags': 'ACK'
        }
    ]
    
    attack = random.choice(attack_types)
    
    traffic = {
        'timestamp': datetime.now(),
        'src_ip': attack['src_ip'],
        'dst_ip': attack['dst_ip'],
        'protocol': attack['protocol'],
        'src_port': random.randint(32768, 65535),
        'dst_port': random.choice(attack['ports']),
        'packet_size': random.randint(64, 1500) * attack.get('size_multiplier', 1),
        'flags': attack['flags'],
        'payload_preview': generate_malicious_payload(),
        'classification': 'suspicious',
        'attack_type': attack['type'],
        'pattern': attack['pattern']
    }
    
    return traffic

def generate_payload_preview():
    """Generate realistic payload previews"""
    payloads = [
        "GET /index.html HTTP/1.1\\r\\nHost: example.com",
        "POST /api/data HTTP/1.1\\r\\nContent-Type: application/json",
        "SMTP DATA\\r\\nFrom: user@example.com",
        "SSH-2.0-OpenSSH_8.0\\r\\n",
        "DNS Query: example.com A?"
    ]
    return random.choice(payloads)

def generate_malicious_payload():
    """Generate suspicious payload previews"""
    payloads = [
        "GET /admin/backup.sql HTTP/1.1",
        "POST /shell.php?cmd=whoami",
        "\\x90\\x90\\x90\\x90\\xcc\\xcc\\xcc",  # NOP sled
        "SELECT * FROM users WHERE id=1; DROP TABLE users;--",
        "powershell.exe -enc UwB0AGEAcgB0AC0AUAByAG8AYw"
    ]
    return random.choice(payloads)

@traffic_analysis_bp.route('/')
def index():
    """Traffic monitoring dashboard with integrated packet capture"""
    # Generate some initial traffic data for the dashboard
    global traffic_log, suspicious_events
    
    # Generate sample traffic if empty
    if not traffic_log:
        for _ in range(20):
            if random.random() < 0.8:  # 80% normal traffic
                traffic = generate_normal_traffic()
            else:  # 20% suspicious
                traffic = generate_suspicious_traffic()
                if traffic['classification'] == 'suspicious':
                    suspicious_events.append(traffic)
            traffic_log.append(traffic)
    
    # Calculate statistics for dashboard
    total_packets = len(traffic_log)
    suspicious_packets = len([t for t in traffic_log if t['classification'] == 'suspicious'])
    
    # Protocol distribution
    protocol_stats = defaultdict(int)
    for traffic in traffic_log[-100:]:  # Last 100 packets
        protocol_stats[traffic['protocol']] += 1
    
    # Top source IPs
    src_ip_stats = defaultdict(int)
    for traffic in traffic_log[-100:]:
        src_ip_stats[traffic['src_ip']] += 1
    
    # Recent suspicious events
    recent_suspicious = suspicious_events[-10:] if suspicious_events else []
    
    # Integration info
    integration_features = {
        'packet_capture': {
            'description': 'Live packet capture simulation with protocol analysis',
            'url': 'traffic_analysis.start_capture'
        },
        'forensics': {
            'description': 'Network forensics and incident analysis',
            'url': 'traffic_analysis.forensics'
        },
        'suspicious_activity': {
            'description': 'Suspicious behavior detection and analysis',
            'url': 'traffic_analysis.suspicious_activity'
        }
    }
    
    dashboard_data = {
        'total_packets': total_packets,
        'suspicious_packets': suspicious_packets,
        'protocol_stats': dict(protocol_stats),
        'src_ip_stats': dict(sorted(src_ip_stats.items(), key=lambda x: x[1], reverse=True)[:5]),
        'recent_suspicious': recent_suspicious,
        'integration_features': integration_features
    }
    
    return render_template('network/traffic_analysis.html', **dashboard_data)

@traffic_analysis_bp.route('/capture')
def start_capture():
    """Start simulated packet capture - integrated with traffic analysis"""
    global traffic_log, suspicious_events
    
    # Generate initial traffic burst for capture simulation
    for _ in range(50):
        if random.random() < 0.85:  # 85% normal traffic
            traffic = generate_normal_traffic()
        else:  # 15% suspicious
            traffic = generate_suspicious_traffic()
            if traffic['classification'] == 'suspicious':
                suspicious_events.append(traffic)
        
        traffic_log.append(traffic)
    
    # Keep only last 1000 packets for performance
    if len(traffic_log) > 1000:
        traffic_log = traffic_log[-1000:]
    
    # Prepare capture session data
    capture_session = {
        'session_id': f"capture_{int(time.time())}",
        'start_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'packets_captured': len(traffic_log),
        'suspicious_detected': len(suspicious_events),
        'interface': 'eth0 (simulated)',
        'filter': 'All packets',
        'integration_note': 'This packet capture is integrated with traffic analysis for comprehensive monitoring'
    }
    
    return render_template('network/packet_capture.html', 
                         capture_session=capture_session,
                         recent_packets=traffic_log[-20:] if traffic_log else [])

@traffic_analysis_bp.route('/api/live-traffic')
def get_live_traffic():
    """API endpoint for real-time traffic data"""
    # Generate new traffic
    new_packets = []
    for _ in range(random.randint(1, 5)):
        if random.random() < 0.9:
            packet = generate_normal_traffic()
        else:
            packet = generate_suspicious_traffic()
            if packet['classification'] == 'suspicious':
                suspicious_events.append(packet)
        
        traffic_log.append(packet)
        new_packets.append({
            'timestamp': packet['timestamp'].strftime('%H:%M:%S.%f')[:-3],
            'src_ip': packet['src_ip'],
            'dst_ip': packet['dst_ip'],
            'protocol': packet['protocol'],
            'src_port': packet['src_port'],
            'dst_port': packet['dst_port'],
            'size': packet['packet_size'],
            'flags': packet['flags'],
            'classification': packet['classification'],
            'payload': packet['payload_preview'][:50] + '...' if len(packet['payload_preview']) > 50 else packet['payload_preview']
        })
    
    return jsonify(new_packets)

@traffic_analysis_bp.route('/api/statistics')
def get_statistics():
    """Get traffic statistics for dashboard"""
    if not traffic_log:
        return jsonify({'error': 'No traffic data available'})
    
    total_packets = len(traffic_log)
    protocols = defaultdict(int)
    top_talkers = defaultdict(int)
    port_usage = defaultdict(int)
    suspicious_count = 0
    
    for packet in traffic_log[-100:]:  # Last 100 packets
        protocols[packet['protocol']] += 1
        top_talkers[packet['src_ip']] += 1
        port_usage[packet['dst_port']] += 1
        if packet['classification'] == 'suspicious':
            suspicious_count += 1
    
    return jsonify({
        'total_packets': total_packets,
        'suspicious_packets': suspicious_count,
        'protocols': dict(protocols),
        'top_talkers': dict(sorted(top_talkers.items(), key=lambda x: x[1], reverse=True)[:10]),
        'top_ports': dict(sorted(port_usage.items(), key=lambda x: x[1], reverse=True)[:10]),
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

@traffic_analysis_bp.route('/suspicious')
def suspicious_activity():
    """Show suspicious activity detection"""
    
    # Group suspicious events by type
    events_by_type = defaultdict(list)
    for event in suspicious_events[-50:]:  # Last 50 events
        attack_type = event.get('attack_type', 'unknown')
        events_by_type[attack_type].append(event)
    
    return render_template('network/suspicious_activity.html', 
                         events_by_type=dict(events_by_type),
                         total_events=len(suspicious_events))

@traffic_analysis_bp.route('/forensics')
def forensics():
    """Network forensics investigation interface"""
    
    # Create investigation scenarios
    scenarios = [
        {
            'id': 'data_breach',
            'title': 'Data Breach Investigation',
            'description': 'Suspicious data exfiltration detected from internal host',
            'timeline': '2024-08-01 14:30:00 - 15:45:00',
            'affected_hosts': ['192.168.1.150', '192.168.1.75'],
            'indicators': ['Large outbound transfers', 'Unusual destinations', 'Off-hours activity'],
            'severity': 'Critical'
        },
        {
            'id': 'malware_infection',
            'title': 'Malware C2 Communication',
            'description': 'Host showing signs of malware communication',
            'timeline': '2024-08-01 09:15:00 - Ongoing',
            'affected_hosts': ['192.168.1.75'],
            'indicators': ['Periodic beaconing', 'Unknown external IPs', 'Encrypted payloads'],
            'severity': 'High'
        },
        {
            'id': 'port_scan_attack',
            'title': 'Network Reconnaissance',
            'description': 'External host performing network scanning',
            'timeline': '2024-08-01 11:20:00 - 11:35:00',
            'affected_hosts': ['All internal hosts'],
            'indicators': ['Sequential port scanning', 'Service enumeration', 'Multiple targets'],
            'severity': 'Medium'
        }
    ]
    
    return render_template('network/forensics.html', scenarios=scenarios)

@traffic_analysis_bp.route('/forensics/<scenario_id>')
def forensics_scenario(scenario_id):
    """Detailed forensics investigation for specific scenario"""
    
    # Generate scenario-specific evidence
    evidence = generate_forensics_evidence(scenario_id)
    
    return render_template('network/forensics_detail.html', 
                         scenario_id=scenario_id,
                         evidence=evidence)

def generate_forensics_evidence(scenario_id):
    """Generate forensics evidence for investigation scenarios"""
    
    evidence_templates = {
        'data_breach': {
            'packets': [
                {
                    'time': '14:32:15.123',
                    'src': '192.168.1.150',
                    'dst': '198.51.100.50',
                    'protocol': 'HTTPS',
                    'size': '8192',
                    'info': 'Large POST request to external server'
                },
                {
                    'time': '14:32:16.891',
                    'src': '192.168.1.150', 
                    'dst': '198.51.100.50',
                    'protocol': 'HTTPS',
                    'size': '16384',
                    'info': 'Continued data upload'
                }
            ],
            'timeline': [
                {'time': '14:30:00', 'event': 'User login detected', 'severity': 'info'},
                {'time': '14:32:15', 'event': 'Large data transfer initiated', 'severity': 'warning'},
                {'time': '14:35:22', 'event': 'Multiple file access attempts', 'severity': 'critical'},
                {'time': '15:45:00', 'event': 'User logout', 'severity': 'info'}
            ],
            'artifacts': [
                {'type': 'Log Entry', 'source': 'Web Server', 'content': 'POST /api/download/database.sql'},
                {'type': 'File Access', 'source': 'File Server', 'content': 'customer_data.xlsx accessed'},
                {'type': 'Network Flow', 'source': 'Firewall', 'content': '50MB transferred to external IP'}
            ]
        },
        'malware_infection': {
            'packets': [
                {
                    'time': '09:15:30.456',
                    'src': '192.168.1.75',
                    'dst': '185.92.220.35',
                    'protocol': 'TCP:8080',
                    'size': '256',
                    'info': 'Periodic beacon to C2 server'
                }
            ],
            'timeline': [
                {'time': '09:15:00', 'event': 'Suspicious executable launched', 'severity': 'warning'},
                {'time': '09:15:30', 'event': 'C2 communication started', 'severity': 'critical'},
                {'time': '09:20:15', 'event': 'Registry modifications detected', 'severity': 'warning'}
            ],
            'artifacts': [
                {'type': 'Process', 'source': 'EDR', 'content': 'svchost.exe spawning unusual child processes'},
                {'type': 'Registry', 'source': 'Host', 'content': 'Persistence key created in HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Run'},
                {'type': 'DNS Query', 'source': 'DNS Logs', 'content': 'Query to known malicious domain evil-c2.com'}
            ]
        }
    }
    
    return evidence_templates.get(scenario_id, {'packets': [], 'timeline': [], 'artifacts': []})

@traffic_analysis_bp.route('/clear-data')
def clear_data():
    """Clear traffic analysis data"""
    global traffic_log, suspicious_events
    traffic_log = []
    suspicious_events = []
    
    return jsonify({'success': True, 'message': 'Traffic data cleared'})
