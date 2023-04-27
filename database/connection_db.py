import sqlite3

conn = sqlite3.connect('database/database.db', check_same_thread=False)
cursor = conn.cursor()


def sqlite_lower(value_):
    return value_.lower()


def sqlite_upper(value_):
    return value_.upper()


def ignore_case_collation(value1_, value2_):
    if value1_.lower() == value2_.lower():
        return 0
    elif value1_.lower() < value2_.lower():
        return -1
    else:
        return 1


conn.create_collation("NOCASE", ignore_case_collation)
conn.create_function("LOWER", 1, sqlite_lower)
conn.create_function("UPPER", 1, sqlite_upper)


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
    cursor.execute("""CREATE TABLE IF NOT EXISTS admin(
                          id INTEGER, 
                          admin_name TEXT
                      )""")
    conn.commit()
    cursor.execute('SELECT * FROM admin ORDER BY admin_name')
    admins_list = list(map(lambda x: x[element], cursor.fetchall()))
    return admins_list


def main_admin_delete_admin(admin_id):
    cursor.execute(f"DELETE FROM admin where id = {admin_id}")
    conn.commit()


def add_competence(title, description):
    cursor.execute("""CREATE TABLE IF NOT EXISTS competencies(
                            id INTEGER PRIMARY KEY,
                            title TEXT, 
                            description TEXT
                        )""")
    conn.commit()
    cursor.execute("INSERT INTO competencies(title, description) VALUES(?,?)", (title, description))
    conn.commit()


def check_competence(title):
    cursor.execute("""CREATE TABLE IF NOT EXISTS competencies(
                                id INTEGER PRIMARY KEY,
                                title TEXT, 
                                description TEXT
                            )""")
    conn.commit()
    status = cursor.execute(f"SELECT title FROM competencies WHERE title = '{title.casefold()}'").fetchone()
    if status is None:
        return True
    else:
        return False


def delete_competence(id):
    status = cursor.execute(f"SELECT id FROM competencies WHERE id = '{id}'").fetchone()
    if status is None:
        return False
    else:
        cursor.execute(f"DELETE FROM competencies WHERE id='{id}'")
        conn.commit()
        return True


def get_competencies_list():
    cursor.execute("""CREATE TABLE IF NOT EXISTS competencies(
                                    id INTEGER PRIMARY KEY,
                                    title TEXT, 
                                    description TEXT
                                )""")
    conn.commit()
    cursor.execute('SELECT id, title FROM competencies')
    competencies_list = cursor.fetchall()
    return competencies_list


def get_competence_description(id):
    description = cursor.execute(f"SELECT description FROM competencies WHERE id = '{id}'").fetchone()
    if description is None:
        return False
    else:
        return description


def create_profile(title):
    cursor.execute("""CREATE TABLE IF NOT EXISTS profiles(
                                                id INTEGER PRIMARY KEY,
                                                title TEXT
                                            )""")
    conn.commit()
    status = cursor.execute(f"SELECT title FROM profiles WHERE title = '{title}'").fetchone()
    if status is None:
        cursor.execute("INSERT INTO profiles(title) VALUES(?)", (title,))
        conn.commit()
        return True
    else:
        return False


def get_profile_id(title):
    id_profile = cursor.execute(f"SELECT id FROM profiles WHERE title = '{title.casefold()}'").fetchone()
    return id_profile[0]


def add_competence_in_profile(id_competence, id_profile):
    cursor.execute("""CREATE TABLE IF NOT EXISTS CompetencyProfile(
                                    id_competence INTEGER, 
                                    id_profile INTEGER
                                )""")
    conn.commit()
    status_exists = cursor.execute(f"SELECT id FROM competencies WHERE id = {id_competence}").fetchone()
    status_add = cursor.execute(f"SELECT id_competence, id_profile FROM CompetencyProfile "
                                f"WHERE id_competence = '{id_competence}' AND id_profile = '{id_profile}'").fetchone()
    if status_exists is None or status_add:
        return False
    else:
        cursor.execute("INSERT INTO CompetencyProfile(id_competence, id_profile) VALUES(?,?)",
                       (id_competence, id_profile,))
        conn.commit()
        return True


def remove_competence_from_profile(id_competence, id_profile):
    cursor.execute(
        f"DELETE FROM CompetencyProfile WHERE id_competence='{id_competence}' AND id_profile ='{id_profile}'")
    conn.commit()


def check_profile(id):
    status = cursor.execute(f"SELECT id FROM profiles WHERE id = '{id}'").fetchone()
    if status is None:
        return False
    else:
        return True


def delete_profile(id):
    cursor.execute(f"DELETE FROM profiles WHERE id='{id}'")
    cursor.execute(f"DELETE FROM CompetencyProfile WHERE id_profile ='{id}'")
    conn.commit()


def get_profile_list():
    cursor.execute("""CREATE TABLE IF NOT EXISTS profiles(
                                    id INTEGER PRIMARY KEY,
                                    title TEXT
                                    )""")
    conn.commit()
    cursor.execute('SELECT id, title FROM profiles')
    profile_list = cursor.fetchall()
    return profile_list


def get_profile_competencies(profile_id):
    comp_list = cursor.execute(
        f"SELECT id_competence FROM CompetencyProfile WHERE id_profile = '{profile_id}'").fetchall()
    if comp_list is None:
        return False
    else:
        comp_list = list(map(lambda x: x[0], comp_list))
        return comp_list


def get_competence_title(id):
    title = cursor.execute(f"SELECT title FROM competencies WHERE id = '{id}'").fetchone()
    return title


def get_admins_name_for_id(current_id):
    admin_name = cursor.execute(f'SELECT admin_name FROM admin WHERE id = {current_id}').fetchone()
    return admin_name[0]


def get_user_name_for_id(current_id):
    user_name = cursor.execute(f'SELECT login FROM login_id WHERE id = {current_id}').fetchone()
    return user_name[0]
