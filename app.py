from flask import Flask, jsonify, redirect, render_template, session, url_for
from api.admin_api import admin_bp  # Import Admin API Blueprint
from api.user_api import user_bp    # Import User API Blueprint
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Secret key for session management
app.secret_key = 'your_secret_key_here'

# Register Blueprints
app.register_blueprint(admin_bp, url_prefix='/api/admin')  
app.register_blueprint(user_bp, url_prefix='/api/user')  

# ------------------- User API Routes -------------------

@app.route('/')
def home():
    return render_template('landing.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/signup')
def signup_page():
    return render_template('signup.html')

@app.route('/logout', methods=['GET'])
def logout():
    return render_template('logout.html')


@app.route('/AdminLogin')
def admin_login_page():
    return render_template('AdminLogin.html')

@app.route('/users')
def admin_users():
    if 'admin_id' not in session:
        return redirect(url_for('admin_login_page'))
    return render_template('users.html')

@app.route('/attractions')
def admin_attractions():
    if 'admin_id' not in session:
        return redirect(url_for('admin_login_page'))
    return render_template('Attractions.html')

@app.route('/destinations')
def admin_destinations():
    if 'admin_id' not in session:
        return redirect(url_for('admin_login_page'))
    return render_template('Destinations.html')



@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin_id' not in session:
        return redirect(url_for('admin_login_page'))
    return render_template('AdminDashboard.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('dashboard.html', welcome_message="Welcome!")


@app.route('/my_trips')
def my_trips():
    return render_template('MyTrips.html')

@app.route('/profile_settings')
def profile_settings():
    return render_template('Profile_Settings.html')

@app.route('/create_trip')
def trip_planner():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('TripPlanner.html')

@app.route('/budget_tracker')
def budget_tracking():
    return render_template('BudgetTracker.html')

# ------------------- Admin API Routes -------------------


@app.route('/api/admin/logout', methods=['GET'])
def admin_logout_api():
    return admin_bp.view_functions['admin_bp.admin_logout']()

@app.route('/dashboard/stats', methods=['GET'])
def admin_dashboard_stats():
    return admin_bp.view_functions['admin_bp.get_dashboard_stats']()

@app.route('/api/admin/users', methods=['GET'])
def admin_users_api():
    return admin_bp.view_functions['admin_bp.get_users']()

@app.route('/api/admin/users/add', methods=['POST'])
def admin_add_user_api():
    return admin_bp.view_functions['admin_bp.add_user']()

@app.route('/api/admin/users/delete', methods=['DELETE'])
def admin_delete_user_api():
    return admin_bp.view_functions['admin_bp.delete_user']()


# ------------------- System Check -------------------

@app.route('/flask-check')
def flask_check():
    return jsonify({"status": "running"})

if __name__ == '__main__':
    app.run(debug=True)
