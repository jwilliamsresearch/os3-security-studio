from flask import Blueprint, render_template, request, session, flash
import bleach
from ..models.database import get_db_connection

xss_bp = Blueprint('xss', __name__)

@xss_bp.route('/')
def index():
    return render_template('xss/index.html')

@xss_bp.route('/insecure', methods=['GET', 'POST'])
def insecure():
    if request.method == 'POST':
        comment = request.form.get('comment', '')
        user_id = session.get('user_id', 1)  # Default to user 1 if not logged in
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO comments (user_id, content) VALUES (?, ?)', (user_id, comment))
        conn.commit()
        conn.close()
        
        flash('Comment added!', 'success')
    
    # Get all comments
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT c.content, u.username, c.created_at 
        FROM comments c 
        JOIN users u ON c.user_id = u.id 
        ORDER BY c.created_at DESC
    ''')
    comments = cursor.fetchall()
    conn.close()
    
    return render_template('xss/insecure.html', comments=comments)

@xss_bp.route('/secure', methods=['GET', 'POST'])
def secure():
    if request.method == 'POST':
        comment = request.form.get('comment', '')
        # SECURE: Sanitize input
        comment = bleach.clean(comment, tags=['b', 'i', 'em', 'strong'], strip=True)
        user_id = session.get('user_id', 1)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO comments (user_id, content) VALUES (?, ?)', (user_id, comment))
        conn.commit()
        conn.close()
        
        flash('Comment added!', 'success')
    
    # Get all comments
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT c.content, u.username, c.created_at 
        FROM comments c 
        JOIN users u ON c.user_id = u.id 
        ORDER BY c.created_at DESC
    ''')
    comments = cursor.fetchall()
    conn.close()
    
    return render_template('xss/secure.html', comments=comments)
