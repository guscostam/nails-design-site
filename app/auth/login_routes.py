from flask import Blueprint, render_template, request, redirect, url_for, session
import sqlite3

login_bp = Blueprint('login', __name__)

def get_name(email):
    conn = sqlite3.connect('data/clients.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM clients WHERE email=?', (email,))
    result = cursor.fetchone()
    conn.close()

    if result:
        name = result[0]
        return name.strip("(),' ")
    else:
        return None
    
def check_login(email, password):
    conn = sqlite3.connect('data/clients.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients WHERE email=? AND password=?', (email, password))
    user = cursor.fetchone()
    conn.close()
    return user

@login_bp.route('/')
def index_login():
    return render_template('login.html')

@login_bp.route('/forgot-password')
def forgot_password():
    return render_template('forgot_password.html')

@login_bp.route('/sign-up')
def sign_up():
    return render_template('sign-up.html')

@login_bp.route('/login', methods=['POST'])
def auth():
    username = request.form['username']
    password = request.form['password']
    user = check_login(username, password)
    if user:
        session['username'] = username
        return redirect(url_for('login.dashboard'))
    else:
        return f'<script>alert("Credenciais inválidas. Tente novamente."); window.location.href = "/";</script>', 400
   
@login_bp.route('/dashboard')
def dashboard():
    if 'username' in session:
        username = session['username']
        name = get_name(username)
        return render_template('system_index.html', name=name)
    else:
        return redirect(url_for('login.index_login'))

@login_bp.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login.index_login'))
