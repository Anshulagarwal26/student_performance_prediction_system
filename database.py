import sqlite3
import pandas as pd

DB_NAME = "users.db"


def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Student records table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            student_name TEXT NOT NULL,
            student_id TEXT NOT NULL,
            attendance REAL,
            internal_marks REAL,
            assignment_marks REAL,
            study_hours REAL,
            previous_marks REAL,
            prediction TEXT,
            performance_score REAL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


def register_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


def login_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, username FROM users WHERE username = ? AND password = ?",
        (username, password)
    )

    user = cursor.fetchone()

    conn.close()

    return user


def add_student(
    user_id,
    student_name,
    student_id,
    attendance,
    internal_marks,
    assignment_marks,
    study_hours,
    previous_marks,
    prediction,
    performance_score
):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO students (
            user_id,
            student_name,
            student_id,
            attendance,
            internal_marks,
            assignment_marks,
            study_hours,
            previous_marks,
            prediction,
            performance_score
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        student_name,
        student_id,
        attendance,
        internal_marks,
        assignment_marks,
        study_hours,
        previous_marks,
        prediction,
        performance_score
    ))

    conn.commit()
    conn.close()


def get_students(user_id):

    conn = sqlite3.connect(DB_NAME)

    query = """
        SELECT
            student_name AS "Student Name",
            student_id AS "Student ID",
            attendance AS "Attendance",
            internal_marks AS "Internal Marks",
            assignment_marks AS "Assignment Marks",
            study_hours AS "Study Hours",
            previous_marks AS "Previous Marks",
            prediction AS "Prediction",
            performance_score AS "Performance Score"
        FROM students
        WHERE user_id = ?
        ORDER BY id DESC
    """

    data = pd.read_sql_query(
        query,
        conn,
        params=(user_id,)
    )

    conn.close()

    return data

create_database()

def clear_student_records(user_id):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM students WHERE user_id = ?",
        (user_id,)
    )

    conn.commit()
    conn.close()