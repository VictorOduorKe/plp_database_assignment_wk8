#-----importing the create_db_connection and close_db_connection functions from db_connection.py file----
from db_connection import create_db_connection, close_db_connection

# ----------------- TABLE CREATION -----------------
def create_tables():
    connection = create_db_connection()
    if connection is None:
        return
    cursor = connection.cursor()
    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS departments (
            id INT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            location VARCHAR(100)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            id INT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            description VARCHAR(255)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            age INT,
            department_id INT,
            FOREIGN KEY (department_id) REFERENCES departments(id)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS teachers (
            id INT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            department_id INT,
            subject_id INT,
            FOREIGN KEY (department_id) REFERENCES departments(id),
            FOREIGN KEY (subject_id) REFERENCES subjects(id)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            department_id INT,
            descriptions VARCHAR(255),
            subject_id INT,
            FOREIGN KEY (department_id) REFERENCES departments(id),
            FOREIGN KEY (subject_id) REFERENCES subjects(id)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS enrollments (
            id INT PRIMARY KEY,
            student_id INT,
            course_id INT,
            enrollment_date DATE,
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (course_id) REFERENCES courses(id)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS grades (
            id INT AUTO_INCREMENT PRIMARY KEY,
            enrollment_id INT,
            grade VARCHAR(2),
            FOREIGN KEY (enrollment_id) REFERENCES enrollments(id)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS students_subjects (
            student_id INT,
            subject_id INT,
            PRIMARY KEY (student_id, subject_id),
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (subject_id) REFERENCES subjects(id)
        )
        """)
        connection.commit()
        print("✅ All tables created successfully.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        close_db_connection(connection)

# ----------------- INSERT FUNCTIONS -----------------
def insert_department():
    data = [
        (1, 'Finance', 'Downtown'),
        (2, 'IT', 'Midtown'),
        (3, 'Marketing', 'Uptown'),
        (4, 'HR', 'Upper East Side')
    ]
    insert_data("departments", data)

def insert_subject():
    data = [
        (1, 'Mathematics', 'Study of numbers and shapes'),
        (2, 'Physics', 'Study of matter and energy'),
        (3, 'Chemistry', 'Study of substances and reactions'),
        (4, 'Biology', 'Study of living organisms')
    ]
    insert_data("subjects", data)

def insert_student():
    data = [
        (1, 'Alice', 20, 1),
        (2, 'Bob', 22, 2),
        (3, 'Charlie', 21, 3),
        (4, 'David', 23, 1)
    ]
    insert_data("students", data)

def insert_teacher():
    data = [
        (1, 'Mr. Smith', 1, 1),
        (2, 'Ms. Johnson', 2, 2),
        (3, 'Dr. Brown', 3, 3),
        (4, 'Prof. Davis', 4, 4)
    ]
    insert_data("teachers", data)

def insert_course():
    data = [
        (1, 'ICT', 1, 'Advanced computing courses', 1),
        (2, 'ENGINEERING', 2, 'Study of motion and forces', 2),
        (3, 'Health Science', 3, 'Study of human health and its environment', 3),
        (4, 'Business', 4, 'Study of Economics', 4)
    ]
    insert_data("courses", data)

def insert_enrollment():
    data = [
        (1, 1, 1, '2023-01-15'),
        (2, 2, 2, '2023-02-20'),
        (3, 3, 3, '2023-03-10'),
        (4, 4, 4, '2023-04-05')
    ]
    insert_data("enrollments", data)

def insert_data(table, rows):
    connection = create_db_connection()
    if connection is None:
        return
    cursor = connection.cursor()
    try:
        for row in rows:
            placeholders = ", ".join(["%s"] * len(row))
            query = f"INSERT IGNORE INTO {table} VALUES ({placeholders})"
            cursor.execute(query, row)
        connection.commit()
        print(f"✅ Data inserted into {table}")
    except Error as e:
        print(f"Error inserting into {table}: {e}")
    finally:
        cursor.close()
        close_db_connection(connection)

# ----------------- RELATIONSHIP FUNCTIONS -----------------
def assign_subject_to_student(student_id, subject_id):
    connection = create_db_connection()
    if connection is None:
        return
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT IGNORE INTO students_subjects (student_id, subject_id) VALUES (%s, %s)", (student_id, subject_id))
        connection.commit()
        print(f"✅ Assigned Subject {subject_id} to Student {student_id}")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        close_db_connection(connection)

def assign_grade(student_id, course_id, grade):
    connection = create_db_connection()
    if connection is None:
        return
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT id FROM enrollments WHERE student_id=%s AND course_id=%s", (student_id, course_id))
        enrollment = cursor.fetchone()
        if not enrollment:
            print(f"⚠️ Student {student_id} not enrolled in course {course_id}")
            return
        enrollment_id = enrollment[0]
        cursor.execute("INSERT INTO grades (enrollment_id, grade) VALUES (%s, %s)", (enrollment_id, grade))
        connection.commit()
        print(f"✅ Grade {grade} assigned to Student {student_id} for Course {course_id}")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        close_db_connection(connection)

# ----------------- VIEW FUNCTIONS -----------------
def view_students_grades():
    connection = create_db_connection()
    cursor = connection.cursor()
    try:
        query = """
        SELECT s.id, s.name, c.name, g.grade
        FROM students s
        JOIN enrollments e ON s.id = e.student_id
        JOIN courses c ON e.course_id = c.id
        LEFT JOIN grades g ON e.id = g.enrollment_id
        """
        cursor.execute(query)
        for row in cursor.fetchall():
            print(f"Student ID: {row[0]}, Name: {row[1]}, Course: {row[2]}, Grade: {row[3]}")
    finally:
        cursor.close()
        close_db_connection(connection)

def view_teachers_subjects():
    connection = create_db_connection()
    cursor = connection.cursor()
    try:
        query = """
        SELECT t.id, t.name, d.name, s.name
        FROM teachers t
        JOIN departments d ON t.department_id = d.id
        JOIN subjects s ON t.subject_id = s.id
        """
        cursor.execute(query)
        for row in cursor.fetchall():
            print(f"Teacher ID: {row[0]}, Name: {row[1]}, Department: {row[2]}, Subject: {row[3]}")
    finally:
        cursor.close()
        close_db_connection(connection)

def view_courses_departments():
    connection = create_db_connection()
    cursor = connection.cursor()
    try:
        query = """
        SELECT c.id, c.name, d.name
        FROM courses c
        JOIN departments d ON c.department_id = d.id
        """
        cursor.execute(query)
        for row in cursor.fetchall():
            print(f"Course ID: {row[0]}, Name: {row[1]}, Department: {row[2]}")
    finally:
        cursor.close()
        close_db_connection(connection)
        
# ----------------- DELETE FUNCTION ----------------- 
from mysql.connector import Error

def delete_student(student_id):
    connection = create_db_connection()
    if connection is None:
        return
    cursor = connection.cursor()
    try:
        # Step 1: Delete grades linked to the student's enrollments
        cursor.execute("""
            DELETE g FROM grades g
            JOIN enrollments e ON g.enrollment_id = e.id
            WHERE e.student_id = %s
        """, (student_id,))

        # Step 2: Delete enrollments linked to the student
        cursor.execute("DELETE FROM enrollments WHERE student_id=%s", (student_id,))

        # Step 3: Delete from students_subjects (many-to-many table)
        cursor.execute("DELETE FROM students_subjects WHERE student_id=%s", (student_id,))

        # Step 4: Delete the student
        cursor.execute("DELETE FROM students WHERE id=%s", (student_id,))

        connection.commit()
        print(f"✅ Student {student_id} and related records deleted")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        close_db_connection(connection)

#----function to update student details----
def update_student(student_id, name=None, age=None, department_id=None):
    connection = create_db_connection()
    if connection is None:
        return
    cursor = connection.cursor()
    try:
        updates = []
        params = []
        if name:
            updates.append("name=%s")
            params.append(name)
        if age:
            updates.append("age=%s")
            params.append(age)
        if department_id:
            updates.append("department_id=%s")
            params.append(department_id)
        params.append(student_id)
        if updates:
            query = f"UPDATE students SET {', '.join(updates)} WHERE id=%s"
            cursor.execute(query, params)
            connection.commit()
            print(f"✅ Student {student_id} updated")
        else:
            print("⚠️ No fields to update")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        close_db_connection(connection)

# ----------------- MAIN -----------------
if __name__ == "__main__":
    create_tables()
    insert_department()
    insert_subject()
    insert_student()
    insert_teacher()
    insert_course()
    insert_enrollment()

    assign_subject_to_student(1, 2)
    assign_subject_to_student(2, 3)
    assign_subject_to_student(3, 1)
    assign_subject_to_student(4, 4)

    assign_grade(1, 1, 'A')
    assign_grade(2, 2, 'B')
    assign_grade(3, 3, 'A')
    assign_grade(4, 4, 'C')

    print("\n--- Student Grades ---")
    view_students_grades()
    print("\n--- Teachers & Subjects ---")
    view_teachers_subjects()
    print("\n--- Courses & Departments ---")
    view_courses_departments()
    delete_student(4)  # Example usage
    update_student(3, name="Charles", age=22)  # Example usage