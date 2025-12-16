"""
SQL Module - Student Grade Management System
============================================

Demonstrates all 5 SQL requirements:
1. Create a SQL database with tables
2. Query data from the database (READ)
3. Add new data to the database (CREATE)
4. Update data in the database (UPDATE)
5. Delete data from the database (DELETE)

Stretch Goal: Multiple tables with JOIN operations
- Students table
- Courses table
- Grades table (JOIN between Students and Courses)
"""

import sqlite3
import os

DB_NAME = "data/grades.db"

def initialize_database():
    """
    Req 1: Create SQL database with multiple tables
    Creates 3 tables with relationships for a student grade management system
    """
    os.makedirs(os.path.dirname(DB_NAME), exist_ok=True)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Table 1: Students
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            gpa REAL DEFAULT 0.0,
            enrollment_date DATE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Table 2: Courses
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_code TEXT NOT NULL UNIQUE,
            course_name TEXT NOT NULL,
            credits INTEGER DEFAULT 3,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Table 3: Grades (JOIN table - Stretch Goal)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            grade TEXT NOT NULL,
            score REAL NOT NULL,
            enrolled_date DATE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students (id),
            FOREIGN KEY (course_id) REFERENCES courses (id),
            UNIQUE(student_id, course_id)
        )
    """)

    conn.commit()
    conn.close()
    print(f"✅ Database initialized: {DB_NAME}")


def add_student(name, email, enrollment_date):
    """Req 3: Add new data to database (CREATE)"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO students (name, email, enrollment_date) VALUES (?, ?, ?)",
            (name, email, enrollment_date)
        )
        conn.commit()
        print(f"✅ Student added: {name}")
    except sqlite3.IntegrityError as e:
        print(f"❌ Error: {e}")
    finally:
        conn.close()


def add_course(course_code, course_name, credits=3):
    """Req 3: Add new data to database (CREATE)"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO courses (course_code, course_name, credits) VALUES (?, ?, ?)",
            (course_code, course_name, credits)
        )
        conn.commit()
        print(f"✅ Course added: {course_name}")
    except sqlite3.IntegrityError as e:
        print(f"❌ Error: {e}")
    finally:
        conn.close()


def add_grade(student_id, course_id, grade, score, enrolled_date):
    """Req 3: Add new data to database (CREATE)"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO grades (student_id, course_id, grade, score, enrolled_date) VALUES (?, ?, ?, ?, ?)",
            (student_id, course_id, grade, score, enrolled_date)
        )
        conn.commit()
        print(f"✅ Grade recorded: Student {student_id}, Course {course_id}, Grade: {grade}")
    except sqlite3.IntegrityError as e:
        print(f"❌ Error: {e}")
    finally:
        conn.close()


def query_all_students():
    """Req 2: Query data from database (READ)"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, gpa, enrollment_date FROM students ORDER BY name")
    students = cursor.fetchall()
    conn.close()
    
    print("\n📚 All Students:")
    if students:
        for student in students:
            print(f"  ID: {student[0]}, Name: {student[1]}, Email: {student[2]}, GPA: {student[3]}, Enrolled: {student[4]}")
    else:
        print("  No students found.")
    return students


def query_student_courses(student_id):
    """Req 2: Query with JOIN (Stretch Goal)"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Stretch Goal: JOIN between Students, Grades, and Courses
    cursor.execute("""
        SELECT s.name, c.course_name, c.course_code, g.grade, g.score, g.enrolled_date
        FROM grades g
        JOIN students s ON g.student_id = s.id
        JOIN courses c ON g.course_id = c.id
        WHERE s.id = ?
        ORDER BY g.enrolled_date
    """, (student_id,))
    results = cursor.fetchall()
    conn.close()
    
    if results:
        print(f"\n📖 Courses for {results[0][0]}:")
        for row in results:
            print(f"  {row[1]} ({row[2]}): {row[3]} ({row[4]}) - Enrolled: {row[5]}")
    else:
        print(f"\n📖 No courses found for student ID {student_id}")
    return results


def update_student_gpa(student_id, new_gpa):
    """Req 4: Update data in database (UPDATE)"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE students SET gpa = ? WHERE id = ?", (new_gpa, student_id))
    conn.commit()
    conn.close()
    print(f"✅ Student {student_id} GPA updated to {new_gpa}")


def update_grade(student_id, course_id, new_grade, new_score):
    """Req 4: Update data in database (UPDATE)"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE grades SET grade = ?, score = ? WHERE student_id = ? AND course_id = ?",
        (new_grade, new_score, student_id, course_id)
    )
    conn.commit()
    conn.close()
    print(f"✅ Grade updated: Student {student_id}, Course {course_id} now {new_grade}")


def delete_student(student_id):
    """Req 5: Delete data from database (DELETE)"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # First delete associated grades
    cursor.execute("DELETE FROM grades WHERE student_id = ?", (student_id,))
    # Then delete student
    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
    
    conn.commit()
    conn.close()
    print(f"✅ Student {student_id} and their grades deleted")


def delete_grade(student_id, course_id):
    """Req 5: Delete data from database (DELETE)"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM grades WHERE student_id = ? AND course_id = ?", (student_id, course_id))
    conn.commit()
    conn.close()
    print(f"✅ Grade deleted: Student {student_id}, Course {course_id}")


def aggregate_student_gpa():
    """Stretch Goal: Aggregate function - AVG"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT AVG(gpa) FROM students")
    avg_gpa = cursor.fetchone()[0]
    conn.close()
    
    print(f"\n📊 Class Average GPA: {avg_gpa:.2f}" if avg_gpa else "No GPA data available")
    return avg_gpa


def aggregate_course_stats():
    """Stretch Goal: Aggregate function - COUNT, AVG"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.course_name, COUNT(g.id) as num_students, AVG(g.score) as avg_score
        FROM courses c
        LEFT JOIN grades g ON c.id = g.course_id
        GROUP BY c.id, c.course_name
        ORDER BY avg_score DESC
    """)
    results = cursor.fetchall()
    conn.close()
    
    print("\n📊 Course Statistics:")
    if results:
        for row in results:
            avg = f"{row[2]:.2f}" if row[2] else "N/A"
            print(f"  {row[0]}: {row[1]} students, Avg Score: {avg}")
    return results


def query_grades_by_date_range(start_date, end_date):
    """Stretch Goal: Date/Time filtering"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.name, c.course_name, g.grade, g.enrolled_date
        FROM grades g
        JOIN students s ON g.student_id = s.id
        JOIN courses c ON g.course_id = c.id
        WHERE g.enrolled_date BETWEEN ? AND ?
        ORDER BY g.enrolled_date
    """, (start_date, end_date))
    results = cursor.fetchall()
    conn.close()
    
    print(f"\n📅 Grades enrolled between {start_date} and {end_date}:")
    if results:
        for row in results:
            print(f"  {row[0]} - {row[1]}: {row[2]} ({row[3]})")
    else:
        print("  No grades found in this date range.")
    return results


if __name__ == '__main__':
    # Initialize database
    initialize_database()
    
    # Demo: Add sample data
    print("\n--- ADDING DATA (Req 3: CREATE) ---")
    add_student("Alice Johnson", "alice@example.com", "2025-01-15")
    add_student("Bob Smith", "bob@example.com", "2025-01-16")
    add_student("Carol Davis", "carol@example.com", "2025-01-17")
    
    add_course("CS101", "Introduction to Computer Science", 3)
    add_course("MATH201", "Calculus II", 4)
    add_course("ENG102", "English Composition", 3)
    
    add_grade(1, 1, "A", 95.5, "2025-01-20")
    add_grade(1, 2, "B+", 87.0, "2025-01-21")
    add_grade(2, 1, "A-", 92.0, "2025-01-20")
    add_grade(2, 3, "A", 94.5, "2025-01-22")
    add_grade(3, 2, "B", 85.5, "2025-01-23")
    
    # Query all students
    print("\n--- READING DATA (Req 2: READ) ---")
    query_all_students()
    
    # Query student with courses (JOIN)
    print("\n--- JOINING TABLES (Stretch Goal) ---")
    query_student_courses(1)
    
    # Aggregate functions
    print("\n--- AGGREGATE FUNCTIONS (Stretch Goal) ---")
    aggregate_student_gpa()
    aggregate_course_stats()
    
    # Date range filtering
    print("\n--- DATE RANGE FILTERING (Stretch Goal) ---")
    query_grades_by_date_range("2025-01-20", "2025-01-22")
    
    # Update data
    print("\n--- UPDATING DATA (Req 4: UPDATE) ---")
    update_student_gpa(1, 93.25)
    update_grade(2, 3, "A+", 96.0)
    
    # Delete data
    print("\n--- DELETING DATA (Req 5: DELETE) ---")
    delete_grade(3, 2)
    
    # Final query
    print("\n--- FINAL STATE (All Students) ---")
    query_all_students()
    print("\n✅ SQL Module Demo Complete!")

