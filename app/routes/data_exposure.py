from flask import Blueprint, render_template
from ..models.database import get_db_connection

data_exposure_bp = Blueprint('data_exposure', __name__)

@data_exposure_bp.route('/')
def index():
    return render_template('data_exposure/index.html')

@data_exposure_bp.route('/insecure')
def insecure():
    # INSECURE: Expose sensitive data in response
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT username, password_hash, email FROM users')
    users = cursor.fetchall()
    conn.close()
    
    return render_template('data_exposure/insecure.html', users=users)

@data_exposure_bp.route('/secure')
def secure():
    # SECURE: Only expose necessary data
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT username, email FROM users')
    users = cursor.fetchall()
    conn.close()
    
    return render_template('data_exposure/secure.html', users=users)
