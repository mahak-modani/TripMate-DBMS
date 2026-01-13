import pandas as pd
import mysql.connector
import re
import numpy as np

# MySQL Config
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "mahak",
    "database": "TravelPlanner"
}

# Read CSV
file_path = "C:\\Users\\Mahak\\OneDrive\\Desktop\\DBS Project\\Attractions.csv"
df = pd.read_csv(file_path)

# Rename Columns (Short & Clean)
df.rename(columns={
    "ID": "id", "Zone": "zone", "State": "state", "City": "city", "Name": "name",
    "Type": "type", "Establishment Year": "year", "time needed to visit in hrs": "time_hr",
    "Google review rating": "rating", "Entrance Fee in INR": "fee", "Airport with 50km Radius": "airport_50km",
    "Weekly Off": "weekly_off", "Significance": "significance", "Best Time to visit": "best_time"
}, inplace=True)

# Function to Clean Text Fields (Trims Extra Spaces & Fixes Formatting)
def clean_text(value):
    if pd.isna(value):
        return None
    if isinstance(value, str):
        return " ".join(value.split())  # Remove extra spaces
    return value

df = df.applymap(clean_text)

# Convert 'year' to INT, replace 'Unknown' with NULL
df["year"] = df["year"].apply(lambda x: int(x) if str(x).isdigit() else None)

# Extract Best Time (Months & Day)
def extract_best_time(value):
    if pd.isna(value) or not isinstance(value, str):
        return None, None
    months = re.search(r"([A-Za-z]+\s*-\s*[A-Za-z]+|[A-Za-z]+)", value)
    daytime = re.search(r"(Morning|Evening|Afternoon|Night|Anytime)", value, re.IGNORECASE)
    return months.group(0) if months else None, daytime.group(0) if daytime else None

df["best_months"], df["best_daytime"] = zip(*df["best_time"].apply(extract_best_time))
df.drop(columns=["best_time"], inplace=True)

# Convert 'airport_50km' to Boolean
df["airport_50km"] = df["airport_50km"].astype(str).str.lower().map(
    {"true": True, "yes": True, "1": True, "false": False, "no": False, "0": False}
).fillna(False)

# Replace NaN with None
df.replace({np.nan: None}, inplace=True)

# Connect to MySQL
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Drop & Create Table (Aligned Columns for Better Display in MySQL)
cursor.execute("DROP TABLE IF EXISTS Attractions")
cursor.execute("""
CREATE TABLE Attractions (
    id            INT PRIMARY KEY,
    zone         ENUM('Northern', 'Southern', 'Eastern', 'Western', 'Central', 'North Eastern') NOT NULL,
    state        VARCHAR(100) NOT NULL,
    city         VARCHAR(100) NOT NULL,
    name         VARCHAR(255) UNIQUE NOT NULL,
    type         VARCHAR(100) NOT NULL,
    year         INT NULL,
    time_hr      DECIMAL(3,1) CHECK (time_hr > 0),
    rating       DECIMAL(2,1) CHECK (rating BETWEEN 0 AND 5),
    fee          INT CHECK (fee >= 0),
    airport_50km BOOLEAN,
    weekly_off   VARCHAR(50),
    significance TEXT,
    best_months  VARCHAR(100),
    best_daytime VARCHAR(50)
);
""")
print("✅ Table 'Attractions' created successfully")

# Insert Data
insert_query = """
INSERT INTO Attractions (id, zone, state, city, name, type, year, time_hr, rating, fee, airport_50km, weekly_off, significance, best_months, best_daytime) 
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE 
    zone=VALUES(zone), state=VALUES(state), city=VALUES(city), 
    type=VALUES(type), year=VALUES(year), time_hr=VALUES(time_hr), 
    rating=VALUES(rating), fee=VALUES(fee), 
    airport_50km=VALUES(airport_50km), weekly_off=VALUES(weekly_off), 
    significance=VALUES(significance), best_months=VALUES(best_months), 
    best_daytime=VALUES(best_daytime);
"""

for _, row in df.iterrows():
    cursor.execute(insert_query, (
        row["id"], row["zone"], row["state"], row["city"], row["name"],
        row["type"], row["year"], row["time_hr"], row["rating"],
        row["fee"], row["airport_50km"], row["weekly_off"],
        row["significance"], row["best_months"], row["best_daytime"]
    ))

conn.commit()
print(f"✅ {cursor.rowcount} rows inserted/updated successfully.")

# Close Connection
cursor.close()
conn.close()
