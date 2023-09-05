
from functools import wraps
from flask import Flask, render_template, jsonify, redirect, request, url_for, session
from flask_sqlalchemy import SQLAlchemy

from Api.v1.student.api_routes import student_api  
from Api.v1.faculty.api_routes import faculty_api
from Api.v1.admin.api_routes import admin_api

import os
from dotenv import load_dotenv


from models import init_db, Student, Faculty, Admin

from flask_jwt_extended import JWTManager
from flask_login import LoginManager, logout_user, current_user

from decorators.auth_decorators import student_required, faculty_required, prevent_authenticated, admin_required

load_dotenv()  # Load environment variables from .env file
app = Flask(__name__)
# SETUP YOUR POSTGRE DATABASE HERE
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour (in seconds)
app.secret_key = os.getenv('SECRET_KEY')  # Replace 'your-secret-key' with an actual secret key

jwt = JWTManager(app)
init_db(app)

@app.context_processor
def custom_context_processor():
    authenticated = False
    if 'user_role' in session:
        authenticated = True
    return {'authenticated': authenticated}

# Define the @prevent_authenticated decorator
def prevent_authenticated(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if 'user_role' in session:
            # User is already authenticated
            if session['user_role'] == 'student':
                return redirect(url_for('student_home'))
            elif session['user_role'] == 'faculty':
                return redirect(url_for('faculty_home'))
            elif session['user_role'] == 'admin':
                return redirect(url_for('admin_home'))
        return view(*args, **kwargs)
    return wrapped_view

# ...


#=========================================================================
# TESTING AREA

@app.after_request
def add_header(response):
    if request.path in ['/student', '/student/home', '/faculty', '/faculty/home']:
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    return response


#===========================================================================
@app.route('/')
@prevent_authenticated
def first():
    session.permanent = True
    return render_template('first/base.html')

@app.route('/first/home')
def index():
    session.permanent = True
    return render_template('first/home.html')

#===========================================================================
# ROUTING FOR YOUR APPLICATION (http:localhost:3000)
@app.route('/main')
@prevent_authenticated
def home():
    session.permanent = True
    return render_template('main/index.html')
# ...

# ========================================================================
# ALL STUDENT ROUTES HERE
@app.route('/student')
@prevent_authenticated  # Use the @prevent_authenticated decorator
def student_login():
    session.permanent = True
    return render_template('student/login.html')

@app.route('/student/home')
@student_required
def student_home():
    session.permanent = True
    return render_template('student/home.html')

@app.route('/student/logout')
@student_required  # Require authentication for the logout route
def logout_student():
    # Clear session data including JWT token and user role
    session.clear()
    return redirect(url_for('student_login'))
    # Redirect to home or appropriate route

# ...

# ========================================================================
# ALL FACULTY ROUTES HERE
@app.route('/faculty')
@prevent_authenticated  # Use the @prevent_authenticated decorator
def faculty_login():
    session.permanent = True
    return render_template('faculty/login.html')

@app.route('/faculty/home')
@faculty_required
def faculty_home():
    session.permanent = True
    return render_template('faculty/home.html')

@app.route('/faculty/logout')
@faculty_required  # Require authentication for the logout route
def logout_faculty():
    # Clear session data including JWT token and user role
    session.clear()
    return redirect(url_for('faculty_login'))
    # Redirect to home or appropriate route

# ...

# ========================================================================
# ALL ADMIN ROUTES HERE
@app.route('/admin')
@prevent_authenticated  # Use the @prevent_authenticated decorator
def admin_login():
    return render_template('admin/login.html')

@app.route('/admin/home')
@admin_required
def admin_home():
    session.permanent = True
    return render_template('admin/home.html')

@app.route('/admin/logout')
@admin_required  # Require authentication for the logout route
def logout_admin():
    # Clear session data including JWT token and user role
    session.clear()
    return redirect(url_for('admin_login'))
    # Redirect to home or appropriate route

# ========================================================================
# Register the API blueprint
app.register_blueprint(admin_api, url_prefix='/api/v1/admin')
app.register_blueprint(faculty_api, url_prefix='/api/v1/faculty')
app.register_blueprint(student_api, url_prefix='/api/v1/student')

# ========================================================================
# TESTING
@app.route('/student/json', methods=['GET'])
def get_student_json():
    students = Student.query.all()

    student_list = []
    for student in students:
        student_data = {
            'id': student.id,
            'name': student.name,
            'email': student.email,
            'password': student.password
            # Add other fields as needed
        }
        student_list.append(student_data)

    return jsonify(student_list)

# ========================================================================
# Username
@app.context_processor
def custom_context_processor():
    authenticated = False
    student_name = ""  # Initialize with an empty string
    if 'user_role' in session and 'student_name' in session:
        authenticated = True
        student_name = session['student.name']
    return {'authenticated': authenticated, 'student_name': student_name}

# ... other route registrations ...
# ========================================================================

if __name__ == '__main__':
    app.run(debug=True)



# ... other route registrations ...
# ========================================================================