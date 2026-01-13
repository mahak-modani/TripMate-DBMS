from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session
import mysql.connector
from flask_cors import CORS

# Blueprint for Admin API
admin_bp = Blueprint('admin_bp', __name__)
CORS(admin_bp)

# Database Configuration
db_config = {
    'host': "localhost",
    'user': "root",
    'password': "mahak",
    'database': "TravelPlanner"
}

# Function to get a database connection
def get_db_connection():
    return mysql.connector.connect(**db_config)



# ========================== ADMIN AUTH ==========================

@admin_bp.route('/logout', methods=['GET'])
def logout():
    return render_template('logout.html')


# 📌 **Admin Login API**
@admin_bp.route('/AdminLogin', methods=['POST'])
def admin_login():
    try:
        data = request.json
        email = data.get("email")
        password = data.get("password")

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM admin WHERE email = %s AND password = %s", (email, password))
        admin = cursor.fetchone()
        cursor.close()
        conn.close()

        if admin:
            session["admin_id"] = admin["Admin_ID"]
            return jsonify({"message": "Login successful!", "redirect": "/admin/dashboard"}), 200
        else:
            return jsonify({"message": "Invalid email or password"}), 401

    except Exception as e:
        return jsonify({"message": f"Error during login: {str(e)}"}), 500

# 📌 **Admin Logout API**
@admin_bp.route('/logout', methods=['GET'])
def admin_logout():
    session.pop("admin_id", None)
    return redirect(url_for("admin_login_page"))

# ========================== DASHBOARD ==========================

# 📌 Fetch Dashboard Stats
@admin_bp.route('/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        stats_query = {
            "totalUsers": "SELECT COUNT(*) AS count FROM users",
            "totalDestinations": "SELECT COUNT(*) AS count FROM destinations",
            "totalAttractions": "SELECT COUNT(*) AS count FROM attractions",
            "totalTrips": "SELECT COUNT(*) AS count FROM user_history",
            "totalBudgets": "SELECT SUM(budget) AS total FROM user_history"
        }

        stats = {}
        for key, query in stats_query.items():
            cursor.execute(query)
            result = cursor.fetchone()
            stats[key] = result["count"] if "count" in result else result["total"]

        cursor.close()
        conn.close()
        return jsonify(stats)

    except Exception as e:
        return jsonify({"message": f"Error fetching dashboard stats: {str(e)}"}), 500

# ========================== USER MANAGEMENT ==========================

# 📌 Fetch Users with Filters
@admin_bp.route('/users', methods=['GET'])
def get_users():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Retrieve filter parameters
        name = request.args.get('name', '')
        age = request.args.get('age', '')
        gender = request.args.get('gender', '')
        interests = request.args.get('interests', '')
        join_date = request.args.get('join_date', '')

        query = """
            SELECT User_ID, Name, Nationality, Email, Phone_Number, Age, Gender, Interests, Join_Date
            FROM Users
            WHERE 1=1
        """
        params = []

        if name:
            query += " AND Name LIKE %s"
            params.append(f"%{name}%")
        if age:
            query += " AND Age = %s"
            params.append(age)
        if gender:
            query += " AND Gender = %s"
            params.append(gender)
        if interests:
            query += " AND Interests LIKE %s"
            params.append(f"%{interests}%")
        if join_date:
            query += " AND DATE(Join_Date) = %s"
            params.append(join_date)

        cursor.execute(query, tuple(params))
        users = cursor.fetchall()
        cursor.close()
        conn.close()

        if users:
            return jsonify(users)
        else:
            return jsonify({"message": "No users found matching the criteria."}), 404
    except Exception as e:
        return jsonify({"message": f"Error fetching users: {str(e)}"}), 500

# 📌 Add a New User
@admin_bp.route('/add_user', methods=['POST'])
def add_user():
    try:
        data = request.json
        if not all([data.get("name"), data.get("nationality"), data.get("email"),
                    data.get("password"), data.get("age"), data.get("gender")]):
            return jsonify({"message": "Missing required fields"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """INSERT INTO users (Name, Nationality, Email, Password, Phone_Number, Age, Gender, Interests, Join_Date) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())"""
        values = (data["name"], data["nationality"], data["email"], data["password"],
                  data["phone"], data["age"], data["gender"], data["interests"])

        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "User added successfully"}), 201
    except Exception as e:
        return jsonify({"message": f"Error adding user: {str(e)}"}), 500

# 📌 Delete a User
@admin_bp.route('/delete_user', methods=['DELETE'])
def delete_user():
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({"message": "User ID is required"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "DELETE FROM users WHERE User_ID = %s"
        cursor.execute(sql, (user_id,))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "User not found"}), 404

        cursor.close()
        conn.close()
        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        return jsonify({"message": f"Error deleting user: {str(e)}"}), 500


# Fetch all attractions, optionally filtered by city
@admin_bp.route('/attractions', methods=['GET'])
def get_attractions():
    city = request.args.get('city', 'none')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM attractions WHERE 1=1"
    filters = []

    if city != "none":
        query += " AND city = %s"
        filters.append(city)

    cursor.execute(query, tuple(filters))
    attractions = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(attractions)

# Fetch available city filters
@admin_bp.route('/attractions/filters', methods=['GET'])
def get_filter_options():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT DISTINCT city FROM attractions")
    cities = [row["city"] for row in cursor.fetchall()]
    cities.insert(0, "none")

    cursor.close()
    conn.close()

    return jsonify({"cities": cities})

# Add new attraction
@admin_bp.route('/attractions/add', methods=['POST'])
def add_attraction():
    data = request.json

    required_fields = [
        'id', 'zone', 'state', 'city', 'name', 'type',
        'year', 'time_hr', 'rating', 'fee', 'airport_50km',
        'weekly_off', 'significance', 'best_daytime', 'area'
    ]

    # Check for missing fields
    if not all(field in data for field in required_fields):
        return jsonify({"message": "Missing fields in request body"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO attractions (id, zone, state, city, name, type, year, time_hr, rating, fee, airport_50km, weekly_off, significance, best_daytime, area)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    cursor.execute(query, (
        data['id'], data['zone'], data['state'], data['city'], data['name'],
        data['type'], data['year'], data['time_hr'], data['rating'], data['fee'],
        data['airport_50km'], data['weekly_off'], data['significance'], data['best_daytime'],
        data['area']
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Attraction added successfully"})

# Delete attraction by ID
@admin_bp.route('/attractions/delete/<int:attraction_id>', methods=['DELETE'])
def delete_attraction(attraction_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "DELETE FROM attractions WHERE id = %s"
    cursor.execute(query, (attraction_id,))
    conn.commit()

    if cursor.rowcount == 0:
        return jsonify({"message": "Attraction not found"}), 404

    cursor.close()
    conn.close()

    return jsonify({"message": "Attraction deleted successfully"})

@admin_bp.route('/destinations', methods=['GET'])
def get_destinations():
    name = request.args.get('name')
    city = request.args.get('city')
    country = request.args.get('country')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM destinations WHERE 1=1"
    filters = []

    if name:
        query += " AND destination_id LIKE %s"
        filters.append(f"%{name}%")
    if city:
        query += " AND city = %s"
        filters.append(city)
    if country:
        query += " AND country = %s"
        filters.append(country)

    cursor.execute(query, tuple(filters))
    destinations = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(destinations)

# Get unique cities and countries for filter dropdowns
@admin_bp.route('/destinations/filters', methods=['GET'])
def get_destination_filters():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT DISTINCT city FROM destinations")
    cities = [row["city"] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT country FROM destinations")
    countries = [row["country"] for row in cursor.fetchall()]

    cursor.close()
    conn.close()

    return jsonify({"cities": cities, "countries": countries})

# Add a new destination
@admin_bp.route('/destinations/add', methods=['POST'])
def add_destination():
    data = request.json

    required_fields = ['destination_id', 'city', 'country', 'avg_cost']
    if not all(field in data for field in required_fields):
        return jsonify({"message": "Missing fields"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO destinations (destination_id, city, country, avg_cost)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (
        data['destination_id'],
        data['city'],
        data['country'],
        data['avg_cost']
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Destination added successfully"})

# Delete a destination by ID
@admin_bp.route('/destinations/delete/<string:destination_id>', methods=['DELETE'])
def delete_destination(destination_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "DELETE FROM destinations WHERE destination_id = %s"
    cursor.execute(query, (destination_id,))
    conn.commit()

    if cursor.rowcount == 0:
        return jsonify({"message": "Destination not found"}), 404

    cursor.close()
    conn.close()

    return jsonify({"message": "Destination deleted successfully"})

