import sqlite3

def init_db():
    conn = sqlite3.connect('xbox_usage.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            username TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gameplay_logs (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            game_title TEXT NOT NULL,
            duration INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_logs (
            chat_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')
    conn.commit()
    conn.close()

def add_user(user_id, username):
    conn = sqlite3.connect('xbox_usage.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (user_id, username) VALUES (?, ?)
    ''', (user_id, username))
    conn.commit()
    conn.close()

def log_gameplay(user_id, game_title, duration, timestamp):
    conn = sqlite3.connect('xbox_usage.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO gameplay_logs (user_id, game_title, duration, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (user_id, game_title, duration, timestamp))
    conn.commit()
    conn.close()

def log_chat(user_id, message, timestamp):
    conn = sqlite3.connect('xbox_usage.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO chat_logs (user_id, message, timestamp)
        VALUES (?, ?, ?)
    ''', (user_id, message, timestamp))
    conn.commit()
    conn.close()

def get_users():
    conn = sqlite3.connect('xbox_usage.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    return users

def get_gameplay_logs():
    conn = sqlite3.connect('xbox_usage.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM gameplay_logs')
    logs = cursor.fetchall()
    conn.close()
    return logs

def get_chat_logs():
    conn = sqlite3.connect('xbox_usage.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM chat_logs')
    logs = cursor.fetchall()
    conn.close()
    return logs

if __name__ == '__main__':
    init_db()
