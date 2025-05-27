import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

cursor.execute('select * from  users')
rows = cursor.fetchall()
conn.commit()

for row in rows:
    print(row)

conn.close()

  