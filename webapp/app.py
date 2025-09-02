#!/usr/bin/env python3
"""
Aplicación Web Dinámica con Sistema de Autenticación
Creada con Flask, SQLAlchemy y SQLite
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
import secrets

# Configuración de la aplicación
app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

# Inicializar extensiones
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor, inicia sesión para acceder a esta página.'
login_manager.login_message_category = 'info'

# Modelos de Base de Datos
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    bio = db.Column(db.Text, default='')
    avatar_color = db.Column(db.String(7), default='#667eea')
    posts = db.relationship('Post', backref='author', lazy=True, cascade='all, delete-orphan')
    todos = db.relationship('Todo', backref='user', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_stats(self):
        return {
            'posts': len(self.posts),
            'todos': len(self.todos),
            'completed_todos': len([t for t in self.todos if t.completed]),
            'days_member': (datetime.utcnow() - self.created_at).days
        }

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    likes = db.Column(db.Integer, default=0)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=True)
    priority = db.Column(db.String(20), default='medium')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Rutas de la aplicación
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validaciones
        if not all([username, email, password, confirm_password]):
            flash('Todos los campos son obligatorios', 'danger')
            return redirect(url_for('register'))
        
        if password != confirm_password:
            flash('Las contraseñas no coinciden', 'danger')
            return redirect(url_for('register'))
        
        if len(password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres', 'danger')
            return redirect(url_for('register'))
        
        # Verificar si el usuario ya existe
        if User.query.filter_by(username=username).first():
            flash('El nombre de usuario ya está en uso', 'danger')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('El email ya está registrado', 'danger')
            return redirect(url_for('register'))
        
        # Crear nuevo usuario
        colors = ['#667eea', '#f56565', '#48bb78', '#ed8936', '#9f7aea', '#38b2ac', '#ed64a6']
        new_user = User(
            username=username,
            email=email,
            avatar_color=secrets.choice(colors)
        )
        new_user.set_password(password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('¡Registro exitoso! Por favor, inicia sesión.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('Error al crear la cuenta. Por favor, intenta de nuevo.', 'danger')
            return redirect(url_for('register'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember') == 'on'
        
        if not username or not password:
            flash('Por favor, completa todos los campos', 'danger')
            return redirect(url_for('login'))
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user, remember=remember)
            session.permanent = remember
            next_page = request.args.get('next')
            flash(f'¡Bienvenido de nuevo, {user.username}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión exitosamente', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    user_stats = current_user.get_stats()
    recent_posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    user_todos = Todo.query.filter_by(user_id=current_user.id, completed=False).order_by(Todo.created_at.desc()).limit(5).all()
    return render_template('dashboard.html', stats=user_stats, recent_posts=recent_posts, todos=user_todos)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@app.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    bio = request.form.get('bio', '')
    current_user.bio = bio
    
    try:
        db.session.commit()
        flash('Perfil actualizado exitosamente', 'success')
    except:
        db.session.rollback()
        flash('Error al actualizar el perfil', 'danger')
    
    return redirect(url_for('profile'))

@app.route('/posts')
@login_required
def posts():
    all_posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('posts.html', posts=all_posts)

@app.route('/posts/create', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        
        if not title or not content:
            flash('El título y contenido son obligatorios', 'danger')
            return redirect(url_for('create_post'))
        
        new_post = Post(
            title=title,
            content=content,
            user_id=current_user.id
        )
        
        try:
            db.session.add(new_post)
            db.session.commit()
            flash('Post creado exitosamente', 'success')
            return redirect(url_for('posts'))
        except:
            db.session.rollback()
            flash('Error al crear el post', 'danger')
    
    return render_template('create_post.html')

@app.route('/posts/<int:post_id>/like', methods=['POST'])
@login_required
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.likes += 1
    db.session.commit()
    return jsonify({'likes': post.likes})

@app.route('/todos')
@login_required
def todos():
    user_todos = Todo.query.filter_by(user_id=current_user.id).order_by(Todo.created_at.desc()).all()
    return render_template('todos.html', todos=user_todos)

@app.route('/todos/add', methods=['POST'])
@login_required
def add_todo():
    task = request.form.get('task')
    priority = request.form.get('priority', 'medium')
    
    if not task:
        flash('La tarea no puede estar vacía', 'danger')
        return redirect(url_for('todos'))
    
    new_todo = Todo(
        task=task,
        priority=priority,
        user_id=current_user.id
    )
    
    try:
        db.session.add(new_todo)
        db.session.commit()
        flash('Tarea añadida exitosamente', 'success')
    except:
        db.session.rollback()
        flash('Error al añadir la tarea', 'danger')
    
    return redirect(url_for('todos'))

@app.route('/todos/<int:todo_id>/toggle', methods=['POST'])
@login_required
def toggle_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    
    if todo.user_id != current_user.id:
        return jsonify({'error': 'No autorizado'}), 403
    
    todo.completed = not todo.completed
    db.session.commit()
    return jsonify({'completed': todo.completed})

@app.route('/todos/<int:todo_id>/delete', methods=['POST'])
@login_required
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    
    if todo.user_id != current_user.id:
        flash('No autorizado', 'danger')
        return redirect(url_for('todos'))
    
    try:
        db.session.delete(todo)
        db.session.commit()
        flash('Tarea eliminada', 'info')
    except:
        db.session.rollback()
        flash('Error al eliminar la tarea', 'danger')
    
    return redirect(url_for('todos'))

# API endpoints
@app.route('/api/stats')
@login_required
def api_stats():
    return jsonify(current_user.get_stats())

@app.route('/api/users')
@login_required
def api_users():
    users = User.query.all()
    return jsonify([{
        'id': u.id,
        'username': u.username,
        'posts': len(u.posts),
        'avatar_color': u.avatar_color
    } for u in users])

# Crear tablas al iniciar
def init_db():
    with app.app_context():
        db.create_all()
        
        # Crear usuario de prueba si no existe
        if not User.query.filter_by(username='demo').first():
            demo_user = User(
                username='demo',
                email='demo@example.com',
                bio='Usuario de demostración',
                avatar_color='#667eea'
            )
            demo_user.set_password('demo123')
            db.session.add(demo_user)
            
            # Añadir algunos posts de ejemplo
            sample_post = Post(
                title='¡Bienvenido a la aplicación!',
                content='Esta es una aplicación web dinámica con sistema de autenticación completo.',
                user_id=1
            )
            db.session.add(sample_post)
            
            # Añadir algunas tareas de ejemplo
            sample_todo = Todo(
                task='Explorar todas las funcionalidades',
                priority='high',
                user_id=1
            )
            db.session.add(sample_todo)
            
            db.session.commit()

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)