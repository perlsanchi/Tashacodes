from flask import Flask, render_template, request
import sqlite3
import random

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row  # To access columns by name
    return conn

@app.route('/')
def login_form():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        return f"Welcome, {user['username']}! Your email is {user['email']}."
    else:
        return render_template('index.html', error = "Invalid username or password. Please try again OR Sign up on <a href = /signup>Sign Up</a> page.")
    
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        mobile_number = request.form.get('mobile_number', None)

        
        conn = get_db_connection()
        cursor = conn.cursor()
        num = generate_10_digit_number()
        
        try:
            cursor.execute('''
                INSERT INTO users (username, password, email,mobile_number, match_id)
                VALUES (?, ?, ?,?,?)
            ''', (username, password, email, mobile_number,num))
            conn.commit()
            return f"User {username} created successfully!"
        except sqlite3.IntegrityError:
            return render_template('signup.html', error="Username or email already exists.")
        finally:
            conn.close()
    
    return render_template('signup.html')

def generate_10_digit_number():
    return random.randint(1000000000, 9999999999)

if __name__ == '__main__':
    app.run(debug=True, port = 5001)
