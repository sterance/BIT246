"""
 PYTHON + SQLITE CRUD
===========================

This program is designed for beginners using PyCharm.

WHAT WILL WE LEARN?
-------------------
CRUD means:
C = Create -> add new information
R = Read   -> look at information
U = Update -> change information
D = Delete -> remove information

We will use:
Python -> SQLite database -> students table

BEFORE YOU RUN THIS PROGRAM IN PYCHARM
--------------------------------------
1. Open PyCharm.
2. Create a new Python project.
3. Create a new Python file.
4. Paste this code into the file.
5. Open the PyCharm Terminal at the bottom of the screen.
6. Type:

       pip install pandas

7. Press Enter.
8. Run this file using the green Run triangle.

IMPORTANT:
- sqlite3 is already included with Python.
- You do NOT need to install sqlite3.
- A file called school_database.db will be created in your project folder.
- A CSV file called students_from_database.csv will also be created.
"""

# ------------------------------------------------------------
# STEP 1: IMPORT THE TOOLS WE NEED
# ------------------------------------------------------------

# sqlite3 lets Python talk to an SQLite database.
import sqlite3

# pandas helps us display database information like a table.
import pandas as pd

print("\nSTEP 1")
print("Great! Python has loaded the database tools.")


# ------------------------------------------------------------
# STEP 2: CONNECT TO A DATABASE
# ------------------------------------------------------------

# This creates the database file if it does not already exist.
connection = sqlite3.connect("school_database.db")

print("\nSTEP 2")
print("Connected to school_database.db")
print("Look in your PyCharm project folder to find this file.")


# ------------------------------------------------------------
# STEP 3: CREATE A CURSOR
# ------------------------------------------------------------

# A cursor carries SQL instructions from Python to the database.
# Think of it like a messenger.
cursor = connection.cursor()

print("\nSTEP 3")
print("The cursor is ready.")
print("The cursor is like a messenger between Python and the database.")


# ------------------------------------------------------------
# STEP 4: CREATE THE STUDENTS TABLE
# ------------------------------------------------------------

# For a classroom demonstration, we reset the table each time.
# This stops duplicate students appearing every time we press Run.
cursor.execute("DROP TABLE IF EXISTS students")

cursor.execute("""
CREATE TABLE students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    subject TEXT NOT NULL,
    mark INTEGER
)
""")

connection.commit()

print("\nSTEP 4")
print("The students table is ready.")
print("It has four columns: student_id, name, subject and mark.")


# ------------------------------------------------------------
# HELPER FUNCTION: SHOW A QUERY AS A TABLE
# ------------------------------------------------------------

def show_table(sql, params=None, title="Results"):
    """
    Run a SELECT query and print the answer neatly.

    sql    = our SQL question
    params = values used safely inside the SQL question
    title  = heading printed above the answer
    """
    if params is None:
        table = pd.read_sql_query(sql, connection)
    else:
        table = pd.read_sql_query(sql, connection, params=params)

    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

    if table.empty:
        print("There are no records to show.")
    else:
        print(table.to_string(index=False))

    return table


# ------------------------------------------------------------
# CRUD 1: CREATE
# CREATE MEANS "ADD NEW DATA"
# ------------------------------------------------------------

print("\nCRUD 1 - CREATE")
print("CREATE means add new information.")

# Add one student.
cursor.execute(
    "INSERT INTO students (name, subject, mark) VALUES (?, ?, ?)",
    ("Emma", "Python", 85)
)

connection.commit()
print("Emma was added.")


# Add several students.
more_students = [
    ("Noah", "Database", 78),
    ("Mia", "Python", 92),
    ("Oliver", "Cyber Security", 74),
    ("Ava", "Database", 88)
]

cursor.executemany(
    "INSERT INTO students (name, subject, mark) VALUES (?, ?, ?)",
    more_students
)

connection.commit()
print("Four more students were added.")

show_table(
    "SELECT * FROM students",
    title="Students after CREATE"
)


# ------------------------------------------------------------
# CRUD 2: READ
# READ MEANS "LOOK AT DATA"
# ------------------------------------------------------------

print("\nCRUD 2 - READ")
print("READ means look at information stored in the database.")

# Read all columns and all students.
show_table(
    "SELECT * FROM students",
    title="READ 1 - All students"
)

# Read only some columns.
show_table(
    "SELECT name, subject, mark FROM students",
    title="READ 2 - Name, subject and mark only"
)

# Read students with a mark of 80 or higher.
show_table(
    "SELECT * FROM students WHERE mark >= 80",
    title="READ 3 - Marks of 80 or higher"
)

# Read only students studying Python.
show_table(
    "SELECT * FROM students WHERE subject = ?",
    params=("Python",),
    title="READ 4 - Python students"
)


# ------------------------------------------------------------
# CRUD 3: UPDATE
# UPDATE MEANS "CHANGE DATA"
# ------------------------------------------------------------

print("\nCRUD 3 - UPDATE")
print("UPDATE means change information that is already stored.")

# Change Noah's mark from 78 to 82.
cursor.execute(
    "UPDATE students SET mark = ? WHERE name = ?",
    (82, "Noah")
)

connection.commit()
print("Noah's mark was changed to 82.")

show_table(
    "SELECT * FROM students WHERE name = ?",
    params=("Noah",),
    title="Check Noah after UPDATE"
)

# Change Oliver's subject to Python.
cursor.execute(
    "UPDATE students SET subject = ? WHERE name = ?",
    ("Python", "Oliver")
)

connection.commit()
print("Oliver's subject was changed to Python.")

show_table(
    "SELECT * FROM students WHERE name = ?",
    params=("Oliver",),
    title="Check Oliver after UPDATE"
)


# ------------------------------------------------------------
# CRUD 4: DELETE
# DELETE MEANS "REMOVE DATA"
# ------------------------------------------------------------

print("\nCRUD 4 - DELETE")
print("DELETE means remove information.")

cursor.execute(
    "DELETE FROM students WHERE name = ?",
    ("Ava",)
)

connection.commit()
print("Ava was removed from the database.")

show_table(
    "SELECT * FROM students",
    title="Students after DELETE"
)


# ------------------------------------------------------------
# STEP 5: SIMPLE DATABASE QUESTIONS
# ------------------------------------------------------------

show_table(
    "SELECT COUNT(*) AS total_students FROM students",
    title="How many students are there?"
)

show_table(
    "SELECT ROUND(AVG(mark), 2) AS average_mark FROM students",
    title="What is the average mark?"
)

show_table(
    """
    SELECT subject, ROUND(AVG(mark), 2) AS average_mark
    FROM students
    GROUP BY subject
    ORDER BY average_mark DESC
    """,
    title="Average mark for each subject"
)

show_table(
    "SELECT * FROM students ORDER BY mark DESC",
    title="Students sorted from highest mark to lowest mark"
)


# ------------------------------------------------------------
# STEP 6: USE A PYTHON VARIABLE IN AN SQL QUESTION
# ------------------------------------------------------------

minimum_mark = 80

show_table(
    "SELECT * FROM students WHERE mark >= ?",
    params=(minimum_mark,),
    title=f"Students with a mark of {minimum_mark} or higher"
)


# ------------------------------------------------------------
# STEP 7: ADD LIAM USING PYTHON VARIABLES
# ------------------------------------------------------------

student_name = "Liam"
student_subject = "Python"
student_mark = 90

cursor.execute(
    "INSERT INTO students (name, subject, mark) VALUES (?, ?, ?)",
    (student_name, student_subject, student_mark)
)

connection.commit()

print("\nLiam was added using Python variables.")


# ------------------------------------------------------------
# STEP 8: SAVE THE FINAL TABLE TO A CSV FILE
# ------------------------------------------------------------

final_table = show_table(
    "SELECT * FROM students",
    title="Final students table"
)

final_table.to_csv(
    "students_from_database.csv",
    index=False
)

print("\nstudents_from_database.csv was created.")
print("Look for it in your PyCharm project folder.")


# ------------------------------------------------------------
# MINI CHALLENGE ANSWERS
# ------------------------------------------------------------

show_table(
    "SELECT * FROM students ORDER BY mark DESC LIMIT 1",
    title="Mini Challenge 1 - Highest mark"
)

show_table(
    "SELECT * FROM students ORDER BY mark ASC LIMIT 1",
    title="Mini Challenge 2 - Lowest mark"
)

show_table(
    "SELECT COUNT(*) AS python_students FROM students WHERE subject = ?",
    params=("Python",),
    title="Mini Challenge 3 - Number of Python students"
)

show_table(
    "SELECT ROUND(AVG(mark), 2) AS python_average FROM students WHERE subject = ?",
    params=("Python",),
    title="Mini Challenge 4 - Average Python mark"
)


# ------------------------------------------------------------
# STUDENT PRACTICE
# ------------------------------------------------------------

print("""
============================================================
STUDENT PRACTICE
============================================================

Try changing the code or adding your own code.

Task 1:
Add Sophie.
Subject: Database
Mark: 86

Task 2:
Display all students.

Task 3:
Show students with marks above 85.

Task 4:
Change Sophie's mark to 91.

Task 5:
Delete Sophie.

Remember:
CREATE = INSERT
READ   = SELECT
UPDATE = UPDATE
DELETE = DELETE
""")


# ------------------------------------------------------------
# FINAL STEP: CLOSE THE DATABASE
# ------------------------------------------------------------

# We close the connection when our work is finished.
connection.close()

print("\nDatabase connection closed.")
print("Excellent work! You have completed the SQLite CRUD lesson.")
