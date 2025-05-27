import sqlite3

# Connect or create the database
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        dateofbirth DATE,
        email TEXT UNIQUE,
        insert_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        is_active BOOLEAN DEFAULT 1,
        locked_flg CHAR(1) DEFAULT 'N',
        failed_login_attempts INTEGER DEFAULT 0,
        last_failed_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        match_id TEXT UNIQUE,
        aadhar_number TEXT UNIQUE,
        mobile_number TEXT UNIQUE,
        address TEXT,
        city TEXT,
        state TEXT,
        country TEXT,
        zip_code TEXT
    )
''')

# Insert sample user with all fields
cursor.execute('''
    INSERT INTO users (
        username, password, dateofbirth, email,
        match_id, aadhar_number, mobile_number,
        address, city, state, country, zip_code
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', (
    'admin', '1234', '1995-06-15', 'admin@example.com',
    'ABCDE1234F', '123412341234', '9876543210',
    '123 Admin Street', 'Mumbai', 'Maharashtra', 'India', '400001'
))

conn.commit()
conn.close()

print("Table 'users' created and sample user inserted successfully.")
