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
        last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        is_active BOOLEAN DEFAULT 1,
               locked_flg char(1) DEFAULT 'N',
        failed_login_attempts INTEGER DEFAULT 0,
        last_failed_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
               pancard_number TEXT UNIQUE,
        aadhar_number TEXT UNIQUE,
        mobile_number TEXT UNIQUE,
        address TEXT,
        city TEXT,
        state TEXT,
        country TEXT,
        zip_code TEXT
    )
''')

# Insert sample user
cursor.execute('''
    INSERT INTO users (username, password, dateofbirth, email, pancard_number, aadhar_number, mobile_number, address, city, state, country, zip_code)
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
''')
conn.commit()
conn.close()

print("Table 'users' created and sample user inserted successfully.")