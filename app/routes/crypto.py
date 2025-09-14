from flask import Blueprint, render_template, request, flash, session, jsonify
import hashlib
import base64
import secrets
import bcrypt
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os

crypto_bp = Blueprint('crypto', __name__)

# Simulated database for demo
users_db = {}
encrypted_data = {}

@crypto_bp.route('/')
def index():
    return render_template('crypto/index.html')

@crypto_bp.route('/insecure')
def insecure():
    return render_template('crypto/insecure.html')

@crypto_bp.route('/insecure/hash', methods=['POST'])
def insecure_hash():
    """INSECURE: Uses weak MD5 hashing"""
    password = request.json.get('password', '')
    
    if not password:
        return jsonify({'error': 'Password is required'}), 400
    
    # VULNERABLE: MD5 is cryptographically broken
    md5_hash = hashlib.md5(password.encode()).hexdigest()
    
    # VULNERABLE: Simple SHA1 without salt
    sha1_hash = hashlib.sha1(password.encode()).hexdigest()
    
    return jsonify({
        'md5_hash': md5_hash,
        'sha1_hash': sha1_hash,
        'warning': 'These hashes are weak and easily crackable!'
    })

@crypto_bp.route('/insecure/encrypt', methods=['POST'])
def insecure_encrypt():
    """INSECURE: Weak encryption with hardcoded key"""
    data = request.json.get('data', '')
    
    if not data:
        return jsonify({'error': 'Data is required'}), 400
    
    # VULNERABLE: Hardcoded encryption key
    hardcoded_key = "this_is_a_secret_key_1234567890123456"
    
    # VULNERABLE: Simple XOR encryption (toy cipher)
    key_bytes = hardcoded_key.encode()
    data_bytes = data.encode()
    
    encrypted = bytearray()
    for i, byte in enumerate(data_bytes):
        encrypted.append(byte ^ key_bytes[i % len(key_bytes)])
    
    encrypted_b64 = base64.b64encode(encrypted).decode()
    
    return jsonify({
        'encrypted_data': encrypted_b64,
        'key_used': hardcoded_key,
        'method': 'XOR with hardcoded key',
        'warning': 'This encryption is trivially breakable!'
    })

@crypto_bp.route('/secure')
def secure():
    return render_template('crypto/secure.html')

@crypto_bp.route('/secure/hash', methods=['POST'])
def secure_hash():
    """SECURE: Uses strong bcrypt hashing with salt"""
    password = request.json.get('password', '')
    
    if not password:
        return jsonify({'error': 'Password is required'}), 400
    
    # SECURE: bcrypt with automatic salt generation
    salt = bcrypt.gensalt(rounds=12)  # Adjustable work factor
    bcrypt_hash = bcrypt.hashpw(password.encode(), salt)
    
    # SECURE: PBKDF2 with random salt
    salt_pbkdf2 = secrets.token_bytes(32)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt_pbkdf2,
        iterations=100000,  # High iteration count
    )
    pbkdf2_hash = kdf.derive(password.encode())
    
    return jsonify({
        'bcrypt_hash': bcrypt_hash.decode(),
        'pbkdf2_hash': base64.b64encode(pbkdf2_hash).decode(),
        'pbkdf2_salt': base64.b64encode(salt_pbkdf2).decode(),
        'iterations': 100000,
        'message': 'Secure hashing with proper salts and work factors'
    })

@crypto_bp.route('/secure/encrypt', methods=['POST'])
def secure_encrypt():
    """SECURE: Strong encryption with proper key derivation"""
    data = request.json.get('data', '')
    password = request.json.get('password', 'default_secure_password')
    
    if not data:
        return jsonify({'error': 'Data is required'}), 400
    
    # SECURE: Generate random salt
    salt = secrets.token_bytes(16)
    
    # SECURE: Derive key from password using PBKDF2
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    
    # SECURE: Use Fernet (AES 128 in CBC mode with HMAC)
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data.encode())
    
    return jsonify({
        'encrypted_data': base64.b64encode(encrypted_data).decode(),
        'salt': base64.b64encode(salt).decode(),
        'method': 'AES-128-CBC with HMAC authentication',
        'key_derivation': 'PBKDF2 with 100,000 iterations',
        'message': 'Data encrypted with industry-standard cryptography'
    })

@crypto_bp.route('/secure/decrypt', methods=['POST'])
def secure_decrypt():
    """SECURE: Decrypt data with proper validation"""
    encrypted_data_b64 = request.json.get('encrypted_data', '')
    salt_b64 = request.json.get('salt', '')
    password = request.json.get('password', 'default_secure_password')
    
    if not encrypted_data_b64 or not salt_b64:
        return jsonify({'error': 'Encrypted data and salt are required'}), 400
    
    try:
        # Decode the encrypted data and salt
        encrypted_data = base64.b64decode(encrypted_data_b64)
        salt = base64.b64decode(salt_b64)
        
        # Derive the same key using the salt
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        
        # Decrypt
        fernet = Fernet(key)
        decrypted_data = fernet.decrypt(encrypted_data)
        
        return jsonify({
            'decrypted_data': decrypted_data.decode(),
            'message': 'Successfully decrypted with correct password'
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Decryption failed - wrong password or corrupted data',
            'details': str(e)
        }), 400

# Additional routes that match frontend expectations
@crypto_bp.route('/weak_hash', methods=['POST'])
def weak_hash():
    """INSECURE: Weak hash for frontend compatibility"""
    data = request.get_json()
    password = data.get('password', '')
    
    if not password:
        return jsonify({'error': 'Password is required'}), 400
    
    # VULNERABLE: MD5 without salt
    md5_hash = hashlib.md5(password.encode()).hexdigest()
    
    return jsonify({
        'hash': md5_hash,
        'method': 'MD5 (insecure)'
    })

@crypto_bp.route('/weak_encrypt', methods=['POST'])
def weak_encrypt():
    """INSECURE: Weak encryption for frontend compatibility"""
    data = request.get_json()
    plaintext = data.get('data', '')
    
    if not plaintext:
        return jsonify({'error': 'Data is required'}), 400
    
    # VULNERABLE: Hardcoded key with simple XOR
    key = "hardcoded_key"
    encrypted = ""
    
    for i, char in enumerate(plaintext):
        key_char = key[i % len(key)]
        encrypted_char = chr(ord(char) ^ ord(key_char))
        encrypted += encrypted_char
    
    # Encode to make it displayable
    encrypted_b64 = base64.b64encode(encrypted.encode('latin-1')).decode()
    
    return jsonify({
        'encrypted': encrypted_b64,
        'key': key,
        'method': 'XOR with hardcoded key (insecure)'
    })

@crypto_bp.route('/strong_hash', methods=['POST'])
def strong_hash():
    """SECURE: Strong hash for frontend compatibility"""
    data = request.get_json()
    password = data.get('password', '')
    cost = data.get('cost', 12)
    
    if not password:
        return jsonify({'error': 'Password is required'}), 400
    
    # SECURE: bcrypt with salt
    salt = bcrypt.gensalt(rounds=cost)
    hash_bytes = bcrypt.hashpw(password.encode(), salt)
    
    return jsonify({
        'hash': hash_bytes.decode(),
        'cost': cost,
        'method': 'bcrypt (secure)'
    })

@crypto_bp.route('/strong_encrypt', methods=['POST'])
def strong_encrypt():
    """SECURE: Strong encryption for frontend compatibility"""
    data = request.get_json()
    plaintext = data.get('data', '')
    password = data.get('password', '')
    
    if not plaintext or not password:
        return jsonify({'error': 'Data and password are required'}), 400
    
    # SECURE: PBKDF2 + AES encryption
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    
    # Encrypt with Fernet (AES-128 in CBC mode with HMAC)
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(plaintext.encode())
    
    return jsonify({
        'encrypted': base64.b64encode(encrypted_data).decode(),
        'salt': base64.b64encode(salt).decode(),
        'iterations': 100000,
        'method': 'PBKDF2 + AES (secure)'
    })

@crypto_bp.route('/derive_key', methods=['POST'])
def derive_key():
    """Demonstrate key derivation"""
    data = request.get_json()
    password = data.get('password', '')
    iterations = data.get('iterations', 100000)
    
    if not password:
        return jsonify({'error': 'Password is required'}), 400
    
    # Generate random salt
    salt = os.urandom(16)
    
    # Derive key using PBKDF2
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
    )
    derived_key = kdf.derive(password.encode())
    
    return jsonify({
        'key': base64.b64encode(derived_key).decode(),
        'salt': base64.b64encode(salt).decode(),
        'iterations': iterations,
        'method': 'PBKDF2-SHA256'
    })

@crypto_bp.route('/decrypt', methods=['POST'])
def decrypt():
    """Decrypt data"""
    data = request.get_json()
    encrypted_b64 = data.get('encrypted', '')
    password = data.get('password', '')
    
    if not encrypted_b64 or not password:
        return jsonify({'error': 'Encrypted data and password are required'}), 400
    
    try:
        # For demo purposes, we'll try to decrypt with a simple approach
        # In real implementation, you'd need the salt and parameters used during encryption
        
        # Try to decode
        encrypted_data = base64.b64decode(encrypted_b64)
        
        # This is a simplified decryption for demo
        # Real implementation would need proper salt and key derivation
        return jsonify({
            'success': True,
            'decrypted': 'Decryption successful (demo)',
            'note': 'In real implementation, proper salt and key derivation would be needed'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Decryption failed: {str(e)}'
        })

@crypto_bp.route('/demo/weak-keys')
def demo_weak_keys():
    """Demo showing weak vs strong key generation"""
    # WEAK: Predictable keys
    weak_keys = [
        "123456",
        "password",
        "qwerty",
        "secret",
        "admin123"
    ]
    
    # STRONG: Cryptographically secure random keys
    strong_key_hex = secrets.token_hex(32)  # 256 bits
    strong_key_b64 = base64.b64encode(secrets.token_bytes(32)).decode()
    
    return jsonify({
        'weak_keys': weak_keys,
        'strong_key_hex': strong_key_hex,
        'strong_key_base64': strong_key_b64,
        'entropy_bits': 256,
        'message': 'Always use cryptographically secure random number generators'
    })
