"""
Network Protocols Security Module
Demonstrates HTTP vs HTTPS transmission security differences
"""
from flask import Blueprint, render_template, request, session, jsonify, flash, redirect, url_for
import base64
import json
import datetime
import secrets
from collections import defaultdict

network_protocols_bp = Blueprint('network_protocols', __name__)

# Simulated intercepted traffic storage
intercepted_traffic = []

@network_protocols_bp.route('/')
def index():
    """Main protocol security demonstration page"""
    return render_template('network/protocol_security.html')

@network_protocols_bp.route('/insecure', methods=['GET', 'POST'])
def insecure():
    """Simulate HTTP login - capture and log all data"""
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        print(f"DEBUG: Form submitted - Username: {username}, Password: {password}")
        
        # Simulate intercepting HTTP traffic
        traffic_data = {
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'method': 'POST',
            'url': '/protocol-security/insecure',
            'headers': dict(request.headers),
            'form_data': {
                'username': username,
                'password': password
            },
            'user_agent': request.headers.get('User-Agent', ''),
            'source_ip': request.remote_addr,
            'protocol': 'HTTP/1.1',
            'encrypted': False
        }
        
        # Store in global list for demonstration
        global intercepted_traffic
        intercepted_traffic.append(traffic_data)
        print(f"DEBUG: Added to global list. Total global: {len(intercepted_traffic)}")
        
        # Store in session - use minimal data to avoid cookie size limits
        if 'intercepted_data' not in session:
            session['intercepted_data'] = []
        
        # Store only essential data in session to avoid cookie size limits
        session_data = {
            'timestamp': traffic_data['timestamp'],
            'method': 'POST',
            'url': '/protocol-security/insecure',
            'form_data': {
                'username': username,
                'password': password
            },
            'user_agent': request.headers.get('User-Agent', '')[:50] + '...' if len(request.headers.get('User-Agent', '')) > 50 else request.headers.get('User-Agent', ''),
            'source_ip': request.remote_addr,
            'protocol': 'HTTP/1.1',
            'encrypted': False
        }
        
        current_data = session['intercepted_data']
        current_data.append(session_data)
        
        # Limit session data to last 10 entries to prevent cookie overflow
        if len(current_data) > 10:
            current_data = current_data[-10:]
        
        session['intercepted_data'] = current_data
        session.permanent = True  # Make session persistent
        print(f"DEBUG: Added to session. Total session: {len(session['intercepted_data'])}")
        
        return render_template('network/protocol_result.html', 
                             traffic_data=traffic_data,
                             security_level='insecure')
    
    return render_template('network/protocol_security.html')

@network_protocols_bp.route('/secure', methods=['GET', 'POST'])
def secure():
    """Simulate HTTPS login - show encrypted payload"""
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        # Simulate HTTPS encryption
        original_data = json.dumps({
            'username': username,
            'password': password
        })
        
        # Simulate encrypted payload (base64 for demo)
        encrypted_payload = base64.b64encode(original_data.encode()).decode()
        
        # Simulate SSL/TLS information
        ssl_info = {
            'protocol': 'TLS 1.3',
            'cipher_suite': 'TLS_AES_256_GCM_SHA384',
            'certificate': {
                'issuer': 'Example University CA',
                'subject': 'cyberlab.excample.ac.uk',
                'valid_from': '2024-01-01',
                'valid_to': '2025-12-31',
                'fingerprint': 'SHA256:1234567890ABCDEF...'
            },
            'key_exchange': 'ECDHE (X25519)',
            'authentication': 'RSA-PSS',
            'bulk_encryption': 'AES-256-GCM',
            'mac': 'AEAD'
        }
        
        traffic_data = {
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'method': 'POST',
            'url': '/protocol-security/secure',
            'encrypted_payload': encrypted_payload,
            'ssl_info': ssl_info,
            'protocol': 'HTTPS/1.1',
            'encrypted': True,
            'session_id': secrets.token_hex(16)
        }
        
        return render_template('network/protocol_result.html', 
                             traffic_data=traffic_data,
                             security_level='secure')
    
    return render_template('network/protocol_security.html')

@network_protocols_bp.route('/intercepted')
def intercepted():
    """Show all captured HTTP traffic"""
    session_data = session.get('intercepted_data', [])
    
    # Use session data as primary source (survives app restarts)
    # Global data is secondary (gets cleared on restart)
    global intercepted_traffic
    all_data = session_data if session_data else intercepted_traffic
    
    # Calculate unique usernames
    unique_usernames = set()
    for traffic in all_data:
        if 'form_data' in traffic and 'username' in traffic['form_data']:
            unique_usernames.add(traffic['form_data']['username'])
    
    return render_template('network/intercepted_traffic.html', 
                         intercepted_traffic=all_data,
                         total_intercepted=len(all_data),
                         unique_usernames=len(unique_usernames))

@network_protocols_bp.route('/test-add-traffic')
def test_add_traffic():
    """Add test traffic data for debugging"""
    test_data = {
        'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'method': 'POST',
        'url': '/protocol-security/insecure',
        'headers': {'User-Agent': 'Test Browser', 'Host': 'localhost'},
        'form_data': {
            'username': 'test_user',
            'password': 'test_password123'
        },
        'user_agent': 'Test Browser',
        'source_ip': '127.0.0.1',
        'protocol': 'HTTP/1.1',
        'encrypted': False
    }
    
    # Add to global list
    global intercepted_traffic
    intercepted_traffic.append(test_data)
    
    # Add to session
    if 'intercepted_data' not in session:
        session['intercepted_data'] = []
    session['intercepted_data'].append(test_data)
    session.permanent = True
    
    flash('Test traffic data added successfully!', 'success')
    return redirect(url_for('network_protocols.intercepted'))

@network_protocols_bp.route('/intercepted/count')
def intercepted_count():
    """Return just the count of intercepted traffic for auto-refresh"""
    session_data = session.get('intercepted_data', [])
    # Use session data as primary source (survives app restarts)
    global intercepted_traffic
    all_data = session_data if session_data else intercepted_traffic
    
    return jsonify({
        'count': len(all_data),
        'latest_timestamp': all_data[-1]['timestamp'] if all_data else None
    })

@network_protocols_bp.route('/clear-traffic')
def clear_traffic():
    """Clear intercepted traffic for demo reset"""
    global intercepted_traffic
    intercepted_traffic = []
    session.pop('intercepted_data', None)
    flash('Intercepted traffic cleared', 'success')
    return render_template('network/intercepted_traffic.html', 
                         intercepted_traffic=[],
                         total_intercepted=0,
                         unique_usernames=0)

@network_protocols_bp.route('/mitm-simulation')
def mitm_simulation():
    """Interactive man-in-the-middle attack simulation"""
    return render_template('network/mitm_simulation.html')

@network_protocols_bp.route('/mitm-step/<int:step>')
def mitm_step(step):
    """Handle individual MITM simulation steps"""
    steps = {
        1: {
            'title': 'Step 1: Attacker Positioning',
            'description': 'The attacker sets up a rogue Wi-Fi hotspot "Free_Coffee_WiFi" in a busy café.',
            'action': 'Victim connects to the fake network',
            'technical': 'Attacker uses tools like aircrack-ng to create fake access point',
            'status': 'Attacker is now positioned between victim and internet',
            'next_step': 2
        },
        2: {
            'title': 'Step 2: Traffic Interception Begins',
            'description': 'All victim traffic now flows through the attacker\'s device.',
            'action': 'Victim browses to http://bank-example.com',
            'technical': 'Attacker runs Wireshark or tcpdump to capture all packets',
            'status': 'HTTP traffic is being intercepted and logged',
            'next_step': 3
        },
        3: {
            'title': 'Step 3: Credential Capture',
            'description': 'Victim submits login form over unencrypted HTTP.',
            'action': 'Username: john_doe, Password: mySecretPass123',
            'technical': 'POST data captured in plain text: username=john_doe&password=mySecretPass123',
            'status': 'Credentials successfully stolen!',
            'next_step': 4
        },
        4: {
            'title': 'Step 4: Session Hijacking',
            'description': 'Attacker captures and reuses the victim\'s session cookie.',
            'action': 'Attacker uses stolen session to access victim\'s account',
            'technical': 'Cookie: SESSIONID=abc123xyz789 replayed to bank-example.com',
            'status': 'Attacker now has full access to victim\'s banking account',
            'next_step': 5
        },
        5: {
            'title': 'Step 5: Data Exfiltration Complete',
            'description': 'Attack successful - all sensitive data compromised.',
            'action': 'Account balance, transaction history, personal details stolen',
            'technical': 'Complete financial profile extracted and stored',
            'status': 'Mission accomplished - victim remains unaware',
            'next_step': None
        }
    }
    
    if step not in steps:
        return jsonify({'error': 'Invalid step'}), 400
    
    return jsonify(steps[step])

@network_protocols_bp.route('/mitm-attack-choice', methods=['POST'])
def mitm_attack_choice():
    """Handle user's attack method choice"""
    attack_method = request.json.get('method', '')
    
    attack_results = {
        'arp_spoofing': {
            'success_rate': 85,
            'description': 'ARP spoofing successful! Victim\'s traffic redirected through your machine.',
            'technical_details': 'Sent forged ARP replies to associate your MAC address with the gateway IP.',
            'captured_data': ['Login credentials', 'Session cookies', 'Email content'],
            'time_to_detect': '2-5 minutes'
        },
        'dns_spoofing': {
            'success_rate': 70,
            'description': 'DNS spoofing active! Victim redirected to your fake banking site.',
            'technical_details': 'Modified DNS responses to point bank-example.com to your server.',
            'captured_data': ['Banking credentials', 'Account numbers', 'Security questions'],
            'time_to_detect': '1-3 minutes'
        },
        'rogue_wifi': {
            'success_rate': 95,
            'description': 'Rogue Wi-Fi successful! 12 devices connected to your fake hotspot.',
            'technical_details': 'Created "Free_Public_WiFi" access point with stronger signal than legitimate network.',
            'captured_data': ['Multiple user credentials', 'Social media tokens', 'Email passwords'],
            'time_to_detect': '10-30 minutes'
        },
        'bgp_hijacking': {
            'success_rate': 60,
            'description': 'BGP hijacking partially successful! Intercepting traffic for target ASN.',
            'technical_details': 'Announced more specific routes to hijack traffic for 192.168.0.0/16.',
            'captured_data': ['Corporate communications', 'Financial transactions', 'Government data'],
            'time_to_detect': '30 seconds - 2 hours'
        }
    }
    
    result = attack_results.get(attack_method, {
        'success_rate': 0,
        'description': 'Unknown attack method selected.',
        'technical_details': 'Please select a valid attack vector.',
        'captured_data': [],
        'time_to_detect': 'N/A'
    })
    
    return jsonify(result)
