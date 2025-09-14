"""
Firewall Rule Simulation Module
Interactive firewall configuration and testing
"""
from flask import Blueprint, render_template, request, jsonify
import ipaddress
import re
from datetime import datetime

firewall_sim_bp = Blueprint('firewall_sim', __name__)

# In-memory firewall rules storage
firewall_rules = [
    {
        'id': 1,
        'name': 'Allow HTTP',
        'action': 'ALLOW',
        'source_ip': 'any',
        'dest_ip': '192.168.1.100',
        'port_range': '80',
        'protocol': 'TCP',
        'priority': 1,
        'enabled': True,
        'description': 'Allow HTTP traffic to web server'
    },
    {
        'id': 2,
        'name': 'Allow HTTPS',
        'action': 'ALLOW',
        'source_ip': 'any',
        'dest_ip': '192.168.1.100',
        'port_range': '443',
        'protocol': 'TCP',
        'priority': 2,
        'enabled': True,
        'description': 'Allow HTTPS traffic to web server'
    },
    {
        'id': 3,
        'name': 'Block Telnet',
        'action': 'DENY',
        'source_ip': 'any',
        'dest_ip': 'any',
        'port_range': '23',
        'protocol': 'TCP',
        'priority': 10,
        'enabled': True,
        'description': 'Block insecure Telnet protocol'
    }
]

firewall_logs = []
next_rule_id = 4

def validate_ip(ip_str):
    """Validate IP address or network"""
    if ip_str.lower() in ['any', 'all', '*']:
        return True
    
    try:
        ipaddress.ip_address(ip_str)
        return True
    except ValueError:
        try:
            ipaddress.ip_network(ip_str, strict=False)
            return True
        except ValueError:
            return False

def validate_port_range(port_str):
    """Validate port range specification"""
    if port_str.lower() in ['any', 'all', '*']:
        return True
    
    try:
        if '-' in port_str:
            start, end = map(int, port_str.split('-'))
            return 1 <= start <= end <= 65535
        else:
            port = int(port_str)
            return 1 <= port <= 65535
    except ValueError:
        return False

def ip_matches(packet_ip, rule_ip):
    """Check if packet IP matches rule IP specification"""
    if rule_ip.lower() in ['any', 'all', '*']:
        return True
    
    try:
        if '/' in rule_ip:  # CIDR notation
            network = ipaddress.ip_network(rule_ip, strict=False)
            return ipaddress.ip_address(packet_ip) in network
        else:
            return packet_ip == rule_ip
    except ValueError:
        return False

def port_matches(packet_port, rule_port):
    """Check if packet port matches rule port specification"""
    if rule_port.lower() in ['any', 'all', '*']:
        return True
    
    try:
        if '-' in rule_port:
            start, end = map(int, rule_port.split('-'))
            return start <= packet_port <= end
        else:
            return packet_port == int(rule_port)
    except ValueError:
        return False

def process_packet(packet):
    """Process packet through firewall rules"""
    matching_rule = None
    decision = 'DENY'  # Default deny
    
    # Sort rules by priority
    sorted_rules = sorted([r for r in firewall_rules if r['enabled']], 
                         key=lambda x: x['priority'])
    
    for rule in sorted_rules:
        if (rule['protocol'].upper() == packet['protocol'].upper() and
            ip_matches(packet['src_ip'], rule['source_ip']) and
            ip_matches(packet['dst_ip'], rule['dest_ip']) and
            port_matches(packet['dst_port'], rule['port_range'])):
            
            matching_rule = rule
            decision = rule['action']
            break
    
    # Log the decision
    log_entry = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'src_ip': packet['src_ip'],
        'dst_ip': packet['dst_ip'],
        'dst_port': packet['dst_port'],
        'protocol': packet['protocol'],
        'action': decision,
        'rule_name': matching_rule['name'] if matching_rule else 'Default Policy',
        'rule_id': matching_rule['id'] if matching_rule else None
    }
    
    firewall_logs.append(log_entry)
    
    return {
        'decision': decision,
        'matching_rule': matching_rule,
        'log_entry': log_entry,
        'reasoning': generate_reasoning(packet, matching_rule, decision)
    }

def generate_reasoning(packet, matching_rule, decision):
    """Generate human-readable reasoning for firewall decision"""
    if matching_rule:
        return f"Packet matched rule '{matching_rule['name']}' (Priority {matching_rule['priority']}) - {decision}"
    else:
        return f"No matching rules found - Default policy applied: {decision}"

@firewall_sim_bp.route('/')
def index():
    """Firewall management interface"""
    return render_template('network/firewall_sim.html', rules=firewall_rules)

@firewall_sim_bp.route('/api/rules', methods=['GET'])
def get_rules():
    """Get all firewall rules"""
    return jsonify(firewall_rules)

@firewall_sim_bp.route('/api/rules', methods=['POST'])
def add_rule():
    """Add new firewall rule"""
    global next_rule_id
    
    data = request.get_json()
    
    # Validate input
    if not validate_ip(data.get('source_ip', '')):
        return jsonify({'error': 'Invalid source IP address'}), 400
    
    if not validate_ip(data.get('dest_ip', '')):
        return jsonify({'error': 'Invalid destination IP address'}), 400
    
    if not validate_port_range(data.get('port_range', '')):
        return jsonify({'error': 'Invalid port range'}), 400
    
    new_rule = {
        'id': next_rule_id,
        'name': data.get('name', f'Rule {next_rule_id}'),
        'action': data.get('action', 'DENY'),
        'source_ip': data.get('source_ip', 'any'),
        'dest_ip': data.get('dest_ip', 'any'),
        'port_range': data.get('port_range', 'any'),
        'protocol': data.get('protocol', 'TCP'),
        'priority': data.get('priority', len(firewall_rules) + 1),
        'enabled': data.get('enabled', True),
        'description': data.get('description', '')
    }
    
    firewall_rules.append(new_rule)
    next_rule_id += 1
    
    return jsonify(new_rule), 201

@firewall_sim_bp.route('/api/rules/<int:rule_id>', methods=['PUT'])
def update_rule(rule_id):
    """Update existing firewall rule"""
    data = request.get_json()
    
    rule = next((r for r in firewall_rules if r['id'] == rule_id), None)
    if not rule:
        return jsonify({'error': 'Rule not found'}), 404
    
    # Update rule fields
    for field in ['name', 'action', 'source_ip', 'dest_ip', 'port_range', 
                  'protocol', 'priority', 'enabled', 'description']:
        if field in data:
            rule[field] = data[field]
    
    return jsonify(rule)

@firewall_sim_bp.route('/api/rules/<int:rule_id>', methods=['DELETE'])
def delete_rule(rule_id):
    """Delete firewall rule"""
    global firewall_rules
    
    firewall_rules = [r for r in firewall_rules if r['id'] != rule_id]
    return jsonify({'success': True})

@firewall_sim_bp.route('/test')
def test_interface():
    """Firewall testing interface"""
    return render_template('network/firewall_test.html')

@firewall_sim_bp.route('/api/test', methods=['POST'])
def test_packet():
    """Test packet against firewall rules"""
    data = request.get_json()
    
    packet = {
        'src_ip': data.get('src_ip', ''),
        'dst_ip': data.get('dst_ip', ''),
        'dst_port': int(data.get('dst_port', 80)),
        'protocol': data.get('protocol', 'TCP')
    }
    
    # Validate packet data
    if not validate_ip(packet['src_ip']) or not validate_ip(packet['dst_ip']):
        return jsonify({'error': 'Invalid IP addresses'}), 400
    
    if not (1 <= packet['dst_port'] <= 65535):
        return jsonify({'error': 'Invalid port number'}), 400
    
    result = process_packet(packet)
    
    return jsonify({
        'packet': packet,
        'decision': result['decision'],
        'matching_rule': result['matching_rule'],
        'reasoning': result['reasoning'],
        'timestamp': result['log_entry']['timestamp']
    })

@firewall_sim_bp.route('/logs')
def view_logs():
    """View firewall logs"""
    return render_template('network/firewall_logs.html', logs=firewall_logs[-100:])

@firewall_sim_bp.route('/api/logs')
def get_logs():
    """Get firewall logs API"""
    return jsonify(firewall_logs[-100:])  # Last 100 log entries

@firewall_sim_bp.route('/scenarios')
def scenarios():
    """Common firewall scenarios"""
    
    scenarios = [
        {
            'name': 'Web Server Protection',
            'description': 'Configure firewall for a public web server',
            'requirements': [
                'Allow HTTP (port 80) from anywhere',
                'Allow HTTPS (port 443) from anywhere', 
                'Allow SSH (port 22) from management network only',
                'Block all other inbound traffic'
            ],
            'rules': [
                {'action': 'ALLOW', 'src': 'any', 'dst': 'web-server', 'port': '80', 'protocol': 'TCP'},
                {'action': 'ALLOW', 'src': 'any', 'dst': 'web-server', 'port': '443', 'protocol': 'TCP'},
                {'action': 'ALLOW', 'src': '10.0.1.0/24', 'dst': 'web-server', 'port': '22', 'protocol': 'TCP'},
                {'action': 'DENY', 'src': 'any', 'dst': 'web-server', 'port': 'any', 'protocol': 'any'}
            ]
        },
        {
            'name': 'DMZ Configuration',
            'description': 'Isolate DMZ servers from internal network',
            'requirements': [
                'DMZ servers can access internet',
                'Internal users can access DMZ services',
                'DMZ servers cannot access internal network',
                'Internet cannot directly access internal network'
            ],
            'rules': [
                {'action': 'ALLOW', 'src': '192.168.100.0/24', 'dst': 'any', 'port': '80,443', 'protocol': 'TCP'},
                {'action': 'ALLOW', 'src': '10.0.0.0/24', 'dst': '192.168.100.0/24', 'port': '80,443', 'protocol': 'TCP'},
                {'action': 'DENY', 'src': '192.168.100.0/24', 'dst': '10.0.0.0/24', 'port': 'any', 'protocol': 'any'},
                {'action': 'DENY', 'src': 'any', 'dst': '10.0.0.0/24', 'port': 'any', 'protocol': 'any'}
            ]
        },
        {
            'name': 'VPN Access Control',
            'description': 'Control remote access through VPN',
            'requirements': [
                'Allow VPN connections on port 1194',
                'VPN users can access internal servers',
                'Limit VPN users to specific services only',
                'Log all VPN user activities'
            ],
            'rules': [
                {'action': 'ALLOW', 'src': 'any', 'dst': 'vpn-server', 'port': '1194', 'protocol': 'UDP'},
                {'action': 'ALLOW', 'src': '10.8.0.0/24', 'dst': '10.0.0.0/24', 'port': '80,443,22', 'protocol': 'TCP'},
                {'action': 'LOG', 'src': '10.8.0.0/24', 'dst': 'any', 'port': 'any', 'protocol': 'any'},
                {'action': 'DENY', 'src': '10.8.0.0/24', 'dst': 'any', 'port': 'any', 'protocol': 'any'}
            ]
        }
    ]
    
    return render_template('network/firewall_scenarios.html', scenarios=scenarios)

@firewall_sim_bp.route('/api/clear-logs')
def clear_logs():
    """Clear firewall logs"""
    global firewall_logs
    firewall_logs = []
    return jsonify({'success': True})

@firewall_sim_bp.route('/api/analyze-rules')
def analyze_rules():
    """Analyze firewall rules for conflicts and optimization"""
    
    analysis = {
        'total_rules': len(firewall_rules),
        'enabled_rules': len([r for r in firewall_rules if r['enabled']]),
        'disabled_rules': len([r for r in firewall_rules if not r['enabled']]),
        'conflicts': [],
        'redundancies': [],
        'optimization_suggestions': []
    }
    
    # Check for rule conflicts
    for i, rule1 in enumerate(firewall_rules):
        for j, rule2 in enumerate(firewall_rules[i+1:], i+1):
            if (rule1['enabled'] and rule2['enabled'] and 
                rule1['action'] != rule2['action'] and
                rules_overlap(rule1, rule2)):
                
                analysis['conflicts'].append({
                    'rule1': rule1,
                    'rule2': rule2,
                    'issue': 'Conflicting actions for overlapping traffic'
                })
    
    # Check for redundant rules
    for i, rule1 in enumerate(firewall_rules):
        for j, rule2 in enumerate(firewall_rules[i+1:], i+1):
            if (rule1['enabled'] and rule2['enabled'] and
                rules_identical(rule1, rule2)):
                
                analysis['redundancies'].append({
                    'rule1': rule1,
                    'rule2': rule2,
                    'issue': 'Identical rules with different priorities'
                })
    
    # Generate optimization suggestions
    if analysis['conflicts']:
        analysis['optimization_suggestions'].append(
            'Resolve rule conflicts by adjusting priorities or modifying conditions'
        )
    
    if analysis['redundancies']:
        analysis['optimization_suggestions'].append(
            'Remove redundant rules to improve performance'
        )
    
    if len(firewall_rules) > 20:
        analysis['optimization_suggestions'].append(
            'Consider consolidating rules to reduce rule set complexity'
        )
    
    return jsonify(analysis)

def rules_overlap(rule1, rule2):
    """Check if two firewall rules have overlapping conditions"""
    # Simplified overlap detection - in reality this would be more complex
    return (rule1['protocol'] == rule2['protocol'] and
            rule1['source_ip'] == rule2['source_ip'] and
            rule1['dest_ip'] == rule2['dest_ip'] and
            rule1['port_range'] == rule2['port_range'])

def rules_identical(rule1, rule2):
    """Check if two firewall rules are functionally identical"""
    return (rule1['action'] == rule2['action'] and
            rule1['protocol'] == rule2['protocol'] and
            rule1['source_ip'] == rule2['source_ip'] and
            rule1['dest_ip'] == rule2['dest_ip'] and
            rule1['port_range'] == rule2['port_range'])
