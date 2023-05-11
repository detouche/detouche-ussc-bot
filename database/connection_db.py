import sqlite3

conn = sqlite3.connect('database/database.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS admins(
                    admin_id INTEGER, 
                    admin_name TEXT
                )""")
conn.commit()

cursor.execute("""CREATE TABLE IF NOT EXISTS competencies(
                        competence_id INTEGER PRIMARY KEY,
                        competence_name TEXT, 
                        competence_description TEXT
                    )""")
conn.commit()

cursor.execute("""CREATE TABLE IF NOT EXISTS competence_profile(
                                competence_id INTEGER, 
                                profile_id INTEGER
                            )""")
conn.commit()

cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                        user_id INTEGER, 
                        user_name TEXT
                    )""")
conn.commit()

cursor.execute("""CREATE TABLE IF NOT EXISTS profiles(
                                            profile_id INTEGER PRIMARY KEY,
                                            profile_name TEXT
                                        )""")
conn.commit()

cursor.execute("""CREATE TABLE IF NOT EXISTS sessions(
                        session_id INTEGER PRIMARY KEY,
                        candidate_name TEXT, 
                        profile_name TEXT,
                        connection_code INTEGER,
                        admin_id INTEGER,
                        competence_name TEXT,
                        competence_description TEXT
                    )""")
conn.commit()

cursor.execute("""CREATE TABLE IF NOT EXISTS user_session(
                                        user_session_id INTEGER PRIMARY KEY,
                                        candidate_name TEXT, 
                                        profile_name TEXT,
                                        competence_name TEXT,
                                        competence_description TEXT,
                                        connection_code INTEGER,
                                        user_id INTEGER,
                                        grade INTEGER
                                    )""")
conn.commit()


def auth_validation(user_id: int):
    exists = cursor.execute("SELECT user_id FROM users WHERE user_id = ?", [user_id]).fetchone()
    return True if exists else False


def user_rename(user_id: int, new_user_name: str):
    cursor.execute("UPDATE users SET user_name = ? WHERE user_id = ?", (new_user_name, user_id))
    conn.commit()


def get_user_list_by_column(column):
    cursor.execute('SELECT * FROM users ORDER BY user_name')
    return list(map(lambda x: x[column], cursor.fetchall()))


def user_register(user_id: int, user_name: str):
    cursor.execute(f"SELECT user_id FROM users WHERE user_id = {user_id}")
    data = cursor.fetchone()
    if data is None:
        cursor.execute("INSERT INTO users VALUES(?,?)", (user_id, user_name))
        conn.commit()


def main_admin_add_admin(admin_id: int, admin_name: str):
    cursor.execute(f"SELECT admin_id FROM admins WHERE admin_id = {admin_id}")
    data = cursor.fetchone()
    if data is None:
        cursor.execute("INSERT INTO admins VALUES(?,?)", (admin_id, admin_name))
        cursor.execute("SELECT * FROM admins ORDER BY admin_name")
        conn.commit()


def get_admins_list_by_column(column):
    cursor.execute('SELECT * FROM admins ORDER BY admin_name')
    return list(map(lambda x: x[column], cursor.fetchall()))


def main_admin_delete_admin(admin_id):
    cursor.execute(f"DELETE FROM admins where admin_id = {admin_id}")
    delete_session(admin_id=admin_id)
    conn.commit()


def add_competence(cometence_name, competence_description):
    cursor.execute("INSERT INTO competencies(competence_name, competence_description) VALUES(?,?)",
                   (cometence_name, competence_description))
    conn.commit()


def check_competence(competence_name):
    status = cursor.execute(
        f"SELECT competence_name FROM competencies WHERE competence_name = '{competence_name.casefold()}'").fetchone()
    if status is None:
        return True
    else:
        return False


def check_competence_id(competence_id):
    status = cursor.execute(
        f"SELECT competence_id FROM competencies WHERE competence_id = '{competence_id}'").fetchone()
    if status is None:
        return False
    else:
        return True


def delete_competence(competence_id):
    cursor.execute(f"DELETE FROM competencies WHERE competence_id ='{competence_id}'")
    cursor.execute(f"DELETE FROM competence_profile WHERE competence_id ='{competence_id}'")
    conn.commit()


def get_competencies_list():
    return cursor.execute('SELECT competence_id, competence_name FROM competencies').fetchall()


def get_competence_description(competence_id):
    description = cursor.execute(
        f"SELECT competence_description FROM competencies WHERE competence_id = '{competence_id}'").fetchone()
    if description is None:
        return False
    else:
        return description


def create_profile_db(profile_name):
    status = cursor.execute(f"SELECT profile_name FROM profiles WHERE profile_name = '{profile_name}'").fetchone()
    if status is None:
        cursor.execute("INSERT INTO profiles(profile_name) VALUES(?)", [profile_name])
        conn.commit()
        return True
    else:
        return False


def get_profile_id(profile_name):
    id_profile = cursor.execute(
        f"SELECT profile_id FROM profiles WHERE profile_name = '{profile_name.casefold()}'").fetchone()
    return id_profile[0]


def add_competence_in_profile(competence_id, profile_id):
    status_exists = cursor.execute(
        f"SELECT competence_id FROM competencies WHERE competence_id = {competence_id}").fetchone()
    status_add = cursor.execute(f"SELECT competence_id, profile_id FROM competence_profile "
                                f"WHERE competence_id = '{competence_id}' AND profile_id = '{profile_id}'").fetchone()
    if status_exists is None or status_add:
        return False
    else:
        cursor.execute("INSERT INTO competence_profile(competence_id, profile_id) VALUES(?,?)",
                       (competence_id, profile_id))
        conn.commit()
        return True


def remove_competence_from_profile(competence_id, profile_id):
    cursor.execute(
        f"DELETE FROM competence_profile WHERE competence_id = '{competence_id}' AND profile_id ='{profile_id}'")
    conn.commit()


def check_profile(profile_id):
    status = cursor.execute(f"SELECT profile_id FROM profiles WHERE profile_id = '{profile_id}'").fetchone()
    if status is None:
        return False
    else:
        return True


def delete_profile(profile_id):
    cursor.execute(f"DELETE FROM profiles WHERE profile_id ='{profile_id}'")
    cursor.execute(f"DELETE FROM competence_profile WHERE profile_id ='{profile_id}'")
    conn.commit()


def get_profile_list():
    return cursor.execute('SELECT profile_id, profile_name FROM profiles').fetchall()


def get_profile_competencies(profile_id):
    comp_list = cursor.execute(
        f"SELECT competence_id FROM competence_profile WHERE profile_id = '{profile_id}'").fetchall()
    if comp_list is None:
        return False
    else:
        return list(map(lambda x: x[0], comp_list))


def get_competence_title(competence_id):
    return cursor.execute(
        f"SELECT competence_name FROM competencies WHERE competence_id = '{competence_id}'").fetchone()


def get_competence_id(competence_title):
    return cursor.execute(
        f"SELECT competence_id FROM competencies WHERE competence_name = '{competence_title}'").fetchone()

def change_competence_title(competence_id, new_competence_name):
    status_title = cursor.execute(
        f"SELECT competence_name FROM competencies WHERE competence_name = '{new_competence_name}'").fetchone()
    status_id = cursor.execute(f"SELECT competence_id FROM competencies "
                               f"WHERE competence_id ='{competence_id}'").fetchone()
    if status_title is None and status_id is not None:
        cursor.execute(
            f"UPDATE competencies "
            f"SET competence_name = '{new_competence_name.casefold()}' WHERE competence_id = '{competence_id}'")
        conn.commit()
        return True
    else:
        return False


def change_competence_description(competence_id, new_competence_description):
    status_id = cursor.execute(f"SELECT competence_id FROM competencies "
                               f"WHERE competence_id ='{competence_id}'").fetchone()
    if status_id is not None:
        cursor.execute(f"UPDATE competencies "
                       f"SET competence_description = '{new_competence_description}' "
                       f"WHERE competence_id = '{competence_id}'")
        conn.commit()
        return True
    else:
        return False


def change_profile_title(profile_id, new_profile_name):
    status_title = cursor.execute(f"SELECT profile_name FROM profiles "
                                  f"WHERE profile_name = '{new_profile_name}'").fetchone()
    status_id = cursor.execute(f"SELECT profile_id FROM profiles WHERE profile_id ='{profile_id}'").fetchone()
    if status_title is None and status_id is not None:
        cursor.execute(f"UPDATE profiles SET profile_name = '{new_profile_name.casefold()}' "
                       f"WHERE profile_id = '{profile_id}'")
        conn.commit()
        return True
    else:
        return False


def competencies_in_profile(profile_id):
    status = cursor.execute(f"SELECT profile_id FROM profiles WHERE profile_id ='{profile_id}'").fetchone()
    if status is None:
        return False
    else:
        comp_list = cursor.execute(
            f"SELECT competence_id FROM competence_profile WHERE profile_id ='{profile_id}'").fetchall()
        return list(map(lambda x: x[0], comp_list))


def competence_in_profile(profile_id, competence_id):
    status = cursor.execute(f"SELECT competence_id, profile_id FROM competence_profile "
                            f"WHERE profile_id = {profile_id} AND competence_id = {competence_id}").fetchone()
    if status is None:
        return False
    return True


def delete_competence_from_profile(competence_id, profile_id):
    status = cursor.execute(
        f"SELECT competence_id FROM competence_profile "
        f"WHERE competence_id ='{competence_id}' AND profile_id ='{profile_id}'").fetchone()
    if status is None:
        return False
    else:
        cursor.execute(
            f"DELETE FROM competence_profile WHERE competence_id='{competence_id}' AND profile_id ='{profile_id}'")
        conn.commit()
        return True


def get_admins_name_for_id(admin_id):
    admin_name = cursor.execute(f'SELECT admin_name FROM admins WHERE admin_id = {admin_id}').fetchone()
    return admin_name[0]


def get_user_name_for_id(user_id):
    user_name = cursor.execute(f'SELECT user_name FROM users WHERE user_id = {user_id}').fetchone()
    return user_name[0]


def create_session(candidate_name, profile_name, connection_code, user_id, competence_name, competence_description):
    cursor.execute(
        "INSERT INTO sessions(candidate_name, "
        "profile_name, "
        "connection_code, "
        "admin_id, "
        "competence_name, "
        "competence_description) "
        "VALUES(?,?,?,?,?,?)",
        (candidate_name, profile_name, connection_code, user_id, competence_name, competence_description))
    conn.commit()


def get_session_info(column):
    cursor.execute('SELECT * FROM sessions')
    return list(map(lambda x: x[column], cursor.fetchall()))


def get_session_code_admin(admin_id):
    connection_code = cursor.execute(f'SELECT connection_code FROM sessions WHERE admin_id = {admin_id}').fetchone()
    return connection_code[0]


def delete_session(admin_id):
    connection_code = cursor.execute(f'SELECT connection_code FROM sessions WHERE admin_id = {admin_id}').fetchone()
    cursor.execute(f"DELETE FROM sessions WHERE admin_id = {admin_id}")
    if connection_code is not None:
        cursor.execute(f"DELETE FROM user_session WHERE connection_code = {connection_code[0]}")
    conn.commit()


def get_candidate_name(connection_code):
    name = cursor.execute(f'SELECT candidate_name FROM sessions WHERE connection_code = {connection_code}').fetchone()
    return name[0]


def get_profile_name_session(connection_code):
    name = cursor.execute(f'SELECT profile_name FROM sessions WHERE connection_code = {connection_code}').fetchone()
    return name[0]


def get_comp_name_session(connection_code):
    name = cursor.execute(f'SELECT competence_name FROM sessions WHERE connection_code = {connection_code}').fetchall()
    return name


def get_comp_desc_session(connection_code):
    name = cursor.execute(
        f'SELECT competence_description FROM sessions WHERE connection_code = {connection_code}').fetchall()
    return name


def get_connection_code_session(user_id):
    connection_code = cursor.execute(f'SELECT connection_code FROM user_session WHERE user_id = {user_id}') \
        .fetchall()
    return connection_code[0]


def get_profile_name(profile_id):
    name = cursor.execute(f'SELECT profile_name FROM profiles WHERE profile_id = {profile_id}').fetchone()
    return name[0]


def get_competencies_id(profile_id):
    name = cursor.execute(f'SELECT competence_id FROM competence_profile WHERE profile_id = {profile_id}').fetchone()
    return name


def user_session_info(candidate_name, profile_name, competence_name, competence_description, connection_code, user_id,
                      grade):
    cursor.execute(
        "INSERT INTO user_session(candidate_name, profile_name, competence_name, competence_description, "
        "connection_code, "
        "user_id, grade) VALUES(?,?,?,?,?,?,?)",
        (candidate_name, profile_name, competence_name, competence_description, connection_code, user_id, grade))
    conn.commit()


def get_user_session_info(column, connection_code):
    cursor.execute(f'SELECT * FROM user_session WHERE connection_code = {connection_code}')
    return list(map(lambda x: x[column], cursor.fetchall()))


def get_session_code(user_id):
    session_code = cursor.execute(f'SELECT connection_code FROM user_session WHERE user_id = {user_id}').fetchone()
    return session_code[0]


def user_has_active_session(user_id):
    exists = cursor.execute(f"SELECT user_id FROM user_session WHERE user_id = {user_id}").fetchone()
    return False if exists is None else True


def get_assessment_comp_session(competence_name, user_id):
    assessment = cursor.execute(f'SELECT grade FROM user_session WHERE user_id = {user_id} '
                                f'AND competence_name = "{competence_name}"').fetchone()
    return assessment[0]


def get_id_comp_session(competence_name, user_id):
    competence_id = cursor.execute(f'SELECT user_session_id FROM user_session WHERE user_id = {user_id} '
                                   f'AND competence_name = "{competence_name}"').fetchone()
    return competence_id[0]


def get_current_comp_desc_session(competence_id):
    competence_description = cursor.execute(
        f"SELECT competence_description FROM user_session WHERE user_session_id = {competence_id}").fetchone()
    return competence_description[0]


def get_current_comp_name_session(competence_id):
    competence_name = cursor.execute(
        f"SELECT competence_name FROM user_session WHERE user_session_id = {competence_id}").fetchone()
    return competence_name[0]


def get_current_comp_grade_session(competence_id):
    competence_grade = cursor.execute(
        f"SELECT grade FROM user_session WHERE user_session_id = {competence_id}").fetchone()
    return competence_grade[0]


def transform_grade_current_comp(competence_id, new_grade):
    cursor.execute(f"UPDATE user_session SET grade = '{new_grade}' WHERE user_session_id = '{competence_id}'")
    conn.commit()


def get_session_user_id(connection_code):
    user_id = cursor.execute(f"SELECT user_id FROM user_session WHERE connection_code = {connection_code} "
                             f"GROUP BY user_id").fetchall()
    return user_id


def get_competence_names(connection_code):
    competence_names = cursor.execute(
        f"SELECT competence_name FROM user_session WHERE connection_code = {connection_code} "
        f"GROUP BY competence_name").fetchall()
    return competence_names


def get_competence_grades(competence_name, connection_code):
    return cursor.execute(f"SELECT grade FROM user_session WHERE competence_name = "
                          f"'{competence_name}' AND connection_code = {connection_code}").fetchall()


def get_user_grades(user_id, connection_code):
    return cursor.execute(f"SELECT competence_name, grade FROM user_session "
                          f"WHERE user_id = {user_id} AND connection_code = {connection_code}").fetchall()
