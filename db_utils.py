import sqlite3

def create_table() -> None:
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY, 
            login TEXT, 
            password TEXT
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

def check_user(login: str, password: str) -> tuple:
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT id FROM users WHERE login = ? AND password = ?
    ''', (login, password))

    data = cursor.fetchone()

    conn.commit()
    conn.close()

    return data

def add_user(login: str, password: str) -> None:
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO users(login, password) VALUES(?, ?)
    ''', (login, password))

    conn.commit()
    conn.close()

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

def add_post(author_id: int, text: str) -> None: 
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO posts(author_id, content) VALUES(?, ?)
    ''', (author_id, text))

    conn.commit()
    conn.close()

def get_posts() -> dict:
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM posts
    ''')
    data = cursor.fetchall()

    cols = [col[0] for col in cursor.description]

    result = [dict(zip(cols, post)) for post in data]

    conn.commit()
    conn.close()

    return result

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

def DESTROY_SERVER(destroy_users:bool = True, destroy_posts:bool = True ) -> None:
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if destroy_users:
        cursor.execute(f'DROP TABLE IF EXISTS users')
    if destroy_posts:
        cursor.execute(f'DROP TABLE IF EXISTS posts')

if __name__ == '__main__':
    DESTROY_SERVER()
    create_table()
    add_user('adminG', 'qQhD')