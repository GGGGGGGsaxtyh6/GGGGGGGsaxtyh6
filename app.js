// App State
let currentUser = null;
let users = JSON.parse(localStorage.getItem('users')) || [];
let posts = JSON.parse(localStorage.getItem('posts')) || [];
let todos = JSON.parse(localStorage.getItem('todos')) || [];
let messages = JSON.parse(localStorage.getItem('messages')) || [];

// Initialize demo user if no users exist
if (users.length === 0) {
    users.push({
        id: Date.now(),
        username: 'demo',
        email: 'demo@example.com',
        password: 'demo123',
        bio: 'Usuario de demostración',
        avatarColor: '#667eea',
        createdAt: new Date().toISOString()
    });
    localStorage.setItem('users', JSON.stringify(users));
}

// Auth Functions
function showTab(tab) {
    const tabs = document.querySelectorAll('.tab-btn');
    const forms = document.querySelectorAll('.auth-form');
    
    tabs.forEach(t => t.classList.remove('active'));
    forms.forEach(f => f.classList.remove('active'));
    
    if (tab === 'login') {
        tabs[0].classList.add('active');
        document.getElementById('loginForm').classList.add('active');
    } else {
        tabs[1].classList.add('active');
        document.getElementById('registerForm').classList.add('active');
    }
}

function handleLogin(event) {
    event.preventDefault();
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;
    
    const user = users.find(u => u.username === username && u.password === password);
    
    if (user) {
        currentUser = user;
        localStorage.setItem('currentUser', JSON.stringify(user));
        showNotification('¡Bienvenido de nuevo, ' + user.username + '!', 'success');
        showApp();
    } else {
        showNotification('Usuario o contraseña incorrectos', 'error');
    }
}

function handleRegister(event) {
    event.preventDefault();
    const username = document.getElementById('regUsername').value;
    const email = document.getElementById('regEmail').value;
    const password = document.getElementById('regPassword').value;
    
    if (users.find(u => u.username === username)) {
        showNotification('El usuario ya existe', 'error');
        return;
    }
    
    const colors = ['#667eea', '#f56565', '#48bb78', '#ed8936', '#9f7aea', '#38b2ac'];
    const newUser = {
        id: Date.now(),
        username: username,
        email: email,
        password: password,
        bio: '',
        avatarColor: colors[Math.floor(Math.random() * colors.length)],
        createdAt: new Date().toISOString()
    };
    
    users.push(newUser);
    localStorage.setItem('users', JSON.stringify(users));
    showNotification('¡Cuenta creada exitosamente!', 'success');
    showTab('login');
}

function logout() {
    currentUser = null;
    localStorage.removeItem('currentUser');
    document.getElementById('authScreen').style.display = 'flex';
    document.getElementById('mainApp').style.display = 'none';
    showNotification('Sesión cerrada', 'success');
}

// App Functions
function showApp() {
    document.getElementById('authScreen').style.display = 'none';
    document.getElementById('mainApp').style.display = 'flex';
    
    // Update user info
    document.getElementById('userAvatar').textContent = currentUser.username[0].toUpperCase();
    document.getElementById('userAvatar').style.background = currentUser.avatarColor;
    document.getElementById('userName').textContent = currentUser.username;
    
    // Load dashboard
    showSection('dashboard');
    updateDashboard();
}

function showSection(section) {
    // Update nav
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
        if (item.textContent.toLowerCase().includes(section) || 
            (section === 'dashboard' && item.textContent.includes('Dashboard'))) {
            item.classList.add('active');
        }
    });
    
    // Update sections
    document.querySelectorAll('.content-section').forEach(s => {
        s.classList.remove('active');
    });
    document.getElementById(section).classList.add('active');
    
    // Load section data
    if (section === 'dashboard') updateDashboard();
    if (section === 'posts') loadPosts();
    if (section === 'todos') loadTodos();
    if (section === 'profile') loadProfile();
    if (section === 'chat') loadChat();
}

// Dashboard
function updateDashboard() {
    const userPosts = posts.filter(p => p.userId === currentUser.id);
    const userTodos = todos.filter(t => t.userId === currentUser.id);
    const completedTodos = userTodos.filter(t => t.completed);
    
    document.getElementById('totalPosts').textContent = userPosts.length;
    document.getElementById('totalTodos').textContent = userTodos.length;
    document.getElementById('completedTodos').textContent = completedTodos.length;
    document.getElementById('userCount').textContent = users.length;
    
    // Recent posts
    const recentPostsHtml = posts.slice(-5).reverse().map(post => {
        const author = users.find(u => u.id === post.userId);
        return `
            <div class="recent-item">
                <strong>${post.title}</strong>
                <div style="color: #718096; font-size: 14px;">
                    Por ${author ? author.username : 'Usuario'} • ${formatDate(post.createdAt)}
                </div>
            </div>
        `;
    }).join('');
    document.getElementById('recentPosts').innerHTML = recentPostsHtml || '<p style="color: #a0aec0;">No hay posts aún</p>';
    
    // Pending todos
    const pendingTodosHtml = userTodos.filter(t => !t.completed).slice(0, 5).map(todo => `
        <div class="recent-item">
            <div>${todo.text}</div>
            <span class="todo-priority priority-${todo.priority}">${todo.priority}</span>
        </div>
    `).join('');
    document.getElementById('pendingTodos').innerHTML = pendingTodosHtml || '<p style="color: #a0aec0;">No hay tareas pendientes</p>';
}

// Posts
function showCreatePost() {
    document.getElementById('createPostForm').style.display = 'block';
}

function hideCreatePost() {
    document.getElementById('createPostForm').style.display = 'none';
    document.getElementById('postTitle').value = '';
    document.getElementById('postContent').value = '';
}

function createPost() {
    const title = document.getElementById('postTitle').value;
    const content = document.getElementById('postContent').value;
    
    if (!title || !content) {
        showNotification('Por favor completa todos los campos', 'error');
        return;
    }
    
    const newPost = {
        id: Date.now(),
        userId: currentUser.id,
        title: title,
        content: content,
        likes: 0,
        likedBy: [],
        createdAt: new Date().toISOString()
    };
    
    posts.push(newPost);
    localStorage.setItem('posts', JSON.stringify(posts));
    showNotification('Post publicado exitosamente', 'success');
    hideCreatePost();
    loadPosts();
}

function loadPosts() {
    const postsHtml = posts.slice().reverse().map(post => {
        const author = users.find(u => u.id === post.userId);
        const isLiked = post.likedBy && post.likedBy.includes(currentUser.id);
        return `
            <div class="post-card">
                <div class="post-header">
                    <div class="post-author">
                        <div class="post-avatar" style="background: ${author ? author.avatarColor : '#667eea'}">
                            ${author ? author.username[0].toUpperCase() : 'U'}
                        </div>
                        <div>
                            <div class="post-author-name">${author ? author.username : 'Usuario'}</div>
                            <div class="post-date">${formatDate(post.createdAt)}</div>
                        </div>
                    </div>
                </div>
                <div class="post-title">${post.title}</div>
                <div class="post-content">${post.content}</div>
                <div class="post-actions">
                    <button class="post-action ${isLiked ? 'liked' : ''}" onclick="likePost(${post.id})">
                        <i class="ri-heart-${isLiked ? 'fill' : 'line'}"></i>
                        <span>${post.likes}</span>
                    </button>
                    <button class="post-action">
                        <i class="ri-chat-1-line"></i>
                        Comentar
                    </button>
                    <button class="post-action">
                        <i class="ri-share-line"></i>
                        Compartir
                    </button>
                </div>
            </div>
        `;
    }).join('');
    
    document.getElementById('postsList').innerHTML = postsHtml || '<p style="text-align: center; color: #a0aec0;">No hay posts aún. ¡Sé el primero en publicar!</p>';
}

function likePost(postId) {
    const post = posts.find(p => p.id === postId);
    if (!post) return;
    
    if (!post.likedBy) post.likedBy = [];
    
    const index = post.likedBy.indexOf(currentUser.id);
    if (index > -1) {
        post.likedBy.splice(index, 1);
        post.likes--;
    } else {
        post.likedBy.push(currentUser.id);
        post.likes++;
    }
    
    localStorage.setItem('posts', JSON.stringify(posts));
    loadPosts();
}

// Todos
function addTodo() {
    const text = document.getElementById('todoInput').value;
    const priority = document.getElementById('todoPriority').value;
    
    if (!text) {
        showNotification('Por favor escribe una tarea', 'error');
        return;
    }
    
    const newTodo = {
        id: Date.now(),
        userId: currentUser.id,
        text: text,
        priority: priority,
        completed: false,
        createdAt: new Date().toISOString()
    };
    
    todos.push(newTodo);
    localStorage.setItem('todos', JSON.stringify(todos));
    document.getElementById('todoInput').value = '';
    showNotification('Tarea añadida', 'success');
    loadTodos();
}

let currentFilter = 'all';

function filterTodos(filter) {
    currentFilter = filter;
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.textContent.toLowerCase().includes(filter) || 
            (filter === 'all' && btn.textContent === 'Todas')) {
            btn.classList.add('active');
        }
    });
    loadTodos();
}

function loadTodos() {
    let userTodos = todos.filter(t => t.userId === currentUser.id);
    
    if (currentFilter === 'pending') {
        userTodos = userTodos.filter(t => !t.completed);
    } else if (currentFilter === 'completed') {
        userTodos = userTodos.filter(t => t.completed);
    }
    
    const todosHtml = userTodos.map(todo => `
        <div class="todo-item">
            <input type="checkbox" class="todo-checkbox" ${todo.completed ? 'checked' : ''} 
                   onchange="toggleTodo(${todo.id})">
            <div class="todo-content">
                <div class="todo-text ${todo.completed ? 'completed' : ''}">${todo.text}</div>
                <span class="todo-priority priority-${todo.priority}">${todo.priority}</span>
            </div>
            <div class="todo-actions">
                <button class="btn-delete" onclick="deleteTodo(${todo.id})">
                    <i class="ri-delete-bin-line"></i>
                </button>
            </div>
        </div>
    `).join('');
    
    document.getElementById('todosList').innerHTML = todosHtml || '<p style="text-align: center; color: #a0aec0;">No hay tareas</p>';
}

function toggleTodo(todoId) {
    const todo = todos.find(t => t.id === todoId);
    if (todo) {
        todo.completed = !todo.completed;
        localStorage.setItem('todos', JSON.stringify(todos));
        loadTodos();
        updateDashboard();
    }
}

function deleteTodo(todoId) {
    todos = todos.filter(t => t.id !== todoId);
    localStorage.setItem('todos', JSON.stringify(todos));
    showNotification('Tarea eliminada', 'success');
    loadTodos();
    updateDashboard();
}

// Profile
function loadProfile() {
    document.getElementById('profileAvatar').textContent = currentUser.username[0].toUpperCase();
    document.getElementById('profileAvatar').style.background = currentUser.avatarColor;
    document.getElementById('profileName').textContent = currentUser.username;
    document.getElementById('profileEmail').textContent = currentUser.email;
    document.getElementById('memberSince').textContent = new Date(currentUser.createdAt).getFullYear();
    document.getElementById('bio').value = currentUser.bio || '';
    document.getElementById('avatarColor').value = currentUser.avatarColor;
    
    const userPosts = posts.filter(p => p.userId === currentUser.id);
    const userTodos = todos.filter(t => t.userId === currentUser.id);
    const days = Math.floor((new Date() - new Date(currentUser.createdAt)) / (1000 * 60 * 60 * 24));
    
    document.getElementById('profilePostCount').textContent = userPosts.length;
    document.getElementById('profileTodoCount').textContent = userTodos.length;
    document.getElementById('profileDays').textContent = days;
}

function updateProfile() {
    currentUser.bio = document.getElementById('bio').value;
    currentUser.avatarColor = document.getElementById('avatarColor').value;
    
    const userIndex = users.findIndex(u => u.id === currentUser.id);
    if (userIndex !== -1) {
        users[userIndex] = currentUser;
        localStorage.setItem('users', JSON.stringify(users));
        localStorage.setItem('currentUser', JSON.stringify(currentUser));
    }
    
    document.getElementById('userAvatar').style.background = currentUser.avatarColor;
    document.getElementById('profileAvatar').style.background = currentUser.avatarColor;
    
    showNotification('Perfil actualizado', 'success');
}

// Chat
function loadChat() {
    const chatHtml = messages.map(msg => {
        const author = users.find(u => u.id === msg.userId);
        const isOwn = msg.userId === currentUser.id;
        return `
            <div class="chat-message ${isOwn ? 'own' : ''}">
                <div class="message-header">
                    <div class="message-avatar" style="background: ${author ? author.avatarColor : '#667eea'}">
                        ${author ? author.username[0].toUpperCase() : 'U'}
                    </div>
                    <span class="message-author">${author ? author.username : 'Usuario'}</span>
                    <span class="message-time">${formatTime(msg.createdAt)}</span>
                </div>
                <div class="message-content">${msg.text}</div>
            </div>
        `;
    }).join('');
    
    const chatMessages = document.getElementById('chatMessages');
    chatMessages.innerHTML = chatHtml || '<p style="text-align: center; color: #a0aec0; padding: 50px;">No hay mensajes aún. ¡Inicia la conversación!</p>';
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function sendMessage() {
    const text = document.getElementById('messageInput').value;
    
    if (!text) return;
    
    const newMessage = {
        id: Date.now(),
        userId: currentUser.id,
        text: text,
        createdAt: new Date().toISOString()
    };
    
    messages.push(newMessage);
    localStorage.setItem('messages', JSON.stringify(messages));
    document.getElementById('messageInput').value = '';
    loadChat();
}

// Enter key for chat
document.addEventListener('DOMContentLoaded', function() {
    const messageInput = document.getElementById('messageInput');
    if (messageInput) {
        messageInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }
});

// Notifications
function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <i class="ri-${type === 'success' ? 'checkbox-circle' : 'error-warning'}-line"></i>
        <span>${message}</span>
    `;
    
    document.getElementById('notifications').appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Utility Functions
function formatDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diff = now - date;
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    
    if (days === 0) return 'Hoy';
    if (days === 1) return 'Ayer';
    if (days < 7) return `Hace ${days} días`;
    
    return date.toLocaleDateString('es-ES', { day: 'numeric', month: 'short', year: 'numeric' });
}

function formatTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' });
}

// Check if user is logged in
window.addEventListener('load', function() {
    const savedUser = localStorage.getItem('currentUser');
    if (savedUser) {
        currentUser = JSON.parse(savedUser);
        showApp();
    }
});

// Animation for notification
const style = document.createElement('style');
style.innerHTML = `
    @keyframes slideOut {
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);