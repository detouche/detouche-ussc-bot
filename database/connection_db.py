import sqlite3

conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()


def db_table_val(competencies_id: int, competencies_name: str, competencies_text: str):
    cursor.execute('INSERT INTO competencies (competencies_id, competencies_name, competencies_text) VALUES (?, ?, ?)',
                   (competencies_id, competencies_name, competencies_text))
    conn.commit()
