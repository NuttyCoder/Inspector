import sqlite3

def init_db():
    conn = sqlite3.connect('homenet.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS devices (
            device_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            device_name TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            action TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')
    conn.commit()
    conn.close()

def add_user(username, password, role):
    conn = sqlite3.connect('homenet.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (username, password, role) VALUES (?, ?, ?)
    ''', (username, password, role))
    conn.commit()
    conn.close()

def get_users():
    conn = sqlite3.connect('homenet.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    return users

def log_action(user_id, action):
    conn = sqlite3.connect('homenet.db')
    cursor = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        INSERT INTO logs (user_id, action, timestamp) VALUES (?, ?, ?)
    ''', (user_id, action, timestamp))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
