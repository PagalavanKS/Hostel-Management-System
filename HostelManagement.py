import sqlite3
import streamlit as st

# Database functions
def create_connection():
    conn = sqlite3.connect('hostel_management.db')
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        age INTEGER NOT NULL,
                        room_number TEXT NOT NULL
                      )''')
    conn.commit()
    conn.close()

def add_student(name, age, room_number):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO students (name, age, room_number) VALUES (?, ?, ?)', (name, age, room_number))
    conn.commit()
    conn.close()

def get_students():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students')
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_student(student_id, name, age, room_number):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE students SET name = ?, age = ?, room_number = ? WHERE id = ?', (name, age, room_number, student_id))
    conn.commit()
    conn.close()

def delete_student(student_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
    conn.commit()
    conn.close()

# Initialize database
create_table()

# Streamlit App
def main():
    st.title("Hostel Management System")
    
    menu = ["Create", "Read", "Update", "Delete"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "Create":
        st.subheader("Add Student")
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=1)
        room_number = st.text_input("Room Number")
        
        if st.button("Add"):
            add_student(name, age, room_number)
            st.success(f"Added {name} to the database")
    
    elif choice == "Read":
        st.subheader("View Students")
        students = get_students()
        
        for student in students:
            st.text(f"ID: {student[0]}")
            st.text(f"Name: {student[1]}")
            st.text(f"Age: {student[2]}")
            st.text(f"Room Number: {student[3]}")
            st.text("---")
    
    elif choice == "Update":
        st.subheader("Update Student")
        students = get_students()
        student_dict = {student[0]: student for student in students}
        
        selected_id = st.selectbox("Select Student", list(student_dict.keys()))
        selected_student = student_dict[selected_id]
        
        name = st.text_input("Name", value=selected_student[1])
        age = st.number_input("Age", value=selected_student[2], min_value=1)
        room_number = st.text_input("Room Number", value=selected_student[3])
        
        if st.button("Update"):
            update_student(selected_id, name, age, room_number)
            st.success(f"Updated student with ID {selected_id}")
    
    elif choice == "Delete":
        st.subheader("Delete Student")
        students = get_students()
        student_dict = {student[0]: student for student in students}
        
        selected_id = st.selectbox("Select Student", list(student_dict.keys()))
        
        if st.button("Delete"):
            delete_student(selected_id)
            st.success(f"Deleted student with ID {selected_id}")

if __name__ == '__main__':
    main()
