import mysql.connector
import csv

# MySQL connection details
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "mahak",
    "database": "TravelPlanner"
}

# Connect to MySQL
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Path to CSV file
csv_file = r"C:\Users\Mahak\Downloads\destinations.csv"

# Read and insert data from CSV file
with open(csv_file, "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader)  # Skip header row

    insert_query = """
    INSERT INTO destinations (destination_id, city, country, avg_cost)
    VALUES (%s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE 
    city = VALUES(city), 
    country = VALUES(country), 
    avg_cost = VALUES(avg_cost);
    """

    valid_data = []
    for row in reader:
        if len(row) == 4:  # Ensure all 4 columns are present
            row = [value if value.strip() else None for value in row]  # Convert empty strings to NULL
            valid_data.append(tuple(row))
        else:
            print(f"Skipping invalid row: {row}")  # Debugging output

    if valid_data:
        cursor.executemany(insert_query, valid_data)
        conn.commit()
        print(f"{cursor.rowcount} rows inserted successfully!")
    else:
        print("No valid data to insert.")

# Close connection
cursor.close()
conn.close()
