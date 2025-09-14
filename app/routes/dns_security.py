"""
DNS Security Module
Demonstrates DNS vulnerabilities and security measures
"""
from flask import Blueprint, render_template, request, jsonify, session
import json
import random
import time
import base64
from datetime import datetime, timedelta

dns_security_bp = Blueprint('dns_security', __name__)

# Mock DNS database
DNS_RECORDS = {
    'example.com': {
        'A': ['93.184.216.34'],
        'AAAA': ['2606:2800:220:1:248:1893:25c8:1946'],
        'MX': ['10 mail.example.com'],
        'NS': ['ns1.example.com', 'ns2.example.com'],
        'TXT': ['v=spf1 include:_spf.example.com ~all']
    },
    'bank.com': {
        'A': ['198.51.100.1'],
        'MX': ['5 mail.bank.com'],
        'NS': ['ns1.bank.com', 'ns2.bank.com'],
        'TXT': ['v=spf1 mx -all']
    },
    'malicious.com': {
        'A': ['192.0.2.66'],  # Attacker controlled
        'NS': ['ns1.malicious.com'],
        'TXT': ['malware-domain']
    }
}

# DNS poisoning cache
poisoned_cache = {}

def simulate_dns_lookup(domain, record_type='A', use_secure_dns=False):
    """Simulate DNS lookup with optional poisoning"""
    
    # Check for poisoned cache first
    cache_key = f"{domain}:{record_type}"
    if not use_secure_dns and cache_key in poisoned_cache:
        return {
            'domain': domain,
            'type': record_type,
            'records': poisoned_cache[cache_key]['records'],
            'ttl': poisoned_cache[cache_key]['ttl'],
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'source': 'Poisoned Cache',
            'secure': False,
            'poisoned': True
        }
    
    # Normal DNS lookup
    if domain in DNS_RECORDS and record_type in DNS_RECORDS[domain]:
        records = DNS_RECORDS[domain][record_type]
        
        if use_secure_dns:
            # Simulate DoH/DoT with additional security info
            return {
                'domain': domain,
                'type': record_type,
                'records': records,
                'ttl': 3600,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'source': 'Secure DNS (DoH)',
                'secure': True,
                'poisoned': False,
                'dnssec': True,
                'encrypted': True,
                'server': 'cloudflare-dns.com'
            }
        else:
            # Regular DNS
            return {
                'domain': domain,
                'type': record_type,
                'records': records,
                'ttl': 3600,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'source': 'Public DNS',
                'secure': False,
                'poisoned': False
            }
    
    # Domain not found
    return {
        'domain': domain,
        'type': record_type,
        'records': [],
        'error': 'NXDOMAIN',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

@dns_security_bp.route('/')
def index():
    """DNS security concepts overview"""
    return render_template('network/dns_security.html')

@dns_security_bp.route('/lookup', methods=['POST'])
def dns_lookup():
    """Perform DNS lookup simulation"""
    data = request.get_json()
    domain = data.get('domain', '').strip().lower()
    record_type = data.get('record_type', 'A')
    use_secure = data.get('secure', False)
    
    if not domain:
        return jsonify({'error': 'Domain name required'}), 400
    
    # Simulate lookup delay
    time.sleep(random.uniform(0.1, 0.3))
    
    result = simulate_dns_lookup(domain, record_type, use_secure)
    return jsonify(result)

@dns_security_bp.route('/poisoning')
def poisoning_demo():
    """DNS cache poisoning demonstration"""
    
    # Simulate attack scenario
    attack_scenario = {
        'name': 'Banking Website Hijack',
        'target_domain': 'bank.com',
        'legitimate_ip': '198.51.100.1',
        'legitimate_ttl': 300,
        'malicious_ip': '192.0.2.66',
        'malicious_ttl': 86400,
        'attack_method': 'Cache Poisoning',
        'attack_vector': 'Race Condition',
        'description': 'Attacker sends forged DNS responses to poison resolver cache',
        'poison_percentage': 25,
        'poisoned_entries': 3,
        'total_entries': 12,
        'timeline': [
            {
                'time': '00:00',
                'action': 'User queries bank.com',
                'type': 'info'
            },
            {
                'time': '00:01',
                'action': 'DNS resolver forwards query',
                'type': 'info'
            },
            {
                'time': '00:02',
                'action': 'Attacker floods with forged responses',
                'type': 'warning'
            },
            {
                'time': '00:03',
                'action': 'Forged response wins the race',
                'type': 'danger'
            },
            {
                'time': '00:04',
                'action': 'Cache poisoned with malicious IP',
                'type': 'danger'
            }
        ]
    }
    
    return render_template('network/dns_poisoning.html', scenario=attack_scenario)

@dns_security_bp.route('/poison', methods=['POST'])
def perform_poisoning():
    """Simulate DNS cache poisoning attack"""
    data = request.get_json()
    target_domain = data.get('domain', '').strip().lower()
    malicious_ip = data.get('malicious_ip', '192.0.2.66')
    
    if not target_domain:
        return jsonify({'error': 'Target domain required'}), 400
    
    # Add to poisoned cache
    cache_key = f"{target_domain}:A"
    poisoned_cache[cache_key] = {
        'records': [malicious_ip],
        'ttl': 3600,
        'poisoned_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'attacker_ip': '192.0.2.100'
    }
    
    return jsonify({
        'success': True,
        'message': f'DNS cache poisoned for {target_domain}',
        'poisoned_ip': malicious_ip,
        'original_lookup': simulate_dns_lookup(target_domain, 'A', False)
    })

@dns_security_bp.route('/tunneling')
def tunneling_demo():
    """DNS tunneling simulation"""
    
    # Example data to exfiltrate
    raw_data = "credit_card:4532-1234-5678-9012|password:admin123|employee_data:confidential"
    
    # Encode and chunk the data for DNS tunneling
    import base64
    encoded_data = base64.b64encode(raw_data.encode()).decode()
    
    # Split into DNS-compatible chunks (max 63 chars per label)
    chunk_size = 32  # Conservative size for DNS labels
    chunks = [encoded_data[i:i+chunk_size] for i in range(0, len(encoded_data), chunk_size)]
    
    sensitive_data = {
        'original': raw_data,
        'encoded': encoded_data,
        'chunks': chunks
    }
    
    return render_template('network/dns_tunneling.html', data=sensitive_data)

@dns_security_bp.route('/tunnel', methods=['POST'])
def perform_tunneling():
    """Simulate DNS tunneling for data exfiltration"""
    data = request.get_json()
    payload = data.get('payload', '')
    
    if not payload:
        return jsonify({'error': 'Payload required'}), 400
    
    # Encode payload for DNS tunneling
    encoded_payload = base64.b64encode(payload.encode()).decode()
    
    # Split into DNS query chunks (max 63 chars per label)
    chunks = [encoded_payload[i:i+50] for i in range(0, len(encoded_payload), 50)]
    
    dns_queries = []
    for i, chunk in enumerate(chunks):
        query = f"{chunk}.{i}.tunnel.malicious.com"
        dns_queries.append({
            'query': query,
            'type': 'TXT',
            'timestamp': datetime.now().strftime('%H:%M:%S.%f')[:-3],
            'chunk_id': i,
            'data_size': len(chunk)
        })
        time.sleep(0.1)  # Simulate timing
    
    return jsonify({
        'success': True,
        'original_payload': payload,
        'encoded_payload': encoded_payload,
        'total_chunks': len(chunks),
        'dns_queries': dns_queries,
        'detection_difficulty': 'High - Looks like normal DNS traffic'
    })

@dns_security_bp.route('/secure')
def secure_dns():
    """Demonstrate secure DNS implementations"""
    
    security_features = {
        'doh': {
            'name': 'DNS over HTTPS (DoH)',
            'port': 443,
            'encryption': 'HTTPS/TLS',
            'privacy': 'High',
            'performance': 'Good',
            'adoption': 'Growing'
        },
        'dot': {
            'name': 'DNS over TLS (DoT)',
            'port': 853,
            'encryption': 'TLS',
            'privacy': 'High',
            'performance': 'Good',
            'adoption': 'Moderate'
        },
        'dnssec': {
            'name': 'DNS Security Extensions',
            'port': 53,
            'encryption': 'Digital Signatures',
            'privacy': 'Low',
            'performance': 'Slower',
            'adoption': 'Limited'
        }
    }
    
    # DoH Configuration
    doh_config = {
        'provider': 'Cloudflare',
        'endpoint': 'https://cloudflare-dns.com/dns-query',
        'port': 443,
        'protocol': 'HTTPS',
        'encryption': 'TLS 1.3',
        'cipher_suite': 'TLS_AES_256_GCM_SHA384'
    }
    
    # DoT Configuration  
    dot_config = {
        'provider': 'Cloudflare',
        'server': '1dot1dot1dot1.cloudflare-dns.com',
        'port': 853,
        'protocol': 'TLS',
        'encryption': 'TLS 1.3',
        'cipher_suite': 'TLS_AES_256_GCM_SHA384'
    }
    
    dns_providers = [
        {
            'name': 'Cloudflare',
            'primary': '1.1.1.1',
            'secondary': '1.0.0.1',
            'doh': 'https://cloudflare-dns.com/dns-query',
            'features': ['DoH', 'DoT', 'DNSSEC', 'Malware Blocking']
        },
        {
            'name': 'Quad9',
            'primary': '9.9.9.9',
            'secondary': '149.112.112.112',
            'doh': 'https://dns.quad9.net/dns-query',
            'features': ['DoH', 'DoT', 'DNSSEC', 'Threat Blocking']
        },
        {
            'name': 'Google',
            'primary': '8.8.8.8',
            'secondary': '8.8.4.4',
            'doh': 'https://dns.google/dns-query',
            'features': ['DoH', 'DoT', 'DNSSEC']
        }
    ]
    
    return render_template('network/secure_dns.html', 
                         security_features=security_features,
                         dns_providers=dns_providers,
                         doh_config=doh_config,
                         dot_config=dot_config)

@dns_security_bp.route('/clear-poison')
def clear_poison():
    """Clear poisoned DNS cache"""
    global poisoned_cache
    poisoned_cache = {}
    return jsonify({'success': True, 'message': 'DNS cache cleared'})

@dns_security_bp.route('/cache-status')
def cache_status():
    """Get current DNS cache status"""
    return jsonify({
        'poisoned_entries': len(poisoned_cache),
        'cache': poisoned_cache
    })
