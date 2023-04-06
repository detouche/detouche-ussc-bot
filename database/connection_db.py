import sqlite3


conn = sqlite3.connect('database/database.db', check_same_thread=False)
cursor = conn.cursor()


def db_table_val(competencies_id: int, competencies_name: str, competencies_text: str):
    cursor.execute('INSERT INTO competencies (competencies_id, competencies_name, competencies_text) VALUES (?, ?, ?)',
                   (competencies_id, competencies_name, competencies_text))
    conn.commit()


def auth_validation(current_id):
    exists = cursor.execute("SELECT id FROM login_id WHERE id = ?", [current_id]).fetchone()
    return True if exists else False


def user_register(current_id: int, user_name: str):
    cursor.execute("""CREATE TABLE IF NOT EXISTS login_id(
                        id INTEGER, 
                        login TEXT
                    )""")
    conn.commit()
    cursor.execute(f"SELECT id FROM login_id WHERE id = {current_id}")
    data = cursor.fetchone()
    if data is None:
        user_id = current_id
        user_name = user_name
        cursor.execute("INSERT INTO login_id VALUES(?,?)", (user_id, user_name))
        conn.commit()
