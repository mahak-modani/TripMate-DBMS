import mysql.connector
import pandas as pd

# Database connection settings
db_config = {
    "host": "localhost",  # Change to your MySQL host
    "user": "root",       # Change to your MySQL username
    "password": "mahak",  # Change to your MySQL password
    "database": "TravelPlanner"   # Change to your database name
}

# Read CSV data
csv_file = "C:\\Users\\Mahak\\OneDrive\\Desktop\\transport.csv"
df = pd.read_csv(csv_file)

# Define allowed transport modes
valid_transport_modes = ['Metro', 'Cab', 'Auto']

# Clean the 'transport_mode' column and ensure it only has valid values
df['transport_mode'] = df['transport_mode'].str.strip()  # Remove leading/trailing spaces
df['transport_mode'] = df['transport_mode'].apply(lambda x: x if x in valid_transport_modes else None)

# Remove rows with invalid transport modes (if necessary)
df = df.dropna(subset=['transport_mode'])

try:
    # Connect to MySQL
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Insert data into the transport table
    insert_query = """
    INSERT INTO transport (from_area, to_area, transport_mode, travel_time_minutes, fare)
    VALUES (%s, %s, %s, %s, %s)
    """

    for _, row in df.iterrows():
        cursor.execute(insert_query, tuple(row))

    # Commit the transaction
    conn.commit()
    print(f"{cursor.rowcount} rows inserted successfully.")

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    cursor.close()
    conn.close()
