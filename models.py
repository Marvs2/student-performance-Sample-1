from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from werkzeug.security import generate_password_hash
from flask_login import UserMixin

db = SQLAlchemy()


class Student(db.Model, UserMixin):
    __tablename__ = 'students'

    studentID = db.Column(db.Integer, primary_key=True) # UserID
    studentNumber = db.Column(db.String(30), unique=True, nullable=False) #StudNumber
    studentName = db.Column(db.String(50), nullable=False)  # Name
    date_of_Birth = db.Column(db.Date)  # DateOfBirth
    place_of_Birth = db.Column(db.String(50), nullable=True)  # PlaceOfBirth
    mobileNumber = db.Column(db.String(11))  # MobileNumber
    email = db.Column(db.String(50), unique=True, nullable=False)  # Email
    address = db.Column(db.String(50), nullable=True) # Address
    password = db.Column(db.String(128), nullable=False)  # Password
    gender = db.Column(db.Integer)  # Gender
    userImg = db.Column(db.String, nullable=False) #img
    cpassword = db.Column(db.String(128), nullable=True)
 #   dropout = db.Column(db.Boolean)  # Dropout
  #  is_graduated = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'id': self.studentID,
            'studentNumber': self.studentNumber,
            'name': self.studentName,
            'dateofBirth': self.date_of_Birth,
            'placeofBirth': self.place_of_Birth,
            'mobileNumber': self.mobileNumber,
            'email': self.email,
            'password': self.password,
            'gender': self.gender,
            'userImg': self.userImg,
            'cpassword': self.cpassword,
        #    'dropout': self.dropout,
        #    'is_graduated': self.is_graduated
        }
        
    def get_id(self):
        return str(self.id)  # Convert to string to ensure compatibility

class Payment(db.Model, UserMixin):
    __tablename__ = 'payments'
    paymentID = db.Column(db.Integer, primary_key=True)
    studentID = db.Column(db.Integer, db.ForeignKey('students.studentID'))
    modeofPayment = db.Column(db.String(50))
    totalPayment = db.Column(db.DECIMAL)  # You can specify precision and scale if needed
    dateofPayment = db.Column(db.Date)
    proofofPayment = db.Column(db.String(255))  # Modify the length as needed
    student = db.relationship('Student', backref='payments')

class Service(db.Model, UserMixin):
    __tablename__ = 'services'
    serviceID = db.Column(db.Integer, primary_key=True)
    studentID = db.Column(db.Integer, db.ForeignKey('students.studentID'))
    typeofServices = db.Column(db.String(50))
    status = db.Column(db.String(50))  # Modify the length as needed
    dateofServices = db.Column(db.Date)
    student = db.relationship('Student', backref='services')

class Feedback(db.Model, UserMixin):
    __tablename__ = 'feedbacks'
    feedbackID = db.Column(db.Integer, primary_key=True)
    studentID = db.Column(db.Integer, db.ForeignKey('students.studentID'))
    studentName = db.Column(db.String(50))
    emailAddress = db.Column(db.String(50))
    ratings = db.Column(db.Integer)  # Assuming ratings are integers
    feedBacks = db.Column(db.TEXT)  # Modify the data type as needed
    student = db.relationship('Student', backref='feedbacks')

class Complaint(db.Model, UserMixin):
    __tablename__ = 'complaints'
    complaintID = db.Column(db.Integer, primary_key=True)
    studentID = db.Column(db.Integer, db.ForeignKey('students.studentID'))
    studentName = db.Column(db.String(50))
    emailAddress = db.Column(db.String(50))
    complaintDetails = db.Column(db.TEXT)
    complaintFile = db.Column(db.String(255))  # Modify the length as needed
    dateofComplaint = db.Column(db.Date)
    student = db.relationship('Student', backref='complaints')


class Announcement(db.Model, UserMixin):
    __tablename__ = 'announcements'
    announcementID = db.Column(db.Integer, primary_key=True)
    studentID = db.Column(db.Integer, db.ForeignKey('students.studentID'))
    facultyID = db.Column(db.Integer, db.ForeignKey('faculties.facultyID'))
    announcementType = db.Column(db.String(50))  # e.g., 'General', 'Event', etc.
    announcementDetails = db.Column(db.TEXT)
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    faculty = db.relationship('Faculty', backref='announcements')



class Faculty(db.Model, UserMixin):
    __tablename__ = 'faculties'

    facultyID = db.Column(db.Integer, primary_key=True)  # UserID
    faculty_Number = db.Column(db.String(30), unique=True, nullable=False) #FacultyNumber
    userType = db.Column(db.String(50))  # e.g., 'Admin', 'Professor', etc.
    name = db.Column(db.String(50), nullable=False)  # Name
    email = db.Column(db.String(50), unique=True, nullable=False)  # Email
    address = db.Column(db.String(255))  # You can use String or TEXT depending on the length
    password = db.Column(db.String(128), nullable=False)  # Password
    gender = db.Column(db.Integer)  # Gender
    date_of_birth = db.Column(db.Date)  # DateOfBirth
    place_of_birth = db.Column(db.String(50))  # PlaceOfBirth
    mobile_number = db.Column(db.String(20))  # MobileNumber
    userImg = db.Column(db.String(255))  # Modify the length as needed
    is_active = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'id': self.facultyID,
            'faculty_Number': self.faculty_Number,
            'userType': self.userType,
            'name': self.name,
            'email': self.email,
            'address': self.address,
            'password': self.password,
            'gender': self.gender,
            'dateofBirth': self.date_of_birth,
            'placeofBirth': self.place_of_birth,
            'mobile_number': self.mobile_number,
            'userImg': self.userImg,
            'is_active': self.is_active
        }
    def get_id(self):
        return str(self.id)  # Convert to string to ensure compatibility
    

class Admin(db.Model, UserMixin):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)  # UserID
    admin_Number = db.Column(db.String(30), unique=True, nullable=False) #AdminNumber
    name = db.Column(db.String(50), nullable=False)  # Name
    email = db.Column(db.String(50), unique=True, nullable=False)  # Email
    password = db.Column(db.String(128), nullable=False)  # Password
    gender = db.Column(db.Integer)  # Gender
    date_of_birth = db.Column(db.Date)  # DateOfBirth
    place_of_birth = db.Column(db.String(50))  # PlaceOfBirth
    mobile_number = db.Column(db.String(11))  # MobileNumber
    is_active = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'id': self.id,
            'admin_Number': self.admin_Number,
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'gender': self.gender,
            'dateofBirth': self.date_of_birth,
            'placeofBirth': self.place_of_birth,
            'mobile_number': self.mobile_number,
            'is_active': self.is_active
        }
    def get_id(self):
        return str(self.id)  # Convert to string to ensure compatibility

def init_db(app):
    db.init_app(app)
    with app.app_context():
        inspector = inspect(db.engine)
        if not inspector.has_table('students'):
            db.create_all()
            create_sample_data()
        
#=====================================================================================================
# INSERTING DATA
def create_sample_data():
    # Create and insert student data
    student_data = [
        {   
            'id':'1',
            'studentNumber': '2020-00001-CM-0',
            'studentName': 'Student 1',
            'email': 'student1@example.com',
            'password': generate_password_hash('password1'),
            'gender': 1,
            'dateofBirth': '2003-01-15',
            'placeofBirth': 'City 1',
            'mobileNumber': '09123123123',
            'userImg': 'default.jpg'
        },
        {
            'id':'2',
            'student_Number': '2020-00002-CM-0',
            'name': 'Student 2',
            'email': 'student2@example.com',
            'password': generate_password_hash('password2'),
            'gender': 2,
            'dateofBirth': '2002-05-20',
            'placeofBirth': 'City 2',
            'mobileNumber': '09123123124',
            'userImg': 'pup2.jpg'
           # 'dropout': True,
            #'is_graduated': False
            # Add more attributes here
        },
        # Add more student data as needed
    ]
    
    for data in student_data:
        student = Student(**data)
        db.session.add(student)

    # Create and insert faculty data
    faculty_data = [
        {
            'id': '1',
            'faculty_Number': '2020-00001-TC-0',
            'userType': 'Professor',
            'name': 'Faculty 1',
            'email': 'faculty1@example.com',
            'password': generate_password_hash('password1'),
            'gender': 1,
            'dateofBirth': '1988-07-20',
            'placeofBirth': 'City 2',
            'mobile_number': '09123123111',
            'userImg': 'default.jpg',
            'is_active': True
            # Add more attributes here
        },
        {
            'id': '2',
            'faculty_Number': '2020-00002-TC-0',
            'userType': 'Professor',
            'name': 'Faculty 2',
            'email': 'faculty2@example.com',
            'password': generate_password_hash('password2'),
            'gender': 2,
            'dateofBirth': '1975-12-05',
            'placeofBirth': 'City 3',
            'mobile_number': '09123123125',
            'userImg': 'default.jpg',
            'is_active': False
            # Add more attributes here
        },
        # Add more faculty data as needed
    ]
    
    for data in faculty_data:
        faculty = Faculty(**data)
        db.session.add(faculty)
        
    # Create and insert admin data
    admin_data = [
        {
            'id': '1',
            'admin_Number': '2020-00001-AD-0',
            'name': 'Admin 1',
            'email': 'admin1@example.com',
            'password': generate_password_hash('password1'),
            'gender': 2,
            'dateofBirth': '1995-03-10',
            'placeofBirth': 'City 3',
            'mobile_number': '09123123222',
            'is_active': True
            # Add more attributes here
        },
        {
            'id': '2',
            'admin_Number': '2020-00002-AD-0',
            'name': 'Admin 2',
            'email': 'admin2@example.com',
            'password': generate_password_hash('password2'),
            'gender': 1,
            'dateofBirth': '1980-09-18',
            'placeofBirth': 'City 4',
            'mobile_number': '09123123223',
            'is_active': True
            # Add more attributes here
        },
        # Add more admin data as needed
    ]
    
    for data in admin_data:
        admin = Admin(**data)
        db.session.add(admin)

    db.session.commit()

