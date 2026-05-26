import sqlite3

conn = sqlite3.connect("db.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM users")
print(cursor.fetchall())

def dell():
    cursor.execute("DELETE FROM users")
    cursor.execute("SELECT * FROM users")
    print(cursor.fetchall())

# dell()