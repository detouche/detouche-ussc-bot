import sqlite3


conn = sqlite3.connect('database/database.db', check_same_thread=False)
cursor = conn.cursor()


def db_table_val(competencies_id: int, competencies_name: str, competencies_text: str):
    cursor.execute('INSERT INTO competencies (competencies_id, competencies_name, competencies_text) VALUES (?, ?, ?)',
                   (competencies_id, competencies_name, competencies_text))
    conn.commit()


def auth_validation(current_id: int):
    cursor.execute("""CREATE TABLE IF NOT EXISTS login_id(
                            id INTEGER, 
                            login TEXT
                        )""")
    conn.commit()
    exists = cursor.execute("SELECT id FROM login_id WHERE id = ?", [current_id]).fetchone()
    return True if exists else False


def user_rename(current_id: int, user_name: str):
    cursor.execute("UPDATE login_id SET login = ? WHERE id = ?", (user_name, current_id))
    conn.commit()


def get_user_list():
    cursor.execute('SELECT * FROM login_id ORDER BY login')
    users_list = list(map(lambda x: x, cursor.fetchall()))
    return users_list


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


def main_admin_add_admin(current_id: int, admin_name: str):
    cursor.execute("""CREATE TABLE IF NOT EXISTS admin(
                        id INTEGER, 
                        admin_name TEXT
                    )""")
    conn.commit()
    cursor.execute(f"SELECT id FROM admin WHERE id = {current_id}")
    data = cursor.fetchone()
    if data is None:
        admin_id = current_id
        admin_name = admin_name
        cursor.execute("INSERT INTO admin VALUES(?,?)", (admin_id, admin_name))
        cursor.execute("SELECT * FROM admin ORDER BY admin_name")
        conn.commit()


def get_admins_list(element):
    cursor.execute('SELECT * FROM admin ORDER BY admin_name')
    admins_list = list(map(lambda x: x[element], cursor.fetchall()))
    return admins_list


def main_admin_delete_admin(admin_id):
    cursor.execute(f"DELETE FROM admin where id = {admin_id}")
    conn.commit()
