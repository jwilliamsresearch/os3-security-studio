from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import re
from ..models.database import get_db_connection

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    return render_template('auth/index.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, password_hash FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user[1], password):
            session['user_id'] = user[0]
            session['username'] = username
            flash('Logged in successfully!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid credentials!', 'danger')
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('main.index'))

@auth_bp.route('/insecure-register', methods=['GET', 'POST'])
def insecure_register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        # INSECURE: No password validation, plain text storage (simulated)
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Still hash for demo purposes, but show weak validation
            password_hash = generate_password_hash(password)
            cursor.execute('INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)', 
                         (username, password_hash, email))
            conn.commit()
            flash('Account created! (Insecure - weak password policy)', 'warning')
        except Exception:
            flash('Username already exists!', 'danger')
        finally:
            conn.close()
    
    return render_template('auth/insecure_register.html')

@auth_bp.route('/secure-register', methods=['GET', 'POST'])
def secure_register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        # SECURE: Strong password validation
        if len(password) < 8:
            flash('Password must be at least 8 characters long!', 'danger')
            return render_template('auth/secure_register.html')
        
        if not re.search(r'[A-Z]', password):
            flash('Password must contain at least one uppercase letter!', 'danger')
            return render_template('auth/secure_register.html')
        
        if not re.search(r'[a-z]', password):
            flash('Password must contain at least one lowercase letter!', 'danger')
            return render_template('auth/secure_register.html')
        
        if not re.search(r'\d', password):
            flash('Password must contain at least one number!', 'danger')
            return render_template('auth/secure_register.html')
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            flash('Password must contain at least one special character!', 'danger')
            return render_template('auth/secure_register.html')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            password_hash = generate_password_hash(password)
            cursor.execute('INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)', 
                         (username, password_hash, email))
            conn.commit()
            flash('Account created with strong password!', 'success')
        except Exception:
            flash('Username already exists!', 'danger')
        finally:
            conn.close()
    
    return render_template('auth/secure_register.html')
