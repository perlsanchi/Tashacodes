from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session

def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

def generate_10_digit_number():
    return random.randint(1000000000, 9999999999)

def generate_otp():
    return str(random.randint(100000, 999999))

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
        # Save user data in session
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        session['email'] = request.form['email']
        session['mobile_number'] = request.form.get('mobile_number')
        return redirect(url_for('signup_step2'))
    return render_template('signup.html')

@app.route('/signup_step2', methods=['GET', 'POST'])
def signup_step2():
    if request.method == 'POST':
        session['address'] = request.form['address']
        session['city'] = request.form['city']

        # Generate and store OTP
        otp = generate_otp()
        session['otp'] = otp
        print(f"DEBUG OTP (simulate sending SMS): {otp}")  # In production, send via SMS

        return redirect(url_for('verify_otp'))
    return render_template('signup_step2.html')

@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        entered_otp = request.form['otp']
        if entered_otp == session.get('otp'):
            # OTP verified, insert into DB
            conn = get_db_connection()
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    INSERT INTO users (username, password, email, mobile_number, match_id, address, city)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    session['username'], session['password'], session['email'],
                    session['mobile_number'], generate_10_digit_number(),
                    session['address'], session['city']
                ))
                conn.commit()
                username = session['username']
                session.clear()
                return f"User {username} created successfully!"
            except sqlite3.IntegrityError:
                return "Username or email already exists. Please use another ID."
            finally:
                conn.close()
        else:
            return render_template('verify_otp.html', error="Invalid OTP. Please try again.")
    return render_template('verify_otp.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
