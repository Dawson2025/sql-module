# SQL Module - Student Grade Management System

A comprehensive Python application demonstrating all 5 SQL requirements using SQLite and the sqlite3 library.

## Module Requirements Met ✅

### 1. Create a SQL Database with Tables ✅
**Location**: [`main.py` lines 24-70](cursor://file/c:/dev/sql-module/main.py:24:1)

Creates 3 interconnected tables:
- **Students Table**: Stores student information with unique constraints
- **Courses Table**: Stores course information with credits
- **Grades Table**: Junction table linking Students to Courses with FOREIGN KEYs

**Evidence**: `initialize_database()` function creates all 3 tables with relationships

---

### 2. Query Data from Database (READ) ✅
**Location**: [`main.py` lines 151-167](cursor://file/c:/dev/sql-module/main.py:151:1)

Multiple query functions:
- [`query_all_students()`](cursor://file/c:/dev/sql-module/main.py:151:1) - Basic SELECT query
- [`query_student_courses()`](cursor://file/c:/dev/sql-module/main.py:170:1) - JOIN query (Stretch Goal)
- [`query_grades_by_date_range()`](cursor://file/c:/dev/sql-module/main.py:229:1) - Date filtering

**Examples**:
```python
# Simple SELECT
cursor.execute("SELECT id, name, email, gpa FROM students")

# JOIN between 3 tables (Stretch Goal)
cursor.execute("""
    SELECT s.name, c.course_name, g.grade, g.score
    FROM grades g
    JOIN students s ON g.student_id = s.id
    JOIN courses c ON g.course_id = c.id
""")

# Date range filtering (Stretch Goal)
cursor.execute("""
    SELECT * FROM grades 
    WHERE enrolled_date BETWEEN ? AND ?
""", (start_date, end_date))
```

---

### 3. Add New Data to Database (CREATE) ✅
**Location**: [`main.py` lines 74-120](cursor://file/c:/dev/sql-module/main.py:74:1)

Three CREATE functions:
- [`add_student()`](cursor://file/c:/dev/sql-module/main.py:74:1) - Insert into students table
- [`add_course()`](cursor://file/c:/dev/sql-module/main.py:86:1) - Insert into courses table
- [`add_grade()`](cursor://file/c:/dev/sql-module/main.py:98:1) - Insert into grades table

**Security**: All use parameterized queries (?) to prevent SQL injection
**Error Handling**: IntegrityError catches duplicate entries (UNIQUE constraints)

---

### 4. Update Data in Database (UPDATE) ✅
**Location**: [`main.py` lines 188-207](cursor://file/c:/dev/sql-module/main.py:188:1)

Two UPDATE functions:
- [`update_student_gpa()`](cursor://file/c:/dev/sql-module/main.py:188:1) - Update GPA field
- [`update_grade()`](cursor://file/c:/dev/sql-module/main.py:198:1) - Update grade and score

**Examples**:
```python
# Update single column
cursor.execute("UPDATE students SET gpa = ? WHERE id = ?", (new_gpa, student_id))

# Update multiple columns
cursor.execute(
    "UPDATE grades SET grade = ?, score = ? WHERE student_id = ? AND course_id = ?",
    (new_grade, new_score, student_id, course_id)
)
```

---

### 5. Delete Data from Database (DELETE) ✅
**Location**: [`main.py` lines 210-227](cursor://file/c:/dev/sql-module/main.py:210:1)

Two DELETE functions:
- [`delete_student()`](cursor://file/c:/dev/sql-module/main.py:210:1) - Delete student AND their grades
- [`delete_grade()`](cursor://file/c:/dev/sql-module/main.py:220:1) - Delete single grade record

**Cascade behavior**: Deleting a student also deletes their associated grades (data integrity)

---

## Stretch Challenges Completed ✅

### Stretch 1: Multiple Tables with JOIN ✅
**Location**: [`main.py` lines 170-188](cursor://file/c:/dev/sql-module/main.py:170:1)

Demonstrates 3-table JOIN:
```sql
SELECT s.name, c.course_name, c.course_code, g.grade, g.score
FROM grades g
JOIN students s ON g.student_id = s.id
JOIN courses c ON g.course_id = c.id
```

**How to test**:
```bash
python3 main.py
# See "Courses for Alice Johnson" output showing JOIN results
```

### Stretch 2: Aggregate Functions ✅
**Location**: [`main.py` lines 228-256](cursor://file/c:/dev/sql-module/main.py:228:1)

Uses two aggregate functions:

**AVG (Average)**:
```sql
SELECT AVG(gpa) FROM students
SELECT AVG(g.score) FROM grades g
```

**COUNT**:
```sql
SELECT COUNT(g.id) as num_students FROM grades g
GROUP BY c.id
```

**Grouping with Multiple Aggregates**:
```sql
SELECT c.course_name, COUNT(g.id), AVG(g.score)
FROM courses c
LEFT JOIN grades g
GROUP BY c.id
```

### Stretch 3: Date/Time Filtering ✅
**Location**: [`main.py` lines 229-256](cursor://file/c:/dev/sql-module/main.py:229:1)

Demonstrates date range filtering:
```sql
SELECT * FROM grades
WHERE enrolled_date BETWEEN ? AND ?
ORDER BY enrolled_date
```

**Features**:
- Stores dates as TEXT (ISO format: YYYY-MM-DD)
- BETWEEN operator for range queries
- ORDER BY for sorting results

---

## Database Schema

```
Students Table
├── id (PRIMARY KEY)
├── name (UNIQUE)
├── email (UNIQUE)
├── gpa (REAL)
├── enrollment_date (DATE)
└── created_at (TIMESTAMP)

Courses Table
├── id (PRIMARY KEY)
├── course_code (UNIQUE)
├── course_name
├── credits (INTEGER)
└── created_at (TIMESTAMP)

Grades Table (Junction/Join Table)
├── id (PRIMARY KEY)
├── student_id (FOREIGN KEY → Students)
├── course_id (FOREIGN KEY → Courses)
├── grade (TEXT: A, B+, B, etc)
├── score (REAL: 95.5, 87.0, etc)
├── enrolled_date (DATE)
└── created_at (TIMESTAMP)
```

---

## Quick Start

### Installation
```bash
# No external dependencies required!
# Python 3.6+ has sqlite3 built-in
python3 main.py
```

### Expected Output
```
✅ Database initialized: data/grades.db

--- ADDING DATA (Req 3: CREATE) ---
✅ Student added: Alice Johnson
✅ Student added: Bob Smith
✅ Course added: Introduction to Computer Science
✅ Grade recorded: Student 1, Course 1, Grade: A

--- READING DATA (Req 2: READ) ---
📚 All Students:
  ID: 1, Name: Alice Johnson, Email: alice@example.com, GPA: 0.0, Enrolled: 2025-01-15
  ID: 2, Name: Bob Smith, Email: bob@example.com, GPA: 0.0, Enrolled: 2025-01-16

--- JOINING TABLES (Stretch Goal) ---
📖 Courses for Alice Johnson:
  Introduction to Computer Science (CS101): A (95.5) - Enrolled: 2025-01-20

--- AGGREGATE FUNCTIONS (Stretch Goal) ---
📊 Class Average GPA: 93.25
📊 Course Statistics:
  Introduction to Computer Science: 2 students, Avg Score: 93.75

--- DATE RANGE FILTERING (Stretch Goal) ---
📅 Grades enrolled between 2025-01-20 and 2025-01-22:
  Alice Johnson - Introduction to Computer Science: A (2025-01-20)

--- UPDATING DATA (Req 4: UPDATE) ---
✅ Student 1 GPA updated to 93.25

--- DELETING DATA (Req 5: DELETE) ---
✅ Grade deleted: Student 3, Course 2

✅ SQL Module Demo Complete!
```

---

## Key Concepts Demonstrated

### SQL Security
- **Parameterized Queries**: All SQL uses `(?, ?)` placeholders, never string concatenation
- **Prevents SQL Injection**: `cursor.execute("SELECT * WHERE id = ?", (user_input,))`

### Data Integrity
- **UNIQUE Constraints**: Prevent duplicate students/courses
- **FOREIGN KEYs**: Maintain referential integrity between tables
- **UNIQUE(student_id, course_id)**: Prevent duplicate grades for same student+course

### SQL Operations
- **CREATE**: Insert operations with error handling
- **READ**: SELECT with WHERE, ORDER BY, GROUP BY, JOIN, BETWEEN
- **UPDATE**: Modify existing records
- **DELETE**: Remove records with cascade behavior

### Advanced Features
- **JOINs**: 3-table JOIN between Students, Grades, Courses
- **Aggregate Functions**: COUNT, AVG with GROUP BY
- **Date Operations**: Store, query, and filter dates

---

## Tech Stack
- **Language**: Python 3
- **Database**: SQLite3
- **Library**: sqlite3 (built-in)

---

## Project Files
- `main.py` - Application with all 5 requirements + stretch goals
- `README.md` - This documentation
- `data/grades.db` - SQLite database (auto-created)

---

## Status
✅ **Complete** - All 5 requirements met with all 3 stretch challenges implemented

