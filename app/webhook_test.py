import sqlite3

def run_select_query(query):
    db_path = 'student_performance.db'  # Update path if needed
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    # Example SELECT query
    query = "SELECT * FROM students;"  # Change table/columns as needed
    run_select_query(query)
    
    
def insert_student(name, age, grade):
    db_path = 'student_performance.db'
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO students (name, age, grade) VALUES (?, ?, ?)",
            (name, age, grade)
        )
        conn.commit()
        print("Student inserted successfully.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def update_student(student_id, name=None, age=None, grade=None):
    db_path = 'student_performance.db'
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        updates = []
        params = []
        if name is not None:
            updates.append("name = ?")
            params.append(name)
        if age is not None:
            updates.append("age = ?")
            params.append(age)
        if grade is not None:
            updates.append("grade = ?")
            params.append(grade)
        params.append(student_id)
        sql = f"UPDATE students SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(sql, params)
        conn.commit()
        print("Student updated successfully.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def delete_student(student_id):
    db_path = 'student_performance.db'
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
        conn.commit()
        print("Student deleted successfully.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def get_student(student_id):
    db_path = 'student_performance.db'
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        row = cursor.fetchone()
        print(row)
        return row
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()