import scapy.all as scapy
import datetime
import sqlite3
import time
from threading import Thread
import socket
import netifaces
import psutil
import hashlib
import jwt
from collections import defaultdict

class NetworkMonitor:
    def __init__(self, db_path="network_data.db"):
        self.db_path = db_path
        self.setup_database()
        self.known_devices = {}
        self.bandwidth_stats = defaultdict(lambda: {'bytes_sent': 0, 'bytes_recv': 0})
        self.alert_subscribers = []
        
    def setup_database(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Create tables for devices and network events
        c.execute('''CREATE TABLE IF NOT EXISTS devices
                    (mac TEXT PRIMARY KEY, ip TEXT, hostname TEXT, 
                     first_seen TIMESTAMP, last_seen TIMESTAMP,
                     bytes_sent INTEGER DEFAULT 0, bytes_recv INTEGER DEFAULT 0)''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS events
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     mac TEXT, event_type TEXT, timestamp TIMESTAMP,
                     details TEXT)''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS users
                    (username TEXT PRIMARY KEY, password_hash TEXT,
                     is_admin BOOLEAN DEFAULT FALSE)''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS alerts
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     type TEXT, condition TEXT, threshold REAL,
                     is_active BOOLEAN DEFAULT TRUE)''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS bandwidth_history
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     mac TEXT, timestamp TIMESTAMP,
                     bytes_sent INTEGER, bytes_recv INTEGER)''')
        
        conn.commit()
        conn.close()
    
    def add_user(self, username, password, is_admin=False):
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password_hash, is_admin) VALUES (?, ?, ?)",
                 (username, password_hash, is_admin))
        conn.commit()
        conn.close()
    
    def verify_user(self, username, password):
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT is_admin FROM users WHERE username=? AND password_hash=?",
                 (username, password_hash))
        result = c.fetchone()
        conn.close()
        return result[0] if result else None
    
    def update_bandwidth_stats(self):
        interfaces = psutil.net_io_counters(pernic=True)
        for interface, stats in interfaces.items():
            if interface != 'lo':  # Skip loopback
                for mac, device in self.known_devices.items():
                    if device['interface'] == interface:
                        current_stats = self.bandwidth_stats[mac]
                        bytes_sent_diff = stats.bytes_sent - current_stats['bytes_sent']
                        bytes_recv_diff = stats.bytes_recv - current_stats['bytes_recv']
                        
                        if bytes_sent_diff > 0 or bytes_recv_diff > 0:
                            self.update_device_bandwidth(mac, bytes_sent_diff, bytes_recv_diff)
                        
                        current_stats['bytes_sent'] = stats.bytes_sent
                        current_stats['bytes_recv'] = stats.bytes_recv
    
    def update_device_bandwidth(self, mac, bytes_sent, bytes_recv):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Update current totals
        c.execute("""UPDATE devices 
                    SET bytes_sent = bytes_sent + ?,
                        bytes_recv = bytes_recv + ?
                    WHERE mac = ?""",
                 (bytes_sent, bytes_recv, mac))
        
        # Add to history
        c.execute("""INSERT INTO bandwidth_history 
                    (mac, timestamp, bytes_sent, bytes_recv)
                    VALUES (?, ?, ?, ?)""",
                 (mac, datetime.datetime.now(), bytes_sent, bytes_recv))
        
        conn.commit()
        conn.close()
        
        # Check bandwidth alerts
        self.check_bandwidth_alerts(mac, bytes_sent, bytes_recv)
    
    def add_alert(self, alert_type, condition, threshold):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("INSERT INTO alerts (type, condition, threshold) VALUES (?, ?, ?)",
                 (alert_type, condition, threshold))
        conn.commit()
        conn.close()
    
    def check_bandwidth_alerts(self, mac, bytes_sent, bytes_recv):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute("SELECT * FROM alerts WHERE type='bandwidth' AND is_active=1")
        alerts = c.fetchall()
        
        for alert in alerts:
            if alert['condition'] == 'upload' and bytes_sent > alert['threshold']:
                self.trigger_alert(mac, f"High upload bandwidth detected: {bytes_sent/1024/1024:.2f} MB")
            elif alert['condition'] == 'download' and bytes_recv > alert['threshold']:
                self.trigger_alert(mac, f"High download bandwidth detected: {bytes_recv/1024/1024:.2f} MB")
        
        conn.close()
    
    def trigger_alert(self, mac, message):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute("SELECT hostname FROM devices WHERE mac=?", (mac,))
        device = c.fetchone()
        
        event_details = f"Alert for {device['hostname']}: {message}"
        self.log_event(c, mac, 'ALERT', event_details)
        
        conn.commit()
        conn.close()
        
        # Notify subscribers
        for callback in self.alert_subscribers:
            callback(event_details)
    
    def get_bandwidth_stats(self, mac=None, timeframe='1h'):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        timeframe_sql = {
            '1h': "timestamp >= datetime('now', '-1 hour')",
            '24h': "timestamp >= datetime('now', '-1 day')",
            '7d': "timestamp >= datetime('now', '-7 days')",
            '30d': "timestamp >= datetime('now', '-30 days')"
        }
        
        where_clause = f"WHERE {timeframe_sql[timeframe]}"
        if mac:
            where_clause += f" AND mac='{mac}'"
        
        c.execute(f"""SELECT mac, 
                            strftime('%Y-%m-%d %H:%M', timestamp) as time,
                            SUM(bytes_sent) as total_sent,
                            SUM(bytes_recv) as total_recv
                     FROM bandwidth_history
                     {where_clause}
                     GROUP BY mac, time
                     ORDER BY time DESC""")
        
        results = c.fetchall()
        conn.close()
        return results

    # ... (previous methods remain the same)
