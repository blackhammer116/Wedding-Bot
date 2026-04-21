import sqlite3
import os

DB_NAME = 'wedding_bot.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS photos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            file_id TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_photo(user_id, file_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('INSERT INTO photos (user_id, file_id) VALUES (?, ?)', (user_id, file_id))
    conn.commit()
    conn.close()

def get_random_photos(limit=10):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT file_id FROM photos ORDER BY RANDOM() LIMIT ?', (limit,))
    photos = c.fetchall()
    conn.close()
    return [p[0] for p in photos]
