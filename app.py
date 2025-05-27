from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required to use session

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
        return render_template('index.html', error="Invalid username or password. Please try again OR Sign up on <a href='/signup'>Sign Up</a> page.")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Save first form data in session
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        session['email'] = request.form['email']
        session['mobile_number'] = request.form.get('mobile_number')
        return redirect(url_for('signup_step2'))
    return render_template('signup.html')

@app.route('/signup_step2', methods=['GET', 'POST'])
def signup_step2():
    if request.method == 'POST':
        address = request.form['address']
        city = request.form['city']

        # Retrieve session data
        username = session.get('username')
        password = session.get('password')
        email = session.get('email')
        mobile_number = session.get('mobile_number')
        match_id = generate_10_digit_number()

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO users (username, password, email, mobile_number, match_id, address, city)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (username, password, email, mobile_number, match_id, address, city))
            conn.commit()
            # Clear session data after insertion
            session.clear()
            return f"User {username} created successfully!"
        except sqlite3.IntegrityError:
            return "Username or email already exists."
        finally:
            conn.close()
    return render_template('signup_step2.html')

def generate_10_digit_number():
    return random.randint(1000000000, 9999999999)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
