from flask import Blueprint, render_template, session, flash, redirect, url_for
from ..models.database import get_db_connection
from ..utils.auth import login_required

access_control_bp = Blueprint('access_control', __name__)

@access_control_bp.route('/')
def index():
    return render_template('access_control/index.html')

@access_control_bp.route('/insecure/<int:user_id>')
@login_required
def insecure(user_id):
    # INSECURE: No authorization check
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT username, email, balance FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return render_template('access_control/insecure.html', user=user, user_id=user_id)
    else:
        flash('User not found!', 'danger')
        return redirect(url_for('access_control.index'))

@access_control_bp.route('/secure/<int:user_id>')
@login_required
def secure(user_id):
    # SECURE: Check if user can access this profile
    if session['user_id'] != user_id:
        flash('Access denied! You can only view your own profile.', 'danger')
        return redirect(url_for('access_control.index'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT username, email, balance FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return render_template('access_control/secure.html', user=user, user_id=user_id)
    else:
        flash('User not found!', 'danger')
        return redirect(url_for('access_control.index'))

@access_control_bp.route('/admin-panel')
def admin_panel():
    from ..utils.auth import admin_required
    
    @admin_required
    def _admin_panel():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, username, email, role, balance FROM users')
        users = cursor.fetchall()
        conn.close()
        
        return render_template('admin_panel.html', users=users)
    
    return _admin_panel()
