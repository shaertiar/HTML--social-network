import sqlite3

# Фукнкция создания таблицы
def create_table() -> None:
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY, 
            login TEXT, 
            password TEXT,
            word TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY,
            author_id INTEGER, 
            content TEXT,
            publish_time DATETIME DEFAULT CURRENT_TIMESTAMP,
            likes INTEGER DEFAULT 0
        )
    ''')

# Функция проверки наличия пользователя
def check_user(login:str, password:str = None, word:str = None) -> tuple:
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if word:
        cursor.execute('''
            SELECT id FROM users WHERE login = ? AND word = ?
        ''', (login, word))
    else:
        cursor.execute('''
            SELECT id FROM users WHERE login = ? AND password = ?
        ''', (login, password))

    data = cursor.fetchone()

    conn.commit()
    conn.close()

    return data

# Функция добавления пользователя
def add_user(login:str, password:str, word:str) -> None:
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO users(login, password, word) VALUES(?, ?, ?)
    ''', (login, password, word))

    conn.commit()
    conn.close()

# Функция проверки наличия логина
def check_login(login) -> bool:
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT id FROM users WHERE login = ?
    ''', (login,))
    data = cursor.fetchone()

    conn.commit()
    conn.close()

    return data != None

# Функция получения логина
def get_login(id) -> str:
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT login FROM users WHERE id = ?
    ''', (id,))
    data = cursor.fetchone()

    conn.commit()
    conn.close()

    return data[0]

# Функция добавления поста
def add_post(author_id:int, text:str) -> None:
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO posts(author_id, content) VALUES(?, ?)
    ''', (author_id, text))

    conn.commit()
    conn.close()

# Функция получения поста
def get_posts(page:int = 1) -> dict:
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    offset = (page-1) * 5

    cursor.execute('''
        SELECT * FROM posts ORDER BY publish_time DESC LIMIT 5 OFFSET ?
    ''', (offset,))
    data = cursor.fetchall()

    cols = [col[0] for col in cursor.description]

    result = [dict(zip(cols, post)) for post in data]

    for post in result:
        cursor.execute('''
            SELECT login FROM users WHERE id = ?
        ''', (post['author_id'],))
        post['author'] = cursor.fetchone()[0]

    conn.commit()
    conn.close()

    return result

# Функция получения количества постов
def count_posts() -> int:
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT COUNT(*) FROM posts
    ''')
    data = cursor.fetchone()

    conn.commit()
    conn.close()

    return data[0]

# Функция удаления таблицы
def DESTROY_SERVER(destroy_users:bool = True, destroy_posts:bool = True) -> None:
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if destroy_users:
        cursor.execute(f'DROP TABLE IF EXISTS users')
    if destroy_posts:
        cursor.execute(f'DROP TABLE IF EXISTS posts')

# Функция обнолвения пароля
def update_password(login:str, password:str) -> None:
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE users SET password = ? WHERE login = ?
    ''', (password, login))

    conn.commit()
    conn.close()

# Удали если хочешь
if __name__ == '__main__':
    DESTROY_SERVER()
    create_table()
    add_user('adminG', 'qQhD', 'Philips')