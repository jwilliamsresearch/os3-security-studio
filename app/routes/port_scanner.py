"""
Port Scanner Simulation Module
Demonstrates network reconnaissance techniques without actual network access
"""
from flask import Blueprint, render_template, request, jsonify
import time
import random
import re
from datetime import datetime

port_scanner_bp = Blueprint('port_scanner', __name__)

# Mock network configuration
COMMON_PORTS = {
    22: {'service': 'SSH', 'banner': 'OpenSSH 8.0', 'status': 'open', 'risk': 'medium'},
    23: {'service': 'Telnet', 'banner': 'Linux telnetd', 'status': 'closed', 'risk': 'high'},
    25: {'service': 'SMTP', 'banner': 'Postfix smtpd', 'status': 'filtered', 'risk': 'low'},
    53: {'service': 'DNS', 'banner': 'ISC BIND 9.16', 'status': 'open', 'risk': 'low'},
    80: {'service': 'HTTP', 'banner': 'Apache/2.4.41', 'status': 'open', 'risk': 'medium'},
    135: {'service': 'RPC', 'banner': 'Microsoft RPC', 'status': 'open', 'risk': 'high'},
    443: {'service': 'HTTPS', 'banner': 'nginx/1.18.0', 'status': 'open', 'risk': 'low'},
    993: {'service': 'IMAPS', 'banner': 'Dovecot ready', 'status': 'open', 'risk': 'low'},
    3389: {'service': 'RDP', 'banner': 'Microsoft Terminal Services', 'status': 'filtered', 'risk': 'high'},
    8080: {'service': 'HTTP-Alt', 'banner': 'Jetty 9.4.z', 'status': 'open', 'risk': 'medium'},
    5432: {'service': 'PostgreSQL', 'banner': 'PostgreSQL 13.0', 'status': 'closed', 'risk': 'high'},
    3306: {'service': 'MySQL', 'banner': 'MySQL 8.0.25', 'status': 'filtered', 'risk': 'high'},
    21: {'service': 'FTP', 'banner': 'vsftpd 3.0.3', 'status': 'open', 'risk': 'medium'},
    445: {'service': 'SMB', 'banner': 'Samba 4.13.13', 'status': 'open', 'risk': 'high'},
    110: {'service': 'POP3', 'banner': 'Dovecot ready', 'status': 'closed', 'risk': 'medium'}
}

def validate_ip(ip):
    """Validate IP address format"""
    pattern = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    return re.match(pattern, ip) is not None

def simulate_scan_delay(scan_type):
    """Simulate realistic scan timing"""
    delays = {
        'tcp_connect': random.uniform(0.1, 0.3),
        'syn_stealth': random.uniform(0.05, 0.15),
        'fin_stealth': random.uniform(0.03, 0.12),
        'null_stealth': random.uniform(0.03, 0.12),
        'xmas_stealth': random.uniform(0.03, 0.12),
        'udp': random.uniform(0.2, 0.5)
    }
    return delays.get(scan_type, 0.1)

def get_port_status(port, scan_type):
    """Simulate port scanning with different techniques"""
    base_info = COMMON_PORTS.get(port, {
        'service': 'Unknown',
        'banner': '',
        'status': random.choice(['closed', 'filtered']),
        'risk': 'unknown'
    })
    
    # Modify status based on scan type
    if scan_type == 'udp' and base_info['status'] == 'open':
        # UDP scans are less reliable
        if random.random() < 0.3:
            base_info['status'] = 'open|filtered'
    elif scan_type in ['syn_stealth', 'fin_stealth', 'null_stealth', 'xmas_stealth']:
        # Stealth scans might show different results for filtered ports
        if base_info['status'] == 'filtered' and random.random() < 0.4:
            base_info['status'] = 'filtered'
        # Advanced stealth scans are harder to detect but less reliable
        if scan_type in ['fin_stealth', 'null_stealth', 'xmas_stealth']:
            if base_info['status'] == 'open' and random.random() < 0.15:
                base_info['status'] = 'open|filtered'  # Less reliable detection
    
    return base_info

@port_scanner_bp.route('/')
def index():
    """Main port scanner interface"""
    return render_template('network/port_scanning.html')

@port_scanner_bp.route('/scan', methods=['POST'])
def perform_scan():
    """AJAX endpoint for port scanning simulation"""
    data = request.get_json()
    
    target_ip = data.get('target_ip', '').strip()
    scan_type = data.get('scan_type', 'tcp_connect')
    port_range = data.get('port_range', 'common')
    
    # Validate IP address
    if not validate_ip(target_ip):
        return jsonify({'error': 'Invalid IP address format'}), 400
    
    # Determine ports to scan
    if port_range == 'common':
        ports_to_scan = list(COMMON_PORTS.keys())
    elif port_range == 'all':
        ports_to_scan = list(range(1, 1001))  # Simulate first 1000 ports
    else:
        # Parse custom range (e.g., "80-90" or "80,443,8080")
        try:
            if '-' in port_range:
                start, end = map(int, port_range.split('-'))
                ports_to_scan = list(range(start, min(end + 1, 65536)))
            elif ',' in port_range:
                ports_to_scan = [int(p.strip()) for p in port_range.split(',')]
            else:
                ports_to_scan = [int(port_range)]
        except ValueError:
            return jsonify({'error': 'Invalid port range format'}), 400
    
    # Limit scan size for demo
    if len(ports_to_scan) > 100:
        ports_to_scan = ports_to_scan[:100]
    
    scan_results = []
    scan_start_time = datetime.now()
    
    for port in ports_to_scan:
        # Simulate scan delay
        time.sleep(simulate_scan_delay(scan_type))
        
        port_info = get_port_status(port, scan_type)
        
        result = {
            'port': port,
            'status': port_info['status'],
            'service': port_info['service'],
            'banner': port_info['banner'] if port_info['status'] == 'open' else '',
            'risk': port_info['risk'],
            'scan_time': simulate_scan_delay(scan_type)
        }
        
        scan_results.append(result)
    
    scan_duration = (datetime.now() - scan_start_time).total_seconds()
    
    # Generate scan summary
    open_ports = [r for r in scan_results if r['status'] == 'open']
    closed_ports = [r for r in scan_results if r['status'] == 'closed']
    filtered_ports = [r for r in scan_results if 'filtered' in r['status']]
    
    summary = {
        'target_ip': target_ip,
        'scan_type': scan_type,
        'total_ports': len(scan_results),
        'open_ports': len(open_ports),
        'closed_ports': len(closed_ports),
        'filtered_ports': len(filtered_ports),
        'scan_duration': round(scan_duration, 2),
        'timestamp': scan_start_time.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    return jsonify({
        'results': scan_results,
        'summary': summary,
        'open_services': open_ports
    })

@port_scanner_bp.route('/stealth')
def stealth_techniques():
    """Demonstrate stealth scanning techniques"""
    techniques = [
        {
            'name': 'SYN Stealth Scan',
            'description': 'Sends SYN packets without completing TCP handshake',
            'stealth_level': 85,
            'stealth_color': 'success',
            'speed': 'Fast',
            'speed_color': 'success',
            'reliability': 'High',
            'reliability_color': 'success'
        },
        {
            'name': 'FIN Scan',
            'description': 'Sends FIN packets to closed ports',
            'stealth_level': 75,
            'stealth_color': 'warning',
            'speed': 'Medium',
            'speed_color': 'warning',
            'reliability': 'Medium',
            'reliability_color': 'warning'
        },
        {
            'name': 'Idle/Zombie Scan',
            'description': 'Uses third-party host to perform scan',
            'stealth_level': 95,
            'stealth_color': 'success',
            'speed': 'Slow',
            'speed_color': 'danger',
            'reliability': 'High',
            'reliability_color': 'success'
        },
        {
            'name': 'Fragmented Packets',
            'description': 'Splits scan packets into fragments',
            'stealth_level': 70,
            'stealth_color': 'warning',
            'speed': 'Slow',
            'speed_color': 'danger',
            'reliability': 'Medium',
            'reliability_color': 'warning'
        }
    ]
    
    evasion_methods = [
        {'name': 'Decoy Scans', 'description': 'Use multiple fake IP addresses to mask real scanner'},
        {'name': 'Source Port Spoofing', 'description': 'Use common ports like 53 (DNS) or 80 (HTTP) as source'},
        {'name': 'Timing Delays', 'description': 'Spread scan over time to avoid rate-based detection'},
        {'name': 'Packet Fragmentation', 'description': 'Split packets to evade signature-based detection'},
        {'name': 'Proxy Chains', 'description': 'Route traffic through multiple intermediate hosts'},
        {'name': 'Random Target Order', 'description': 'Scan ports in random sequence to avoid patterns'}
    ]
    
    # Simulate current scan information
    scan_info = {
        'target': '192.168.1.100',
        'technique': 'SYN Stealth Scan',
        'timing': 'T3 (Normal)',
        'fragmentation': 'Enabled',
        'source_port': '53 (DNS)',
        'decoys': ['192.168.1.50', '192.168.1.75', '192.168.1.200'],
        'estimated_time': '4-8 minutes'
    }
    
    # Simulate scan progress data
    scan_progress = 45
    ports_scanned = 567
    open_ports = 12
    filtered_ports = 23
    
    # Found ports simulation
    found_ports = [
        {'port': 22, 'protocol': 'tcp', 'service': 'ssh'},
        {'port': 80, 'protocol': 'tcp', 'service': 'http'},
        {'port': 443, 'protocol': 'tcp', 'service': 'https'},
        {'port': 3389, 'protocol': 'tcp', 'service': 'rdp'}
    ]
    
    return render_template('network/stealth_scanning.html', 
                         techniques=techniques,
                         evasion_methods=evasion_methods,
                         scan_info=scan_info,
                         scan_progress=scan_progress,
                         ports_scanned=ports_scanned,
                         open_ports=open_ports,
                         filtered_ports=filtered_ports,
                         found_ports=found_ports)

@port_scanner_bp.route('/stealth/run', methods=['POST'])
def run_stealth_scan():
    """Execute stealth scan with selected parameters"""
    data = request.get_json()
    
    target = data.get('target', '192.168.1.100')
    technique = data.get('technique', 'SYN Stealth Scan')
    timing = data.get('timing', 'T3')
    ports = data.get('ports', '1-1000')
    
    # Simulate scan execution
    time.sleep(1)  # Simulate scan time
    
    # Generate scan results based on technique
    results = []
    port_range = [22, 80, 135, 139, 443, 445, 3389, 5900]  # Common ports
    
    stealth_effectiveness = {
        'SYN Stealth Scan': 0.85,
        'FIN Scan': 0.75,
        'Idle/Zombie Scan': 0.95,
        'Fragmented Packets': 0.70
    }
    
    effectiveness = stealth_effectiveness.get(technique, 0.80)
    
    for port in port_range:
        # Simulate port status
        if random.random() < 0.3:  # 30% chance port is open
            status = 'open'
            service = get_service_name(port)
        elif random.random() < effectiveness:  # Stealth effectiveness
            status = 'filtered'
            service = 'unknown'
        else:
            status = 'closed'
            service = ''
        
        results.append({
            'port': port,
            'status': status,
            'service': service,
            'detected': random.random() > effectiveness
        })
    
    scan_summary = {
        'target': target,
        'technique': technique,
        'total_ports': len(results),
        'open_ports': len([r for r in results if r['status'] == 'open']),
        'detected': any(r['detected'] for r in results),
        'stealth_score': int(effectiveness * 100)
    }
    
    return jsonify({
        'success': True,
        'results': results,
        'summary': scan_summary
    })

def get_service_name(port):
    """Get common service name for port"""
    services = {
        22: 'ssh',
        80: 'http',
        135: 'msrpc',
        139: 'netbios-ssn',
        443: 'https',
        445: 'microsoft-ds',
        3389: 'rdp',
        5900: 'vnc'
    }
    return services.get(port, 'unknown')

@port_scanner_bp.route('/defense')
def defense_measures():
    """Show defensive strategies against port scanning"""
    detection_methods = [
        {
            'method': 'Intrusion Detection Systems (IDS)',
            'description': 'Monitor network traffic for scanning patterns',
            'effectiveness': 'High',
            'examples': ['Snort', 'Suricata', 'OSSEC']
        },
        {
            'method': 'Firewall Logging',
            'description': 'Log connection attempts to closed ports',
            'effectiveness': 'Medium',
            'examples': ['iptables', 'pfSense', 'Windows Firewall']
        },
        {
            'method': 'Port Knocking',
            'description': 'Require sequence of connection attempts to open ports',
            'effectiveness': 'High',
            'examples': ['knockd', 'fwknop']
        },
        {
            'method': 'Honeypots',
            'description': 'Deploy fake services to detect and analyze attacks',
            'effectiveness': 'Very High',
            'examples': ['Kippo', 'Cowrie', 'Dionaea']
        }
    ]
    
    prevention_strategies = [
        'Close unnecessary services and ports',
        'Use non-standard ports for services',
        'Implement rate limiting',
        'Deploy network segmentation',
        'Regular security audits',
        'Keep systems patched and updated',
        'Use VPNs for remote access',
        'Implement strong access controls'
    ]
    
    # Simulate real-time monitoring statistics
    monitoring_stats = {
        'connections_per_second': round(random.uniform(10.0, 25.0), 1),
        'unique_sources': random.randint(5, 15),
        'blocked_attempts': random.randint(1000, 2500),
        'alerts_triggered': random.randint(15, 40),
        'false_positives': random.randint(1, 8)
    }
    
    # Simulate recent scan attempts for interactive demo
    recent_scans = []
    for i in range(5):
        recent_scans.append({
            'timestamp': datetime.now().strftime('%H:%M:%S'),
            'source_ip': f"192.168.{random.randint(1,10)}.{random.randint(10,200)}",
            'ports_scanned': random.randint(50, 500),
            'scan_type': random.choice(['TCP Connect', 'SYN Stealth', 'UDP Scan', 'FIN Scan']),
            'blocked': random.choice([True, False]),
            'risk_level': random.choice(['Low', 'Medium', 'High', 'Critical'])
        })
    
    # Prevention methods data
    prevention_methods = {
        'rate_limiting': [
            {
                'name': 'Connection Rate Limit',
                'value': '10 connections/sec per IP',
                'description': 'Limits rapid connection attempts from single source',
                'color': 'warning'
            },
            {
                'name': 'Port Scan Detection',
                'value': '5 ports/sec threshold',
                'description': 'Triggers alerts when rapid port scanning detected',
                'color': 'danger'
            },
            {
                'name': 'Blacklist Duration',
                'value': '24 hours',
                'description': 'How long IPs remain blocked after detection',
                'color': 'info'
            }
        ],
        'hardening': [
            {
                'name': 'SSH',
                'default_port': '22',
                'hardened_port': '2222',
                'status': 'Secured',
                'status_color': 'success'
            },
            {
                'name': 'HTTP',
                'default_port': '80',
                'hardened_port': '8080',
                'status': 'Redirected',
                'status_color': 'warning'
            },
            {
                'name': 'FTP',
                'default_port': '21',
                'hardened_port': 'Disabled',
                'status': 'Disabled',
                'status_color': 'danger'
            },
            {
                'name': 'Telnet',
                'default_port': '23',
                'hardened_port': 'Disabled',
                'status': 'Disabled',
                'status_color': 'danger'
            }
        ]
    }
    
    return render_template('network/port_scan_defense.html',
                         detection_methods=detection_methods,
                         prevention_strategies=prevention_strategies,
                         monitoring_stats=monitoring_stats,
                         prevention_methods=prevention_methods,
                         recent_scans=recent_scans,
                         defense_stats={
                             'protection_level': random.randint(80, 95),
                             'fast_scan_detection': random.randint(90, 99),
                             'stealth_scan_detection': random.randint(70, 85),
                             'distributed_scan_detection': random.randint(55, 75)
                         })

# Add real-time monitoring endpoint
@port_scanner_bp.route('/defense/monitor')
def defense_monitor():
    """Real-time monitoring data for defense dashboard"""
    return jsonify({
        'timestamp': datetime.now().strftime('%H:%M:%S'),
        'connections_per_second': round(random.uniform(8.0, 30.0), 1),
        'unique_sources': random.randint(3, 20),
        'blocked_attempts': random.randint(800, 3000),
        'alerts_triggered': random.randint(10, 50),
        'recent_block': {
            'ip': f"192.168.{random.randint(1,10)}.{random.randint(10,200)}",
            'reason': random.choice(['Port scan detected', 'Rate limit exceeded', 'Suspicious pattern', 'Blacklisted IP']),
            'ports_attempted': random.randint(20, 200)
        }
    })
