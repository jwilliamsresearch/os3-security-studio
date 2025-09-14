"""
Security Logging and Monitoring Failures Demo - OWASP Top 10 2021: A09
This module demonstrates insufficient logging, monitoring, and incident response
"""

from flask import Blueprint, render_template, request, jsonify, session
import json
import logging
import time
import random
from datetime import datetime, timedelta
import os

# Create blueprint
logging_monitoring_bp = Blueprint('logging_monitoring', __name__)

# Configure different loggers for demonstration
def setup_demo_loggers():
    """Setup various logging configurations for demonstration"""
    
    # Insecure logger - no security events
    insecure_logger = logging.getLogger('insecure_app')
    insecure_handler = logging.StreamHandler()
    insecure_handler.setLevel(logging.ERROR)  # Only errors, no security events
    insecure_logger.addHandler(insecure_handler)
    insecure_logger.setLevel(logging.ERROR)
    
    # Secure logger - comprehensive security logging
    secure_logger = logging.getLogger('secure_app')
    secure_handler = logging.StreamHandler()
    secure_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s - [IP: %(ip)s] [User: %(user)s] [Session: %(session_id)s]'
    )
    secure_handler.setFormatter(secure_formatter)
    secure_logger.addHandler(secure_handler)
    secure_logger.setLevel(logging.INFO)
    
    return insecure_logger, secure_logger

# Initialize loggers
insecure_logger, secure_logger = setup_demo_loggers()

# Simulated log storage
security_logs = []
attack_attempts = []
failed_logins = []

@logging_monitoring_bp.route('/')
def index():
    """Main logging and monitoring demonstration page"""
    return render_template('logging_monitoring/index.html')

@logging_monitoring_bp.route('/insecure-logging')
def insecure_logging():
    """Demonstrate poor logging practices"""
    return render_template('logging_monitoring/insecure_logging.html')

@logging_monitoring_bp.route('/secure-logging')
def secure_logging():
    """Demonstrate proper security logging"""
    return render_template('logging_monitoring/secure_logging.html')

@logging_monitoring_bp.route('/simulate_attack', methods=['POST'])
def simulate_attack():
    """Simulate various types of attacks and log them differently"""
    try:
        data = request.get_json()
        attack_type = data.get('attack_type', 'unknown')
        logging_mode = data.get('logging_mode', 'insecure')
        user_ip = request.remote_addr
        user_agent = request.headers.get('User-Agent', 'Unknown')
        
        # Generate attack data
        attack_data = {
            'timestamp': datetime.now().isoformat(),
            'attack_type': attack_type,
            'source_ip': user_ip,
            'user_agent': user_agent,
            'session_id': session.get('session_id', 'anonymous'),
            'user_id': session.get('user_id', 'unknown')
        }
        
        if logging_mode == 'insecure':
            # INSECURE: Minimal or no logging of security events
            if attack_type == 'sql_injection':
                # Don't log SQL injection attempts
                pass
            elif attack_type == 'xss':
                # Log as generic error without context
                insecure_logger.error("Application error occurred")
            elif attack_type == 'brute_force':
                # Don't track failed login attempts
                pass
            elif attack_type == 'file_upload':
                # Generic file processing error
                insecure_logger.error("File processing failed")
            
            response_data = {
                'logged': False,
                'message': 'Attack processed with minimal logging',
                'security_risk': 'High - No security monitoring, attacks go undetected'
            }
            
        else:
            # SECURE: Comprehensive security logging
            log_entry = {
                'timestamp': attack_data['timestamp'],
                'event_type': 'SECURITY_INCIDENT',
                'attack_type': attack_type,
                'source_ip': user_ip,
                'user_agent': user_agent,
                'session_id': attack_data['session_id'],
                'user_id': attack_data['user_id'],
                'severity': get_attack_severity(attack_type),
                'details': get_attack_details(attack_type)
            }
            
            # Log to secure logger with extra context
            extra_context = {
                'ip': user_ip,
                'user': attack_data['user_id'],
                'session_id': attack_data['session_id']
            }
            
            secure_logger.warning(
                f"SECURITY INCIDENT: {attack_type} attempt from {user_ip}",
                extra=extra_context
            )
            
            # Store in security logs
            security_logs.append(log_entry)
            
            # Track specific attack patterns
            if attack_type == 'brute_force':
                failed_logins.append({
                    'ip': user_ip,
                    'timestamp': attack_data['timestamp'],
                    'user_agent': user_agent
                })
            
            attack_attempts.append(attack_data)
            
            response_data = {
                'logged': True,
                'log_entry': log_entry,
                'message': 'Attack logged with full security context',
                'security_benefit': 'Enables detection, analysis, and incident response'
            }
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@logging_monitoring_bp.route('/get_security_logs')
def get_security_logs():
    """Get recent security logs for monitoring dashboard"""
    try:
        # Return recent logs (last 10)
        recent_logs = security_logs[-10:] if len(security_logs) > 10 else security_logs
        
        # Generate some statistics
        stats = {
            'total_incidents': len(security_logs),
            'recent_incidents': len([log for log in security_logs 
                                   if datetime.fromisoformat(log['timestamp']) > 
                                   datetime.now() - timedelta(hours=1)]),
            'top_attack_types': get_top_attack_types(),
            'top_source_ips': get_top_source_ips(),
            'severity_breakdown': get_severity_breakdown()
        }
        
        return jsonify({
            'logs': recent_logs,
            'statistics': stats,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@logging_monitoring_bp.route('/detect_anomalies', methods=['POST'])
def detect_anomalies():
    """Demonstrate anomaly detection capabilities"""
    try:
        data = request.get_json()
        detection_type = data.get('type', 'basic')
        
        anomalies = []
        
        if detection_type == 'brute_force':
            # Detect brute force patterns
            ip_attempts = {}
            for attempt in failed_logins[-50:]:  # Check last 50 attempts
                ip = attempt['ip']
                ip_attempts[ip] = ip_attempts.get(ip, 0) + 1
            
            for ip, count in ip_attempts.items():
                if count >= 5:  # 5+ failed attempts
                    anomalies.append({
                        'type': 'brute_force',
                        'severity': 'high',
                        'description': f'Brute force attack detected from {ip}',
                        'count': count,
                        'ip': ip
                    })
        
        elif detection_type == 'rate_limiting':
            # Detect rate limiting violations
            recent_attacks = [attack for attack in attack_attempts 
                            if datetime.fromisoformat(attack['timestamp']) > 
                            datetime.now() - timedelta(minutes=5)]
            
            if len(recent_attacks) > 10:
                anomalies.append({
                    'type': 'rate_limit_violation',
                    'severity': 'medium',
                    'description': f'High request rate detected: {len(recent_attacks)} requests in 5 minutes',
                    'count': len(recent_attacks)
                })
        
        elif detection_type == 'suspicious_patterns':
            # Detect suspicious patterns
            attack_types = [attack['attack_type'] for attack in attack_attempts[-20:]]
            unique_attacks = set(attack_types)
            
            if len(unique_attacks) >= 3:
                anomalies.append({
                    'type': 'multiple_attack_vectors',
                    'severity': 'high',
                    'description': f'Multiple attack types detected: {", ".join(unique_attacks)}',
                    'attack_types': list(unique_attacks)
                })
        
        return jsonify({
            'anomalies': anomalies,
            'detection_type': detection_type,
            'timestamp': datetime.now().isoformat(),
            'total_checked': len(attack_attempts)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@logging_monitoring_bp.route('/generate_alert', methods=['POST'])
def generate_alert():
    """Generate security alerts based on log analysis"""
    try:
        data = request.get_json()
        alert_type = data.get('alert_type', 'generic')
        
        alert = {
            'id': f"ALERT-{int(time.time())}",
            'timestamp': datetime.now().isoformat(),
            'type': alert_type,
            'status': 'active',
            'source': 'OS³ Security Monitor'
        }
        
        if alert_type == 'critical_incident':
            alert.update({
                'severity': 'critical',
                'title': 'Critical Security Incident Detected',
                'description': 'Multiple high-severity attacks detected from same source',
                'recommended_actions': [
                    'Block source IP immediately',
                    'Review user accounts for compromise',
                    'Escalate to security team',
                    'Increase monitoring sensitivity'
                ]
            })
        
        elif alert_type == 'data_breach':
            alert.update({
                'severity': 'high',
                'title': 'Potential Data Breach Detected',
                'description': 'Unusual data access patterns detected',
                'recommended_actions': [
                    'Investigate data access logs',
                    'Check for privilege escalation',
                    'Notify data protection officer',
                    'Consider user notification'
                ]
            })
        
        elif alert_type == 'account_compromise':
            alert.update({
                'severity': 'medium',
                'title': 'Account Compromise Suspected',
                'description': 'Suspicious login patterns detected',
                'recommended_actions': [
                    'Force password reset',
                    'Review recent user activity',
                    'Enable additional authentication',
                    'Monitor user behavior'
                ]
            })
        
        return jsonify({
            'alert': alert,
            'message': 'Security alert generated successfully',
            'next_steps': 'Alert would be sent to SIEM/security team'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_attack_severity(attack_type):
    """Get severity level for attack type"""
    severity_map = {
        'sql_injection': 'high',
        'xss': 'medium',
        'brute_force': 'high',
        'file_upload': 'medium',
        'csrf': 'medium',
        'ssrf': 'high'
    }
    return severity_map.get(attack_type, 'low')

def get_attack_details(attack_type):
    """Get detailed description for attack type"""
    details_map = {
        'sql_injection': 'Attempted database manipulation through SQL injection',
        'xss': 'Cross-site scripting attempt detected',
        'brute_force': 'Brute force login attempt detected',
        'file_upload': 'Malicious file upload attempt',
        'csrf': 'Cross-site request forgery attempt',
        'ssrf': 'Server-side request forgery attempt'
    }
    return details_map.get(attack_type, 'Unknown attack pattern')

def get_top_attack_types():
    """Get most common attack types"""
    attack_types = [log['attack_type'] for log in security_logs]
    type_counts = {}
    for attack_type in attack_types:
        type_counts[attack_type] = type_counts.get(attack_type, 0) + 1
    
    return sorted(type_counts.items(), key=lambda x: x[1], reverse=True)[:5]

def get_top_source_ips():
    """Get most active source IPs"""
    source_ips = [log['source_ip'] for log in security_logs]
    ip_counts = {}
    for ip in source_ips:
        ip_counts[ip] = ip_counts.get(ip, 0) + 1
    
    return sorted(ip_counts.items(), key=lambda x: x[1], reverse=True)[:5]

def get_severity_breakdown():
    """Get breakdown of incidents by severity"""
    severities = [log['severity'] for log in security_logs]
    severity_counts = {}
    for severity in severities:
        severity_counts[severity] = severity_counts.get(severity, 0) + 1
    
    return severity_counts
