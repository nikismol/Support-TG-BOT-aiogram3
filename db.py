import sqlite3

db_path = 'path'  # Путь к файлу базы данных SQLite


connection = sqlite3.connect(db_path)
cursor = connection.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS profiles (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    access INTEGER,
    ban INTEGER
)
''')
connection.commit()

def db_profile_exist(uid):
    cursor.execute("SELECT 1 FROM profiles WHERE id = ?", (uid,))
    return cursor.fetchone() is not None

def db_profile_exist_usr(username):
    cursor.execute("SELECT 1 FROM profiles WHERE username = ?", (username,))
    return cursor.fetchone() is not None

def db_profile_insert(query):
    try:
        cursor.execute("INSERT INTO profiles (id, username, access, ban) VALUES (?, ?, ?, ?)",
                       (query['_id'], query['username'], query['access'], query['ban']))
        connection.commit()
    except sqlite3.IntegrityError:
        print("Профиль с таким username уже существует.")

def db_profile_access(uid):
    cursor = connection.cursor()
    cursor.execute("SELECT access FROM profiles WHERE id = ?", (uid,))
    result = cursor.fetchone()

    if result is None:
        return 0

    return result[0]

def db_profile_banned(uid):
    cursor.execute("SELECT ban FROM profiles WHERE id = ?", (uid,))
    return cursor.fetchone()[0] == 1

def db_profile_update(uid, updates):
    # Формируем запрос на обновление только тех полей, которые есть в словаре updates
    query = "UPDATE profiles SET "
    query_fields = []
    query_values = []

    if 'access' in updates:
        query_fields.append("access = ?")
        query_values.append(updates['access'])

    if 'ban' in updates:
        query_fields.append("ban = ?")
        query_values.append(updates['ban'])

    query += ", ".join(query_fields)
    query += " WHERE id = ?"
    query_values.append(uid)

    # Выполняем SQL-запрос с нужными значениями
    cursor.execute(query, tuple(query_values))
    connection.commit()


def db_profile_get_user_name(username, get):
    cursor.execute(f"SELECT {get} FROM profiles WHERE username = ?", (username,))
    return cursor.fetchone()[0]

# Закрытие подключения к базе данных при завершении работы
def close_connection():
    connection.close()
