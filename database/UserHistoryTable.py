import mysql.connector
import pandas as pd

# Database connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mahak",  # Update this with your MySQL password
    database="TravelPlanner"
)
cursor = conn.cursor()

# Read data from CSV
file_path = r"C:\Users\Mahak\OneDrive\Desktop\DBS Project\database\user_history.csv"
df = pd.read_csv(file_path)

# Convert date format from YYYY:MM:DD to YYYY-MM-DD
df['start_date'] = df['start_date'].str.replace(":", "-")
df['end_date'] = df['end_date'].str.replace(":", "-")

# Insert Data into User_History table
for index, row in df.iterrows():
    try:
        insert_query = """
        INSERT INTO User_History 
        (trip_id, destination_id, start_date, end_date, user_id, accommodation_type, 
        accommodation_cost, transportation_type, transportation_cost, budget) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            row['trip_id'],
            row['destination_id'],
            row['start_date'],   # Already formatted as YYYY-MM-DD
            row['end_date'],
            row['user_id'],
            row['accommodation_type'],
            row['accommodation_cost'],
            row['transportation_type'],
            row['transportation_cost'],
            row['budget']
        )
        cursor.execute(insert_query, values)
    
    except mysql.connector.Error as err:
        print(f"❌ Error inserting row {index}: {err}")

# Commit changes
conn.commit()

# Verify if data was inserted
cursor.execute("SELECT COUNT(*) FROM User_History;")
count = cursor.fetchone()[0]
if count > 0:
    print(f"✅ Data inserted successfully! Total Rows: {count}")
else:
    print("⚠️ No data inserted! Check constraints or foreign keys.")

# Close connection
cursor.close()
conn.close()
