import sqlite3

def init_db():
    conn = sqlite3.connect("honeypot.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        ip TEXT,
        port INTEGER,
        service TEXT,
        data TEXT,
        country TEXT,
        city TEXT,
        isp TEXT
    )''')
    conn.commit()
    conn.close()

def save_log(timestamp, ip, port, service, data, geo):
    conn = sqlite3.connect("honeypot.db")
    c = conn.cursor()
    c.execute("INSERT INTO logs (timestamp, ip, port, service, data, country, city, isp) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
              (timestamp, ip, port, service, data, geo["country"], geo["city"], geo["isp"]))
    conn.commit()
    conn.close()
