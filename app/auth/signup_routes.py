from flask import Blueprint, request
import sqlite3
import dns.resolver

signup_bp = Blueprint('signup', __name__)

def create_client_db(username):
    db_name = f'user_{username}.db'
    conn = sqlite3.connect(f'data/{db_name}')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS clients (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        last_name TEXT,
                        email TEXT,
                        phone TEXT,
                        address TEXT
                        )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY,
                    product_name TEXT,
                    product_price REAL,
                    product_size TEXT,
                    product_color TEXT
                    )''')

    conn.commit()
    conn.close()

def check_email_existence(email):
    try:
        domain = email.split('@')[1]
        mx_records = dns.resolver.resolve(domain, 'MX')
        return len(mx_records) > 0
    except Exception:
        return False
    
def is_valid_email(email):
    if check_email_existence(email):
        return True
    else:
        return False

@signup_bp.route('/sign-up', methods=['POST'])
def client_signup():
    name = request.form['sign-up name'].capitalize()
    lastname = request.form['sign-up lastname'].capitalize()
    email = request.form['sign-up email'].lower()
    password = request.form['sign-up password']
    confirm_password = request.form['sign-up confirm-password']

    if password != confirm_password:
        return f'<script>alert("As senhas não coincidem. Tente novamente."); window.location.href = "/sign-up";</script>', 400
    
    conn = sqlite3.connect('data/clients.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clients WHERE email=?", (email,))
    existing_user = cursor.fetchone()

    if existing_user:
        return f'<script>alert("O email já está cadastrado. Por favor, use outro email."); window.location.href = "/sign-up";</script>', 400

    if is_valid_email(email):
        cursor.execute("INSERT INTO clients (name, lastname, email, password) VALUES (?, ?, ?, ?)", (name, lastname, email, password))
        conn.commit()
        conn.close()

        create_client_db(email)

        return f'<script>alert("Cadastrado feito com sucesso!"); window.location.href = "/";</script>'
    else:
        return f'<script>alert("O email digitado não é válido."); window.location.href = "/sign-up";</script>', 
