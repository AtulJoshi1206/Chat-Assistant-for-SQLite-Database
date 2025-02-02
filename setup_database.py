import sqlite3
import os

def create_database():
    # Ensure we start fresh
    if os.path.exists("database.db"):
        os.remove("database.db")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Create Employees table
    cursor.execute('''
        CREATE TABLE Employees (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Department TEXT NOT NULL,
            Salary INTEGER NOT NULL,
            Hire_Date TEXT NOT NULL
        )
    ''')

    # Create Departments table
    cursor.execute('''
        CREATE TABLE Departments (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Manager TEXT NOT NULL
        )
    ''')

    # Insert sample data
    cursor.executemany("INSERT INTO Employees (Name, Department, Salary, Hire_Date) VALUES (?, ?, ?, ?)", [
        ("Alice", "Sales", 50000, "2021-01-15"),
        ("Bob", "Engineering", 70000, "2020-06-10"),
        ("Charlie", "Marketing", 60000, "2022-03-20"),
    ])

    cursor.executemany("INSERT INTO Departments (Name, Manager) VALUES (?, ?)", [
        ("Sales", "Alice"),
        ("Engineering", "Bob"),
        ("Marketing", "Charlie"),
    ])

    conn.commit()
    conn.close()
    print("✅ Database created successfully!")

if __name__ == "__main__":
    create_database()
