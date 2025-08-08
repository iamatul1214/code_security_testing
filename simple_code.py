from flask import Flask, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecret' 

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')

    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    c.execute(f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')")
    conn.commit()
    conn.close()

    return f"User {username} registered."

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    c.execute(f"SELECT * FROM users WHERE username='{username}' AND password='{password}'")
    user = c.fetchone()
    conn.close()

    if user:
        session['user'] = username
        return f"Welcome {username}!"
    else:
        return "Invalid credentials", 401

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return f"Dashboard for {session['user']}"
    else:
        return redirect('/login')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
