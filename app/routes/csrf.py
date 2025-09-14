from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from ..models.database import get_db_connection
from ..utils.auth import login_required, generate_csrf_token, validate_csrf_token

csrf_bp = Blueprint('csrf', __name__)

@csrf_bp.route('/')
def index():
    return render_template('csrf/index.html')

@csrf_bp.route('/insecure')
@login_required
def insecure():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT balance FROM users WHERE id = ?', (session['user_id'],))
    balance = cursor.fetchone()[0]
    conn.close()
    return render_template('csrf/insecure.html', balance=balance)

@csrf_bp.route('/insecure/transfer', methods=['POST'])
@login_required
def insecure_transfer():
    amount = float(request.form.get('amount', 0))
    recipient = request.form.get('recipient', '')
    
    if amount > 0:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Update sender balance
        cursor.execute('UPDATE users SET balance = balance - ? WHERE id = ?', (amount, session['user_id']))
        
        # Update recipient balance (if exists)
        cursor.execute('UPDATE users SET balance = balance + ? WHERE username = ?', (amount, recipient))
        
        conn.commit()
        conn.close()
        
        flash(f'Transferred ${amount} to {recipient}', 'success')
    
    return redirect(url_for('csrf.insecure'))

@csrf_bp.route('/secure')
@login_required
def secure():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT balance FROM users WHERE id = ?', (session['user_id'],))
    balance = cursor.fetchone()[0]
    conn.close()
    return render_template('csrf/secure.html', balance=balance, csrf_token=generate_csrf_token())

@csrf_bp.route('/secure/transfer', methods=['POST'])
@login_required
def secure_transfer():
    # SECURE: Validate CSRF token
    csrf_token = request.form.get('csrf_token', '')
    if not validate_csrf_token(csrf_token):
        flash('Invalid CSRF token!', 'danger')
        return redirect(url_for('csrf.secure'))
    
    amount = float(request.form.get('amount', 0))
    recipient = request.form.get('recipient', '')
    
    if amount > 0:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('UPDATE users SET balance = balance - ? WHERE id = ?', (amount, session['user_id']))
        cursor.execute('UPDATE users SET balance = balance + ? WHERE username = ?', (amount, recipient))
        
        conn.commit()
        conn.close()
        
        flash(f'Transferred ${amount} to {recipient}', 'success')
    
    return redirect(url_for('csrf.secure'))
