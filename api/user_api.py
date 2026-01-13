from flask import Blueprint, request, jsonify, session, redirect, render_template, url_for
import mysql.connector
import random
from datetime import datetime
from flask_cors import CORS
from datetime import timedelta
import json
import os

# Create Blueprint for User API
user_bp = Blueprint('user_bp', __name__)
CORS(user_bp)

# Database Configuration
db_config = {
    'host': "localhost",
    'user': "root",
    'password': "mahak",
    'database': "TravelPlanner"
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# Function to generate a unique user ID (YYMMxx format)
def generate_user_id():
    current_date = datetime.datetime.now()
    year = str(current_date.year)[2:]  # Last two digits of the year (YY)
    month = f"{current_date.month:02d}"  # MM (01-12)

    while True:
        random_num = f"{random.randint(10, 99)}"  # Random 2-digit number
        user_id = f"{year}{month}{random_num}"

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users WHERE user_id = %s", (user_id,))
        if cursor.fetchone()[0] == 0:
            cursor.close()
            conn.close()
            return user_id  # Unique ID found
        cursor.close()
        conn.close()

# ------------------- User Authentication Routes -------------------

# 📌 User Signup API
@user_bp.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid request format"}), 400

        email = data.get("email")
        password = data.get("password")
        name = data.get("name")
        nationality = data.get("nationality")
        phone = data.get("phone")
        age = data.get("age")
        gender = data.get("gender")
        interests = data.get("interests")

        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if email already exists
        cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            return jsonify({"error": "Email already registered"}), 400

        # Generate a unique user ID
        user_id = generate_user_id()

        # Insert user into database
        sql = """INSERT INTO users (user_id, Name, Nationality, Email, Password, Phone_Number, Age, Gender, Interests, Join_Date) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())"""
        values = (user_id, name, nationality, email, password, phone, age, gender, interests)
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Sign-Up successful", "redirect": "/login"}), 201

    except Exception as e:
        return jsonify({"error": f"Error signing up: {str(e)}"}), 500


# 📌 User Login API
@user_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid request format"}), 400

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT user_id, Name, Password FROM users WHERE Email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and user["Password"] == password:
            session["user_id"] = user["user_id"]  # ✅ Store user_id in session
            return jsonify({
                "message": "Login successful",
                "user_id": user["user_id"],
                "name": user["Name"],
                "redirect": "/dashboard"
            }), 200
        else:
            return jsonify({"error": "Invalid email or password"}), 401

    except Exception as e:
        return jsonify({"error": f"Error during login: {str(e)}"}), 500



# 📌 Logout API
@user_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login_page'))


# ------------------- User Profile Management -------------------

# ✅ API to Fetch User Profile
@user_bp.route('/profile_settings', methods=['GET', 'POST'])
def profile_settings():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized", "redirect": url_for('user_bp.login')}), 401

    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'GET':
        cursor.execute("""
            SELECT Name, Email, Phone_Number, Age, Gender, Nationality, Interests
            FROM users WHERE user_id = %s
        """, (user_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            return jsonify(user)
        else:
            return jsonify({"error": "User not found"}), 404

    elif request.method == 'POST':
        data = request.json  # Accepting JSON sent from JS
        cursor.execute("""
            UPDATE users 
            SET Name = %s, Email = %s, Phone_Number = %s, Age = %s, 
                Gender = %s, Nationality = %s, Interests = %s 
            WHERE user_id = %s
        """, (
            data['name'], data['email'], data['phone_number'], data['age'],
            data['gender'], data['nationality'], data['interests'], user_id
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"success": True, "message": "Profile updated successfully"})


# ------------------- Trip Management Routes -------------------

# 📌 My Trips Page
@user_bp.route('/my_trips', methods=['GET'])
def my_trips():
    user_id = session.get('user_id')  # Ensure user is logged in
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
    SELECT uh.trip_id, d.city, d.country, uh.start_date, uh.end_date, 
           uh.accommodation_type, uh.accommodation_cost, 
           uh.transportation_type, uh.transportation_cost, uh.budget
    FROM user_history uh
    JOIN destinations d ON uh.destination_id = d.destination_id
    WHERE uh.user_id = %s;
    ''', (user_id,))
    
    trips = [
        {
            "trip_id": row[0],
            "city": row[1],  
            "country": row[2],  
            "start_date": row[3].strftime("%Y-%m-%d"),
            "end_date": row[4].strftime("%Y-%m-%d"),
            "accommodation_type": row[5],
            "accommodation_cost": float(row[6]) if row[6] else 0.0,
            "transportation_type": row[7],
            "transportation_cost": float(row[8]) if row[8] else 0.0,
            "budget": float(row[9]) if row[9] else 0.0
        }
        for row in cursor.fetchall()
    ]

    return jsonify(trips)




# 📌 Trip Planner Page

@user_bp.route('/generate_itinerary', methods=['POST'])
def generate_itinerary():
    data = request.json
    user_id = session.get('user_id')
    city = data.get('city')
    area = data.get('area')  # Stay area
    start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d')
    end_date = datetime.strptime(data.get('end_date'), '%Y-%m-%d')

    trip_prefix = start_date.strftime('%y%m')
    random_suffix = str(random.randint(100, 999))
    trip_id = trip_prefix + random_suffix

    budget = float(data.get('budget'))
    transport_mode = data.get('transport_mode')  # metro, cab, auto

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM attractions 
        WHERE city = %s 
        ORDER BY FIELD(best_daytime, 'Morning', 'Afternoon', 'Evening')
    """, (city,))
    attractions = cursor.fetchall()

    time_buckets = {'Morning': [], 'Afternoon': [], 'Evening': []}
    for attr in attractions:
        slot = attr['best_daytime'].capitalize()
        if slot in time_buckets:
            time_buckets[slot].append(attr)

    itinerary = []
    budget_used = 0
    days = (end_date - start_date).days + 1

    for day in range(days):
        curr_date = start_date + timedelta(days=day)
        prev_area = area  # Start from stay area

        for slot in ['Morning', 'Afternoon', 'Evening']:
            if time_buckets[slot]:
                attraction = time_buckets[slot].pop(0)
                attraction_area = attraction['area']
                fee = float(attraction['fee'])
                travel_time = round(float(attraction['time_hr']) * 60)

                # Query transport with case-insensitive match
                cursor.execute("""
                    SELECT fare FROM transport
                    WHERE LOWER(TRIM(from_area)) = LOWER(TRIM(%s))
                    AND LOWER(TRIM(to_area)) = LOWER(TRIM(%s))
                    AND LOWER(TRIM(transport_mode)) = LOWER(TRIM(%s))
                """, (
                    prev_area.strip(),
                    attraction_area.strip(),
                    transport_mode.strip()
                ))
                result = cursor.fetchone()

                if result:
                    transport_cost = float(result.get('fare', 0.0))
                else:
                    print(f"[Warning] No transport data from {prev_area} to {attraction_area} for {transport_mode}. Setting cost to 0.")
                    transport_cost = 0.0

                total_cost = fee + transport_cost

                if budget_used + total_cost > budget:
                    print(f"[Info] Skipping attraction '{attraction['name']}' to stay within budget.")
                    continue

                budget_used += total_cost

                itinerary.append({
                    'attraction_id': attraction['id'],
                    'name': attraction['name'],
                    'significance': attraction['significance'],
                    'fee': fee,
                    'visit_date': curr_date.strftime('%Y-%m-%d'),
                    'visit_time': slot,
                    'travel_time': travel_time,
                    'transport_mode': transport_mode.capitalize(),
                    'transport_cost': transport_cost
                })

                cursor.execute("""
                    INSERT INTO itinerary 
                    (User_ID, trip_id, attraction_id, visit_date, visit_time, travel_time, transport_mode)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    user_id, trip_id, attraction['id'],
                    curr_date.strftime('%Y-%m-%d'),
                    slot, travel_time, transport_mode.capitalize()
                ))

                prev_area = attraction_area  # For next hop

    conn.commit()
    cursor.close()

    remaining_budget = round(budget - budget_used, 2)
    print("Final Itinerary:", itinerary)

    return jsonify({
        'itinerary': itinerary,
        'budget_used': round(budget_used, 2),
        'remaining_budget': remaining_budget
    })
