import sqlite3
import json
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'meetings.db')

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS meetings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            person_company TEXT NOT NULL,
            date_time TEXT,
            purpose TEXT,
            previous_notes TEXT,
            additional_info TEXT,
            brief_json TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_meeting(title, person_company, date_time, purpose, previous_notes, additional_info, brief_data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO meetings (title, person_company, date_time, purpose, previous_notes, additional_info, brief_json)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        title,
        person_company,
        date_time,
        purpose,
        previous_notes,
        additional_info,
        json.dumps(brief_data)
    ))
    meeting_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return meeting_id

def update_meeting_brief(meeting_id, brief_data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE meetings SET brief_json = ? WHERE id = ?
    ''', (json.dumps(brief_data), meeting_id))
    conn.commit()
    conn.close()

def get_all_meetings(limit=50):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, title, person_company, date_time, purpose, created_at
        FROM meetings
        ORDER BY id DESC
        LIMIT ?
    ''', (limit,))
    rows = cursor.fetchall()
    results = [dict(row) for row in rows]
    conn.close()
    return results

def get_meeting_by_id(meeting_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM meetings WHERE id = ?
    ''', (meeting_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        d = dict(row)
        try:
            d['brief'] = json.loads(d['brief_json'])
        except Exception:
            d['brief'] = {}
        return d
    return None

def delete_meeting(meeting_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM meetings WHERE id = ?', (meeting_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted
