from flask import Blueprint, render_template, request, flash, jsonify
import requests
import urllib.parse
from urllib.parse import urlparse
import re
import socket

ssrf_bp = Blueprint('ssrf', __name__)

@ssrf_bp.route('/')
def index():
    return render_template('ssrf/index.html')

@ssrf_bp.route('/insecure')
def insecure():
    return render_template('ssrf/insecure.html')

@ssrf_bp.route('/insecure/fetch', methods=['POST'])
def insecure_fetch():
    """INSECURE: No URL validation - vulnerable to SSRF attacks"""
    url = request.json.get('url', '')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    try:
        # VULNERABLE: Direct request without validation
        response = requests.get(url, timeout=5)
        return jsonify({
            'status_code': response.status_code,
            'content': response.text[:1000],  # Truncate for demo
            'headers': dict(response.headers)
        })
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500

@ssrf_bp.route('/secure')
def secure():
    return render_template('ssrf/secure.html')

@ssrf_bp.route('/secure/fetch', methods=['POST'])
def secure_fetch():
    """SECURE: Proper URL validation and restrictions"""
    url = request.json.get('url', '')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    # SECURE: Validate URL format
    try:
        parsed = urlparse(url)
    except Exception:
        return jsonify({'error': 'Invalid URL format'}), 400
    
    # SECURE: Only allow HTTP/HTTPS
    if parsed.scheme not in ['http', 'https']:
        return jsonify({'error': 'Only HTTP and HTTPS protocols are allowed'}), 400
    
    # SECURE: Block localhost and private IPs
    if _is_private_or_localhost(parsed.hostname):
        return jsonify({'error': 'Access to private/localhost addresses is not allowed'}), 400
    
    # SECURE: Whitelist allowed domains
    allowed_domains = [
        'httpbin.org',
        'jsonplaceholder.typicode.com',
        'api.github.com',
        'www.example.com'
    ]
    
    if parsed.hostname not in allowed_domains:
        return jsonify({'error': f'Domain {parsed.hostname} is not in the allowed list'}), 400
    
    try:
        # SECURE: Additional safety headers and timeout
        response = requests.get(
            url, 
            timeout=3,
            allow_redirects=False,  # Prevent redirect-based bypasses
            headers={'User-Agent': 'SecureLab/1.0'}
        )
        
        return jsonify({
            'status_code': response.status_code,
            'content': response.text[:1000],
            'headers': dict(response.headers),
            'message': 'Request completed securely'
        })
    except requests.RequestException as e:
        return jsonify({'error': f'Request failed: {str(e)}'}), 500

def _is_private_or_localhost(hostname):
    """Check if hostname resolves to private or localhost IP"""
    if not hostname:
        return True
    
    # Check for localhost variations
    localhost_patterns = [
        'localhost', '127.0.0.1', '::1', '0.0.0.0',
        '10.', '172.16.', '172.17.', '172.18.', '172.19.',
        '172.20.', '172.21.', '172.22.', '172.23.',
        '172.24.', '172.25.', '172.26.', '172.27.',
        '172.28.', '172.29.', '172.30.', '172.31.',
        '192.168.'
    ]
    
    hostname_lower = hostname.lower()
    for pattern in localhost_patterns:
        if hostname_lower.startswith(pattern):
            return True
    
    try:
        # Resolve hostname to IP and check if private
        ip = socket.gethostbyname(hostname)
        return _is_private_ip(ip)
    except socket.gaierror:
        return True  # If can't resolve, block it
    
def _is_private_ip(ip):
    """Check if IP is in private ranges"""
    try:
        parts = [int(x) for x in ip.split('.')]
        
        # Check private IP ranges
        if parts[0] == 10:  # 10.0.0.0/8
            return True
        if parts[0] == 172 and 16 <= parts[1] <= 31:  # 172.16.0.0/12
            return True
        if parts[0] == 192 and parts[1] == 168:  # 192.168.0.0/16
            return True
        if parts[0] == 127:  # 127.0.0.0/8 (localhost)
            return True
        if parts[0] == 169 and parts[1] == 254:  # 169.254.0.0/16 (link-local)
            return True
            
        return False
    except (ValueError, IndexError):
        return True  # If invalid IP format, block it
