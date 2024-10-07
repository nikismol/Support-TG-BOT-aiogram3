import sqlite3
import logging

db_path = 'db.sqlite3'


connection = sqlite3.connect(db_path)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS profiles (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    access INTEGER,
    ban INTEGER,
    ban_reason TEXT
)
''')

connection.commit()
connection.commit()

def db_profile_exist(uid):
    cursor = connection.cursor()
    cursor.execute("SELECT 1 FROM profiles WHERE id = ?", (uid,))
    result = cursor.fetchone()
    cursor.close()
    return result is not None

def db_profile_exist_usr(username):
    cursor = connection.cursor()
    cursor.execute("SELECT 1 FROM profiles WHERE username = ?", (username,))
    result = cursor.fetchone()
    cursor.close()
    return result is not None

def db_profile_insertone(query):
    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO profiles (id, username, access, ban) VALUES (?, ?, ?, ?)",
                       (query['_id'], query['username'], query['access'], query['ban']))
        connection.commit()
        cursor.close()
    except sqlite3.IntegrityError:
        logging.error("Профиль с таким username уже существует.")

def db_profile_access(uid):
    cursor = connection.cursor()
    cursor.execute("SELECT access FROM profiles WHERE id = ?", (uid,))
    result = cursor.fetchone()
    cursor.close()

    if result is None:
        return 0
    return result[0]

def db_profile_banned(uid):
    cursor = connection.cursor()
    cursor.execute("SELECT ban FROM profiles WHERE id = ?", (uid,))
    result = cursor.fetchone()
    cursor.close()
    return result[0] == 1


def db_profile_updateone(uid, updates):
    query = "UPDATE profiles SET "
    query_fields = []
    query_values = []

    if 'access' in updates:
        query_fields.append("access = ?")
        query_values.append(updates['access'])

    if 'ban' in updates:
        query_fields.append("ban = ?")
        query_values.append(updates['ban'])

    if 'ban_reason' in updates:
        query_fields.append("ban_reason = ?")
        query_values.append(updates['ban_reason'])

    if query_fields:
        query += ", ".join(query_fields)
        query += " WHERE id = ?"  # Добавляем пробел перед WHERE
        query_values.append(uid)

        # Логируем запрос и параметры
        logging.debug(f"Executing query: {query}")
        logging.debug(f"With values: {query_values}")

        try:
            cursor = connection.cursor()
            cursor.execute(query, tuple(query_values))
            connection.commit()
            logging.info(f"Rows updated: {cursor.rowcount}")
            cursor.close()

            cursor = connection.cursor()
            cursor.execute("SELECT ban, ban_reason FROM profiles WHERE id = ?", (uid,))
            result = cursor.fetchone()
            new_ban_status = result[0]
            ban_reason = result[1]
            logging.info(f"New ban status in DB: {new_ban_status}, Ban reason: {ban_reason}")
            cursor.close()

        except Exception as e:
            logging.error(f"Error during update: {e}")



def db_profile_get_usrname(username, get):
    cursor = connection.cursor()
    cursor.execute(f"SELECT {get} FROM profiles WHERE username = ?", (username,))
    result = cursor.fetchone()
    cursor.close()
    return result[0]


def close_connection():
    connection.close()
