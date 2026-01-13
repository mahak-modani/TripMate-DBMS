import pandas as pd
import mysql.connector

# Load the CSV file
df = pd.read_csv("C:\\Users\\Mahak\\Downloads\\USERS_DATA_LOGIN.csv")

# Trim column names and values
df.columns = df.columns.str.strip()  # Remove spaces in column names
df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)  # Trim spaces from string columns

# Standardize date format (Set `dayfirst=False` if needed)
df["join date"] = pd.to_datetime(df["join date"], format="%m/%d/%Y", errors="coerce").dt.strftime("%Y-%m-%d")

# Convert "Gender" to only "M" or "F"
df["gender"] = df["gender"].str.strip().replace({"Male": "M", "Female": "F"})

# Convert age column to numeric and keep valid values
df["age"] = pd.to_numeric(df["age"], errors="coerce")
df = df[(df["age"] > 21) & (df["age"] < 60)]

# MySQL DB connection details
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mahak",
    database="TravelPlanner"
)
cursor = conn.cursor()

# Create table query
table_query = """
CREATE TABLE IF NOT EXISTS users (
    Join_Date DATE NOT NULL,
    User_ID VARCHAR(10) PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Nationality VARCHAR(50),
    Password VARCHAR(8) NOT NULL CHECK (Password REGEXP '^[A-Za-z0-9@_]{8}$'),
    Email VARCHAR(100) UNIQUE NOT NULL,
    Phone_Number CHAR(10) UNIQUE NOT NULL CHECK (Phone_Number REGEXP '^[0-9]{10}$'),
    Age INT CHECK (Age > 21 AND Age < 60) NOT NULL,
    Gender ENUM('M', 'F') NOT NULL
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
"""

# Drop table if exists and create a new one
cursor.execute("DROP TABLE IF EXISTS users")
cursor.execute(table_query)

# Insert data into table
insert_query = """
INSERT INTO users (Join_Date, User_ID, Name, Nationality, Password, Email, Phone_Number, Age, Gender)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

for _, row in df.iterrows():
    cursor.execute(insert_query, (
        row["join date"], 
        row["User_ID"], 
        row["name"], 
        row["nationality"], 
        row["password"], 
        row["email"], 
        row["phone"], 
        row["age"], 
        row["gender"]
    ))

# Commit and close
conn.commit()
cursor.close()
conn.close()

print("Data successfully transferred to MySQL.")
