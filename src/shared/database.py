import sqlite3
import os

def init_db():
    # Create database file if it does not exist
    db_path = os.path.join(os.path.dirname(__file__), 'users.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    
    # Add test user
    cursor.execute('INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)', 
                   ('user', 'password'))
    
    conn.commit()
    conn.close()

def get_user(username):
    db_path = os.path.join(os.path.dirname(__file__), 'users.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user

if __name__ == '__main__':
    init_db()
