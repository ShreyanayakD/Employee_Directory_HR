import streamlit as st
import pandas as pd
from backend_hr import (
    get_employees,
    get_departments,
    get_employee_counts,
    get_total_salary_expense,
    get_average_salary,
    get_min_max_salaries,
)

# Set page title and layout
st.set_page_config(page_title="HR Employee Directory & Analytics", layout="wide")
st.title("👨‍💼 HR Employee Directory & Analytics")
st.markdown("---")

# --- Business Insights Section (Aggregations) ---
st.header("📊 Business Insights")
col1, col2, col3 = st.columns(3)

# Get aggregation data
total_employees = get_employee_counts()
total_salary_expense = get_total_salary_expense()
avg_salary = get_average_salary()
min_salary, max_salary = get_min_max_salaries()

with col1:
    st.metric(label="Total Employees", value=total_employees)

with col2:
    st.metric(label="Total Monthly Salary Expense", value=f"${total_salary_expense:,.2f}")

with col3:
    st.metric(label="Average Salary", value=f"${avg_salary:,.2f}")

st.markdown("---")

st.header("💲 Salary Range")
col_min, col_max = st.columns(2)
with col_min:
    if min_salary:
        st.metric(label="Lowest Paid Employee Salary", value=f"${min_salary:,.2f}")
    else:
        st.metric(label="Lowest Paid Employee Salary", value="N/A")
with col_max:
    if max_salary:
        st.metric(label="Highest Paid Employee Salary", value=f"${max_salary:,.2f}")
    else:
        st.metric(label="Highest Paid Employee Salary", value="N/A")

st.markdown("---")

# --- READ & Filtering Section ---
st.header("📝 Employee Directory")

# Get unique departments for the selectbox
departments = ['All'] + get_departments()
selected_department = st.selectbox("Filter by Department", departments)

# Sorting options
sort_options = {
    "None": None,
    "Salary (Descending)": "salary",
    "Hire Date (Descending)": "hire_date",
}
sort_by_selection = st.selectbox("Sort employees by", list(sort_options.keys()))
sort_column = sort_options[sort_by_selection]

# Fetch employees based on filters and sorting
employees_data = get_employees(department=selected_department, sort_by=sort_column)

# Display data using pandas DataFrame
if employees_data:
    df = pd.DataFrame(employees_data, columns=["ID", "First Name", "Last Name", "Department", "Hire Date", "Salary"])
    st.dataframe(df)
else:
    st.info("No employee data to display.")