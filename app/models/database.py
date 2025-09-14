import sqlite3
import os

DATABASE = 'cyber_lab.db'

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with tables"""
    if os.path.exists(DATABASE):
        return
    
    conn = get_db_connection()
    
    # Create users table
    conn.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT,
            role TEXT DEFAULT 'user',
            balance REAL DEFAULT 1000.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create comments table for XSS demo
    conn.execute('''
        CREATE TABLE comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Create uploaded_files table
    conn.execute('''
        CREATE TABLE uploaded_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            original_filename TEXT NOT NULL,
            upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Create firewall_rules table for network security module
    conn.execute('''
        CREATE TABLE firewall_rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            action TEXT NOT NULL CHECK(action IN ('ALLOW', 'DENY', 'LOG')),
            source_ip TEXT,
            dest_ip TEXT,
            port_range TEXT,
            protocol TEXT,
            priority INTEGER,
            enabled BOOLEAN DEFAULT 1,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insert default users
    from werkzeug.security import generate_password_hash
    
    conn.execute("INSERT INTO users (username, password_hash, email, role) VALUES (?, ?, ?, ?)",
                ('admin', generate_password_hash('admin123'), 'admin@example.com', 'admin'))
    conn.execute("INSERT INTO users (username, password_hash, email, role) VALUES (?, ?, ?, ?)",
                ('testuser', generate_password_hash('password'), 'user@example.com', 'user'))
    conn.execute("INSERT INTO users (username, password_hash, email, role) VALUES (?, ?, ?, ?)",
                ('john', generate_password_hash('weak'), 'john@example.com', 'user'))
    
    # Insert sample comments
    conn.execute("INSERT INTO comments (user_id, content) VALUES (?, ?)",
                (1, 'Welcome to OS³: Open Source Security Studio!'))
    conn.execute("INSERT INTO comments (user_id, content) VALUES (?, ?)",
                (2, 'This is a great learning platform for cybersecurity education.'))
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")
