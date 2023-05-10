import sqlite3


conn = sqlite3.connect('database/database.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS user_session(
                                        id INTEGER PRIMARY KEY,
                                        candidate_names TEXT, 
                                        profile_names TEXT,
                                        comp_names TEXT,
                                        comp_desc TEXT,
                                        connection_codes INTEGER,
                                        id_evaluating INTEGER,
                                        assessments_competencies INTEGER
                                    )""")
conn.commit()

cursor.execute("""CREATE TABLE IF NOT EXISTS session(
                        id INTEGER PRIMARY KEY,
                        candidate_name TEXT, 
                        profile_name TEXT,
                        connection_code INTEGER,
                        admin_id INTEGER,
                        comp_name TEXT,
                        comp_desc TEXT
                    )""")
conn.commit()


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


def get_user_list(element):
    cursor.execute('SELECT * FROM login_id ORDER BY login')
    users_list = list(map(lambda x: x[element], cursor.fetchall()))
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
    delete_session(admin_id)
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


def check_competence_id(id):
    status = cursor.execute(f"SELECT id FROM competencies WHERE id = '{id}'").fetchone()
    if status is None:
        return False
    else:
        return True


def delete_competence(id):
    cursor.execute(f"DELETE FROM competencies WHERE id='{id}'")
    cursor.execute(f"DELETE FROM CompetencyProfile WHERE id_competence ='{id}'")
    conn.commit()


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


def change_competence_title(id, new_title):
    status_title = cursor.execute(f"SELECT title FROM competencies WHERE title = '{new_title}'").fetchone()
    status_id = cursor.execute(f"SELECT id FROM competencies WHERE id ='{id}'").fetchone()
    if status_title is None and status_id is not None:
        cursor.execute(f"UPDATE competencies SET title = '{new_title.casefold()}' WHERE id = '{id}'")
        conn.commit()
        return True
    else:
        return False


def change_competence_description(id, new_desc):
    status_id = cursor.execute(f"SELECT id FROM competencies WHERE id ='{id}'").fetchone()
    if status_id is not None:
        cursor.execute(f"UPDATE competencies SET description = '{new_desc}' WHERE id = '{id}'")
        conn.commit()
        return True
    else:
        return False


def change_profile_title(id, new_title):
    status_title = cursor.execute(f"SELECT title FROM profiles WHERE title = '{new_title}'").fetchone()
    status_id = cursor.execute(f"SELECT id FROM profiles WHERE id ='{id}'").fetchone()
    if status_title is None and status_id is not None:
        cursor.execute(f"UPDATE profiles SET title = '{new_title.casefold()}' WHERE id = '{id}'")
        conn.commit()
        return True
    else:
        return False


def competencies_in_profile(id_profile):
    status = cursor.execute(f"SELECT id FROM profiles WHERE id ='{id_profile}'").fetchone()
    if status is None:
        return False
    else:
        comp_list = cursor.execute(
            f"SELECT id_competence FROM CompetencyProfile WHERE id_profile ='{id_profile}'").fetchall()
        comp_list = list(map(lambda x: x[0], comp_list))
        return comp_list


def delete_competence_from_profile(competence_id, profile_id):
    status = cursor.execute(
        f"SELECT id_competence FROM CompetencyProfile WHERE id_competence ='{competence_id}' AND id_profile='{profile_id}'").fetchone()
    if status is None:
        return False
    else:
        cursor.execute(
            f"DELETE FROM CompetencyProfile WHERE id_competence='{competence_id}' AND id_profile ='{profile_id}'")
        conn.commit()
        return True


def get_admins_name_for_id(current_id):
    admin_name = cursor.execute(f'SELECT admin_name FROM admin WHERE id = {current_id}').fetchone()
    return admin_name[0]


def get_user_name_for_id(current_id):
    user_name = cursor.execute(f'SELECT login FROM login_id WHERE id = {current_id}').fetchone()
    return user_name[0]


def create_session(candidate_name, profile_name, connection_code, user_id, comp_name, comp_desc):
    cursor.execute("INSERT INTO session(candidate_name, profile_name, connection_code, admin_id, comp_name, comp_desc) "
                   "VALUES(?,?,?,?,?,?)",
                   (candidate_name, profile_name, connection_code, user_id, comp_name, comp_desc))
    conn.commit()


def get_session_info(element):
    cursor.execute('SELECT * FROM session')
    session_info_list = list(map(lambda x: x[element], cursor.fetchall()))
    return session_info_list


def get_session_code_admin(admin_id):
    connection_code = cursor.execute(f'SELECT connection_code FROM session WHERE admin_id = {admin_id}').fetchone()
    return connection_code[0]


def delete_session(admin_id):
    connection_code = cursor.execute(f'SELECT connection_code FROM session WHERE admin_id = {admin_id}').fetchone()
    cursor.execute(f"DELETE FROM session WHERE admin_id = {admin_id}")
    if connection_code is not None:
        cursor.execute(f"DELETE FROM user_session WHERE connection_codes = {connection_code[0]}")
    conn.commit()


def get_candidate_name(connection_code):
    name = cursor.execute(f'SELECT candidate_name FROM session WHERE connection_code = {connection_code}').fetchone()
    return name[0]


def get_profile_name_session(connection_code):
    name = cursor.execute(f'SELECT profile_name FROM session WHERE connection_code = {connection_code}').fetchone()
    return name[0]


def get_comp_name_session(connection_code):
    name = cursor.execute(f'SELECT comp_name FROM session WHERE connection_code = {connection_code}').fetchall()
    return name


def get_comp_desc_session(connection_code):
    name = cursor.execute(f'SELECT comp_desc FROM session WHERE connection_code = {connection_code}').fetchall()
    return name


def get_connection_code_session(user_id):
    connection_code = cursor.execute(f'SELECT connection_codes FROM user_session WHERE id_evaluating = {user_id}')\
        .fetchall()
    return connection_code[0]


def get_profile_name(profile_number):
    name = cursor.execute(f'SELECT title FROM profiles WHERE id = {profile_number}').fetchone()
    return name[0]


def get_competencies_id(id_profile):
    name = cursor.execute(f'SELECT id_competence FROM CompetencyProfile WHERE id_profile = {id_profile}').fetchone()
    return name


def user_session_info(candidate_name, profile_name, comp_name, comp_desc, connection_code, user_id,
                      assessment_competence):
    cursor.execute("INSERT INTO user_session(candidate_names, profile_names, comp_names, comp_desc, connection_codes, "
                   "id_evaluating, assessments_competencies) VALUES(?,?,?,?,?,?,?)",
                   (candidate_name, profile_name, comp_name, comp_desc, connection_code, user_id, assessment_competence))
    conn.commit()


def get_user_session_info(element, start_session):
    cursor.execute(f'SELECT * FROM user_session WHERE connection_codes = {start_session}')
    session_info_list = list(map(lambda x: x[element], cursor.fetchall()))
    return session_info_list


def get_session_code(current_id):
    session_code = cursor.execute(f'SELECT connection_codes FROM user_session WHERE id_evaluating = {current_id}').\
        fetchone()
    return session_code[0]


def user_has_active_session(current_id):
    exists = cursor.execute(f"SELECT id_evaluating FROM user_session WHERE id_evaluating = {current_id}").fetchone()
    return False if exists is None else True


def get_assessment_comp_session(comp_name, current_id):
    assessment = cursor.execute(f'SELECT assessments_competencies FROM user_session WHERE id_evaluating = {current_id} '
                                f'AND comp_names = "{comp_name}"').fetchone()
    return assessment[0]


def get_id_comp_session(comp_name, current_id):
    id_comp = cursor.execute(f'SELECT id FROM user_session WHERE id_evaluating = {current_id} '
                             f'AND comp_names = "{comp_name}"').fetchone()
    return id_comp[0]


def get_current_comp_desc_session(comp_id):
    comp_desc = cursor.execute(f"SELECT comp_desc FROM user_session WHERE id = {comp_id}").fetchone()
    return comp_desc[0]


def get_current_comp_name_session(comp_id):
    comp_name = cursor.execute(f"SELECT comp_names FROM user_session WHERE id = {comp_id}").fetchone()
    return comp_name[0]


def get_current_comp_grade_session(comp_id):
    comp_grade = cursor.execute(f"SELECT assessments_competencies FROM user_session WHERE id = {comp_id}").fetchone()
    return comp_grade[0]


def transform_grade_current_comp(comp_id, new_grade):
    cursor.execute(f"UPDATE user_session SET assessments_competencies = '{new_grade}' WHERE id = '{comp_id}'")
    conn.commit()


def get_id_evaluating(connection_code):
    id_evaluating = cursor.execute(f"SELECT id_evaluating FROM user_session WHERE connection_codes = {connection_code} "
                                   f"GROUP BY id_evaluating").fetchall()
    return id_evaluating


def get_comp_names(connection_code):
    comp_names = cursor.execute(f"SELECT comp_names FROM user_session WHERE connection_codes = {connection_code} "
                                f"GROUP BY comp_names").fetchall()
    return comp_names


def get_assessments_competencies(comp_name, connection_code):
    assessments_competencies = cursor.execute(f"SELECT assessments_competencies FROM user_session WHERE comp_names = "
                                              f"'{comp_name}' AND connection_codes = {connection_code}").fetchall()
    return assessments_competencies


def get_user_grades(id_evaluating, connection_code):
    grades = cursor.execute(f"SELECT comp_names, assessments_competencies FROM user_session "
                            f"WHERE id_evaluating = {id_evaluating} AND connection_codes = {connection_code}").fetchall()
    return grades
