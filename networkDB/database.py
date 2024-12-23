import sqlite3

def init_db():
    conn = sqlite3.connect('home_network.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS device_logs (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            device TEXT NOT NULL,
            date_of_use DATE NOT NULL,
            time_of_use TIME NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')
    conn.commit()
    conn.close()

def add_user(username):
    conn = sqlite3.connect('home_network.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (username) VALUES (?)
    ''', (username,))
    conn.commit()
    conn.close()

def log_device_use(user_id, device, date_of_use, time_of_use):
    conn = sqlite3.connect('home_network.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO device_logs (user_id, device, date_of_use, time_of_use)
        VALUES (?, ?, ?, ?)
    ''', (user_id, device, date_of_use, time_of_use))
    conn.commit()
    conn.close()

def get_users():
    conn = sqlite3.connect('home_network.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    return users

def get_logs():
    conn = sqlite3.connect('home_network.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM device_logs')
    logs = cursor.fetchall()
    conn.close()
    return logs

if __name__ == '__main__':
    init_db()
