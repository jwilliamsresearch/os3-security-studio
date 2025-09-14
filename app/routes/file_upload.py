from flask import Blueprint, render_template, request, session, flash, redirect, url_for, current_app
from werkzeug.utils import secure_filename
import os
import time
from ..models.database import get_db_connection
from ..utils.auth import login_required

file_upload_bp = Blueprint('file_upload', __name__)

@file_upload_bp.route('/')
def index():
    return render_template('file_upload/index.html')

@file_upload_bp.route('/insecure', methods=['GET', 'POST'])
@login_required
def insecure():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected!', 'danger')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected!', 'danger')
            return redirect(request.url)
        
        # INSECURE: No file type validation, direct filename usage
        filename = file.filename
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Save to database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO uploaded_files (user_id, filename, original_filename) VALUES (?, ?, ?)',
                      (session['user_id'], filename, filename))
        conn.commit()
        conn.close()
        
        flash(f'File {filename} uploaded successfully! (Insecure)', 'warning')
    
    # Get user's files
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT filename, original_filename, upload_time FROM uploaded_files WHERE user_id = ?', 
                  (session['user_id'],))
    files = cursor.fetchall()
    conn.close()
    
    return render_template('file_upload/insecure.html', files=files)

@file_upload_bp.route('/secure', methods=['GET', 'POST'])
@login_required
def secure():
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}
    
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected!', 'danger')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected!', 'danger')
            return redirect(request.url)
        
        if not allowed_file(file.filename):
            flash('File type not allowed!', 'danger')
            return redirect(request.url)
        
        # SECURE: Use secure filename and validate file type
        original_filename = file.filename
        filename = secure_filename(original_filename)
        
        # Add timestamp to prevent filename conflicts
        timestamp = str(int(time.time()))
        name, ext = os.path.splitext(filename)
        filename = f"{name}_{timestamp}{ext}"
        
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Save to database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO uploaded_files (user_id, filename, original_filename) VALUES (?, ?, ?)',
                      (session['user_id'], filename, original_filename))
        conn.commit()
        conn.close()
        
        flash(f'File {original_filename} uploaded securely!', 'success')
    
    # Get user's files
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT filename, original_filename, upload_time FROM uploaded_files WHERE user_id = ?', 
                  (session['user_id'],))
    files = cursor.fetchall()
    conn.close()
    
    return render_template('file_upload/secure.html', files=files)
