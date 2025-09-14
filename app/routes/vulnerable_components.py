"""
Vulnerable Components Demo - OWASP Top 10 2021: A06
This module demonstrates vulnerabilities in third-party components and dependencies
"""

from flask import Blueprint, render_template, request, jsonify, session
import json
import subprocess
import os
import tempfile
import yaml
import pickle
import base64
from datetime import datetime

# Create blueprint
vulnerable_components_bp = Blueprint('vulnerable_components', __name__)

@vulnerable_components_bp.route('/')
def index():
    """Main vulnerable components demonstration page"""
    return render_template('vulnerable_components/index.html')

@vulnerable_components_bp.route('/outdated-libs')
def outdated_libs():
    """Demonstrate using outdated vulnerable libraries"""
    return render_template('vulnerable_components/outdated_libs.html')

@vulnerable_components_bp.route('/insecure-deserialization')
def insecure_deserialization():
    """Demonstrate insecure deserialization vulnerabilities"""
    return render_template('vulnerable_components/insecure_deserialization.html')

@vulnerable_components_bp.route('/check_vulnerability', methods=['POST'])
def check_vulnerability():
    """Check if a package version has known vulnerabilities"""
    try:
        data = request.get_json()
        package = data.get('package', '')
        version = data.get('version', '')
        
        # Simulate vulnerability database lookup
        vulnerable_packages = {
            'requests': {
                '2.19.1': {
                    'cve': 'CVE-2018-18074',
                    'severity': 'Medium',
                    'description': 'Improper handling of redirects',
                    'fixed_in': '2.20.0'
                },
                '2.8.1': {
                    'cve': 'CVE-2015-2296',
                    'severity': 'High', 
                    'description': 'Certificate verification bypass',
                    'fixed_in': '2.9.0'
                }
            },
            'pyyaml': {
                '3.12': {
                    'cve': 'CVE-2017-18342',
                    'severity': 'Critical',
                    'description': 'Arbitrary code execution via unsafe yaml.load()',
                    'fixed_in': '3.13'
                },
                '5.3': {
                    'cve': 'CVE-2020-1747',
                    'severity': 'High',
                    'description': 'Arbitrary code execution',
                    'fixed_in': '5.3.1'
                }
            },
            'django': {
                '1.11.0': {
                    'cve': 'CVE-2017-7233',
                    'severity': 'Medium',
                    'description': 'Open redirect vulnerability',
                    'fixed_in': '1.11.1'
                },
                '2.2.0': {
                    'cve': 'CVE-2019-14232',
                    'severity': 'High',
                    'description': 'Denial of service via truncated emails',
                    'fixed_in': '2.2.4'
                }
            },
            'flask': {
                '0.12.0': {
                    'cve': 'CVE-2018-1000656',
                    'severity': 'High',
                    'description': 'Improper input validation',
                    'fixed_in': '0.12.3'
                }
            }
        }
        
        vulnerability = None
        if package.lower() in vulnerable_packages:
            if version in vulnerable_packages[package.lower()]:
                vulnerability = vulnerable_packages[package.lower()][version]
        
        return jsonify({
            'package': package,
            'version': version,
            'vulnerable': vulnerability is not None,
            'vulnerability': vulnerability,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@vulnerable_components_bp.route('/unsafe_yaml_load', methods=['POST'])
def unsafe_yaml_load():
    """Demonstrate unsafe YAML deserialization (vulnerable)"""
    try:
        data = request.get_json()
        yaml_content = data.get('yaml_content', '')
        
        # VULNERABLE: Using yaml.load without safe loader
        # This can execute arbitrary Python code
        try:
            # Create a safe environment for demo
            restricted_globals = {
                '__builtins__': {
                    'len': len,
                    'str': str,
                    'int': int,
                    'float': float,
                    'list': list,
                    'dict': dict,
                    'print': lambda *args: None,  # Disable print
                }
            }
            
            # Parse YAML unsafely (for demonstration)
            parsed_data = yaml.load(yaml_content, Loader=yaml.UnsafeLoader)
            
            return jsonify({
                'success': True,
                'parsed_data': str(parsed_data)[:500],  # Limit output
                'warning': 'This used unsafe YAML loading - could execute arbitrary code!',
                'method': 'yaml.load() with UnsafeLoader'
            })
            
        except Exception as parse_error:
            return jsonify({
                'success': False,
                'error': f'YAML parsing error: {str(parse_error)}',
                'warning': 'Even errors can be dangerous with unsafe YAML loading!'
            })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@vulnerable_components_bp.route('/safe_yaml_load', methods=['POST'])
def safe_yaml_load():
    """Demonstrate safe YAML deserialization"""
    try:
        data = request.get_json()
        yaml_content = data.get('yaml_content', '')
        
        # SECURE: Using yaml.safe_load
        try:
            parsed_data = yaml.safe_load(yaml_content)
            
            return jsonify({
                'success': True,
                'parsed_data': parsed_data,
                'info': 'This used safe YAML loading - no code execution possible',
                'method': 'yaml.safe_load()'
            })
            
        except yaml.YAMLError as parse_error:
            return jsonify({
                'success': False,
                'error': f'YAML parsing error: {str(parse_error)}',
                'info': 'Safe YAML loading prevents code execution'
            })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@vulnerable_components_bp.route('/unsafe_pickle', methods=['POST'])
def unsafe_pickle():
    """Demonstrate unsafe pickle deserialization (vulnerable)"""
    try:
        data = request.get_json()
        pickle_data = data.get('pickle_data', '')
        
        try:
            # Decode base64
            pickle_bytes = base64.b64decode(pickle_data)
            
            # VULNERABLE: Unpickling untrusted data
            # For safety, we'll simulate this rather than actually unpickle
            return jsonify({
                'success': True,
                'warning': 'Unsafe pickle deserialization attempted!',
                'info': 'This could execute arbitrary code if the pickle contained malicious payloads',
                'method': 'pickle.loads() on untrusted data',
                'simulated': True,
                'data_length': len(pickle_bytes)
            })
            
        except Exception as parse_error:
            return jsonify({
                'success': False,
                'error': f'Pickle error: {str(parse_error)}',
                'warning': 'Even malformed pickle data can be dangerous!'
            })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@vulnerable_components_bp.route('/package_info', methods=['POST'])
def package_info():
    """Get information about installed packages"""
    try:
        data = request.get_json()
        package_name = data.get('package', '')
        
        # Simulate package information
        packages_info = {
            'requests': {'version': '2.19.1', 'last_updated': '2018-06-14'},
            'pyyaml': {'version': '3.12', 'last_updated': '2017-01-01'},
            'django': {'version': '1.11.0', 'last_updated': '2017-04-04'},
            'flask': {'version': '0.12.0', 'last_updated': '2016-12-21'},
            'numpy': {'version': '1.16.0', 'last_updated': '2019-01-13'},
            'pillow': {'version': '5.0.0', 'last_updated': '2018-01-01'}
        }
        
        if package_name.lower() in packages_info:
            return jsonify({
                'package': package_name,
                'found': True,
                'info': packages_info[package_name.lower()]
            })
        else:
            return jsonify({
                'package': package_name,
                'found': False,
                'message': 'Package not found in simulated environment'
            })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@vulnerable_components_bp.route('/generate_vulnerable_yaml')
def generate_vulnerable_yaml():
    """Generate example vulnerable YAML payload"""
    vulnerable_yaml = """
# This YAML contains a malicious payload that would execute code
# if loaded with yaml.load() instead of yaml.safe_load()

user_data:
  name: "John Doe"
  email: "john@example.com"
  
# MALICIOUS PAYLOAD (disabled for safety):
# dangerous: !!python/object/apply:os.system ["echo 'System compromised!'"]

# This would be dangerous:
# exploit: !!python/object/apply:subprocess.check_output [["whoami"]]

safe_data:
  message: "This part is safe"
  numbers: [1, 2, 3, 4, 5]
"""
    
    return jsonify({
        'yaml_content': vulnerable_yaml.strip(),
        'warning': 'This YAML contains commented-out malicious payloads',
        'info': 'Uncomment the dangerous lines to see how unsafe YAML loading can execute code'
    })

@vulnerable_components_bp.route('/generate_pickle_payload')
def generate_pickle_payload():
    """Generate example pickle payload (safe simulation)"""
    # Create a safe pickle for demonstration
    safe_data = {
        'user': 'demo_user',
        'data': [1, 2, 3, 4, 5],
        'message': 'This is safe pickle data'
    }
    
    # Pickle and encode
    pickled_data = pickle.dumps(safe_data)
    encoded_data = base64.b64encode(pickled_data).decode()
    
    return jsonify({
        'pickle_data': encoded_data,
        'info': 'This is safe pickle data, but malicious pickle could contain arbitrary code',
        'warning': 'Never unpickle data from untrusted sources!'
    })
