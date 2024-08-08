import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

db_path = os.path.join(BASE_DIR, 'db_bot.sqlite3'),

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users ( 
id INTEGER PRIMARY KEY,
    username TEXT UNIQUE ,
    first_name TEXT,
    last_name TEXT,
    access TEXT,
    ban INTEGER
    )
''')

conn.commit()


def get_users_exist(uid):
    cursor.execute("SELECT 1 FROM users WHERE id =?",(uid,))
    return cursor.fetchall() is not None


def get_users_exist_by_username(username):
    cursor.execute("SELECT 1 FROM users WHERE username =?",(username,))
    return cursor.fetchall() is not None


def get_users_insertone(query):
    cursor.execute("INSERT INTO users (id, username, access, ban) VALUES (?, ?, ?, ?)",
                   (query['id'], query['username'], query['access'], query['ban']))
    conn.commit()


def get_users_access(uid):
    cursor.execute("SELECT * FROM users WHERE id =?",(uid,))
    return cursor.fetchall()
    if result:
        return result[0]
    return None


def get_users_ban(uid):
    cursor.execute("SELECT ban FROM users WHERE id = ?", (uid,))
    result = cursor.fetchone()
    if result:
        return result[0] == 1
    return False


def get_users_updateone(query, query2):
    cursor.execute("UPDATE users SET username = ?, access = ?, ban = ? WHERE _id = ?",
                   (query2['username'], query2['access'], query2['ban'], query['_id']))
    conn.commit()


def db_profile_get_usrname(username, get):
    cursor.execute(f"SELECT {get} FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    if result:
        return result[0]
    return None


def close_connection():
    conn.close()
