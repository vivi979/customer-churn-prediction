import sqlite3

conn = sqlite3.connect('churn.db')
cursor = conn.cursor()

# 1. Customers table
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cname TEXT,
    tenure INTEGER,
    monthly_charges REAL,
    contract TEXT,
    payment_method TEXT,
    internet_service TEXT,
    has_internet TEXT,
    tech_support TEXT,
    online_security TEXT
)
""")

# 2. Predictions table
cursor.execute("""
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    prediction_result TEXT,
    churn_probability REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
)
""")

# 3. Employees table
cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ename TEXT,
    email TEXT UNIQUE,
    password TEXT,
    role TEXT DEFAULT 'analyst',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# 4. Logs table
cursor.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER,
    action TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print("Database and tables created successfully!")