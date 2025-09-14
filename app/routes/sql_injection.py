from flask import Blueprint, render_template, request
import sqlite3
from ..models.database import get_db_connection

sql_injection_bp = Blueprint('sql_injection', __name__)

@sql_injection_bp.route('/')
def index():
    return render_template('sql_injection/index.html')

@sql_injection_bp.route('/insecure', methods=['GET', 'POST'])
def insecure():
    results = []
    query = ""
    error = ""
    
    if request.method == 'POST':
        query = request.form.get('query', '')
        if query:
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                # VULNERABLE: Direct string concatenation
                sql = f"SELECT username, email, role FROM users WHERE username LIKE '%{query}%'"
                cursor.execute(sql)
                results = cursor.fetchall()
                conn.close()
            except Exception as e:
                error = str(e)
    
    return render_template('sql_injection/insecure.html', results=results, query=query, error=error)

@sql_injection_bp.route('/secure', methods=['GET', 'POST'])
def secure():
    results = []
    query = ""
    error = ""
    
    if request.method == 'POST':
        query = request.form.get('query', '')
        if query:
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                # SECURE: Parameterized query
                sql = "SELECT username, email, role FROM users WHERE username LIKE ?"
                cursor.execute(sql, (f'%{query}%',))
                results = cursor.fetchall()
                conn.close()
            except Exception as e:
                error = str(e)
    
    return render_template('sql_injection/secure.html', results=results, query=query, error=error)
