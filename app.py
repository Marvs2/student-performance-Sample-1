
from flask import Flask, render_template, jsonify, redirect, url_for, session
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


#=========================================================================
# TESTING AREA



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

@app.route('/logout')
def logout():
    # Clear session data including JWT token and user role
    session.clear()
    return redirect(url_for('student_login'))  # Redirect to home or appropriate route

# ========================================================================
# ALL STUDENT ROUTES HERE
@app.route('/student')
@prevent_authenticated
def student_login():
    session.permanent = True
    return render_template('student/login.html')

@app.route('/student/home')
@student_required
def student_home():
    session.permanent = True
    return render_template('student/home.html')

# ========================================================================
# ALL FACULTY ROUTES HERE
@app.route('/faculty')
@prevent_authenticated
def faculty_login():
    return render_template('faculty/login.html')

@app.route('/faculty/home')
@prevent_authenticated
@faculty_required
def faculty_home():
    session.permanent = True
    return render_template('faculty/home.html')


# ========================================================================
# ALL ADMIN ROUTES HERE
@app.route('/admin')
@prevent_authenticated
def admin_login():
    return render_template('admin/login.html')

@app.route('/admin/home')
@admin_required
def admin_home():
    session.permanent = True
    return render_template('admin/home.html')

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

# ... other route registrations ...
# ========================================================================

if __name__ == '__main__':
    app.run(debug=True)



# ... other route registrations ...
# ========================================================================