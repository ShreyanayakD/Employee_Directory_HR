import psycopg2
import streamlit as st

# Database connection details
DB_HOST = "localhost"
DB_NAME = "Employee_Directory"
DB_USER = "postgres"
DB_PASS = "Nayak"

def get_db_connection():
    """Establishes a connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="Employee_Directory",
            user="postgres",
            password="Nayak"
        )
        return conn
    except psycopg2.OperationalError as e:
        st.error(f"Database connection error: {e}")
        return None

# --- CRUD Operations ---

def create_employee(first_name, last_name, department, hire_date, salary):
    """(C)reate a new employee record."""
    conn = get_db_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO employees (first_name, last_name, department, hire_date, salary) VALUES (%s, %s, %s, %s, %s)",
                (first_name, last_name, department, hire_date, salary)
            )
            conn.commit()
        conn.close()

def get_employees(department=None, sort_by=None, sort_order='DESC'):
    """(R)ead employee records with optional filtering and sorting."""
    conn = get_db_connection()
    if conn:
        with conn.cursor() as cur:
            query = "SELECT employee_id, first_name, last_name, department, hire_date, salary FROM employees"
            params = []
            
            if department and department != 'All':
                query += " WHERE department = %s"
                params.append(department)
            
            if sort_by:
                query += f" ORDER BY {sort_by} {sort_order}"

            cur.execute(query, params)
            employees = cur.fetchall()
            return employees
    return []

def update_employee_salary(employee_id, new_salary):
    """(U)pdate an existing employee's salary."""
    conn = get_db_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE employees SET salary = %s WHERE employee_id = %s",
                (new_salary, employee_id)
            )
            conn.commit()
        conn.close()

def delete_employee(employee_id):
    """(D)elete an employee record."""
    conn = get_db_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM employees WHERE employee_id = %s", (employee_id,))
            conn.commit()
        conn.close()

# --- Analytics & Business Insights ---

def get_employee_counts():
    """(COUNT) Get the total number of employees."""
    conn = get_db_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM employees")
            count = cur.fetchone()[0]
            return count
    return 0

def get_total_salary_expense():
    """(SUM) Get the total monthly salary expense."""
    conn = get_db_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute("SELECT SUM(salary) FROM employees")
            total = cur.fetchone()[0]
            return total if total else 0.00
    return 0.00

def get_average_salary():
    """(AVG) Get the average salary."""
    conn = get_db_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute("SELECT AVG(salary) FROM employees")
            avg = cur.fetchone()[0]
            return avg if avg else 0.00
    return 0.00

def get_min_max_salaries():
    """(MIN/MAX) Get the minimum and maximum salaries."""
    conn = get_db_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute("SELECT MIN(salary), MAX(salary) FROM employees")
            min_sal, max_sal = cur.fetchone()
            return min_sal, max_sal
    return None, None

def get_departments():
    """(Helper) Get a list of all unique departments."""
    conn = get_db_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute("SELECT DISTINCT department FROM employees")
            departments = [row[0] for row in cur.fetchall()]
            return departments
    return []