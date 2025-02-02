import sqlite3
import re

def process_query(user_input):
    # Connect to the SQLite database
    conn = sqlite3.connect(r"D:\project sql\sqlite-chat-assistant\database.db")
    cursor = conn.cursor()

    # Normalize the input for easier matching
    query = user_input.lower().strip()

    # 1. Show all employees in a specific department
    m = re.search(r'show me all employees in (?:the )?([\w\s]+) department', query)
    if m:
        department = m.group(1).strip()
        cursor.execute("SELECT Name FROM Employees WHERE Department=?", (department,))
        rows = cursor.fetchall()
        if rows:
            names = ", ".join(row[0] for row in rows)
            return f"Employees in the {department} department: {names}"
        else:
            return f"No employees found in the {department} department."

    # 2. Who is the manager of a specific department?
    m = re.search(r'who is the manager of (?:the )?([\w\s]+) department', query)
    if m:
        department = m.group(1).strip()
        cursor.execute("SELECT Manager FROM Departments WHERE Name=?", (department,))
        row = cursor.fetchone()
        if row:
            return f"The manager of the {department} department is {row[0]}."
        else:
            return f"Department not found: {department}"

    # 3. List all employees hired after a specific date
    m = re.search(r'list all employees hired after ([\d]{4}-[\d]{2}-[\d]{2})', query)
    if m:
        date = m.group(1).strip()
        cursor.execute("SELECT Name FROM Employees WHERE Hire_Date > ?", (date,))
        rows = cursor.fetchall()
        if rows:
            names = ", ".join(row[0] for row in rows)
            return f"Employees hired after {date}: {names}"
        else:
            return f"No employees found that were hired after {date}."

    # 4. What is the total salary expense for a specific department?
    m = re.search(r'what is the total salary expense for (?:the )?([\w\s]+) department', query)
    if m:
        department = m.group(1).strip()
        cursor.execute("SELECT SUM(Salary) FROM Employees WHERE Department=?", (department,))
        row = cursor.fetchone()
        if row and row[0] is not None:
            total = f"${row[0]:,.2f}"
            return f"Total salary expense for the {department} department is {total}."
        else:
            return f"Salary expense information not found for the {department} department."

    # 5. What are the departments?
    m = re.search(r'what are the departments', query)
    if m:
        cursor.execute("SELECT Name FROM Departments")
        rows = cursor.fetchall()
        if rows:
            departments = ", ".join(row[0] for row in rows)
            return f"Departments: {departments}"
        else:
            return "No departments found."

    # 6. What is the average salary in a specific department?
    m = re.search(r'what is the average salary (?:in|for) (?:the )?([\w\s]+) department', query)
    if m:
        department = m.group(1).strip()
        cursor.execute("SELECT AVG(Salary) FROM Employees WHERE Department=?", (department,))
        row = cursor.fetchone()
        if row and row[0] is not None:
            avg_salary = f"${row[0]:,.2f}"
            return f"The average salary in the {department} department is {avg_salary}."
        else:
            return f"Average salary information not available for the {department} department."

    # 7. What is the average salary in the company?
    m = re.search(r'what is the average salary (?:across|in) (?:the )?company', query)
    if m:
        cursor.execute("SELECT AVG(Salary) FROM Employees")
        row = cursor.fetchone()
        if row and row[0] is not None:
            avg_salary = f"${row[0]:,.2f}"
            return f"The average salary across the company is {avg_salary}."
        else:
            return "Average salary information not available for the company."

    # 8. How many employees are in a specific department?
    m = re.search(r'how many employees (?:are there in|in) (?:the )?([\w\s]+) department', query)
    if m:
        department = m.group(1).strip()
        cursor.execute("SELECT COUNT(*) FROM Employees WHERE Department=?", (department,))
        row = cursor.fetchone()
        if row:
            count = row[0]
            return f"There are {count} employees in the {department} department."
        else:
            return f"Information about the {department} department not found."

    # 9. What is the salary of [employee name]?
    m = re.search(r'what is the salary of ([\w\s]+)', query)
    if m:
        name = m.group(1).strip()
        cursor.execute("SELECT Salary FROM Employees WHERE Name=?", (name,))
        row = cursor.fetchone()
        if row:
            salary = f"${row[0]:,.2f}"
            return f"{name}'s salary is {salary}."
        else:
            return f"No salary information found for {name}."

    return "Sorry, I didn't understand the query. Please try rephrasing."

# Example usage
while True:
    user_input = input("Ask a question: ")
    if user_input.lower() == "exit":
        break
    response = process_query(user_input)
    print(response)
