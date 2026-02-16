from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for authentication and authorization"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, index=True)  # admin, teacher, cr, student
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'), nullable=True)
    year_id = db.Column(db.Integer, db.ForeignKey('years.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    branch = db.relationship('Branch', back_populates='users')
    year = db.relationship('Year', back_populates='users')
    
    def set_password(self, password):
        """Set hashed password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        return self.role == 'admin'
    
    def is_teacher(self):
        return self.role == 'teacher'
    
    def is_cr(self):
        return self.role == 'cr'
    
    def is_student(self):
        return self.role == 'student'
    
    def can_edit_class(self, class_obj):
        """Check if user can edit a specific class"""
        if self.is_admin():
            return True
        elif self.is_teacher():
            return class_obj.instructor_id == self.instructor_id if hasattr(self, 'instructor_id') else False
        elif self.is_cr():
            return class_obj.branch_id == self.branch_id and class_obj.year_id == self.year_id
        return False
    
    def __repr__(self):
        return f'<User {self.username} ({self.role})>'


class Branch(db.Model):
    """Branch/Department model"""
    __tablename__ = 'branches'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    users = db.relationship('User', back_populates='branch')
    instructors = db.relationship('Instructor', back_populates='branch')
    classes = db.relationship('Class', back_populates='branch')
    
    def __repr__(self):
        return f'<Branch {self.name} ({self.code})>'


class Year(db.Model):
    """Academic Year model"""
    __tablename__ = 'years'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)  # 1st Year, 2nd Year, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    users = db.relationship('User', back_populates='year')
    modules = db.relationship('Module', back_populates='year')
    
    def __repr__(self):
        return f'<Year {self.name}>'


class Module(db.Model):
    """Module/Semester model"""
    __tablename__ = 'modules'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Semester 1, Semester 2, etc.
    year_id = db.Column(db.Integer, db.ForeignKey('years.id'), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    year = db.relationship('Year', back_populates='modules')
    classes = db.relationship('Class', back_populates='module')
    
    def __repr__(self):
        return f'<Module {self.name}>'


class Instructor(db.Model):
    """Instructor/Teacher model"""
    __tablename__ = 'instructors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, index=True)
    phone = db.Column(db.String(20))
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    branch = db.relationship('Branch', back_populates='instructors')
    classes = db.relationship('Class', back_populates='instructor')
    
    def __repr__(self):
        return f'<Instructor {self.name}>'


class Room(db.Model):
    """Room/Classroom model"""
    __tablename__ = 'rooms'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, index=True)  # Room number/name
    building = db.Column(db.String(100))
    capacity = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    classes = db.relationship('Class', back_populates='room')
    
    def __repr__(self):
        return f'<Room {self.name} ({self.building})>'


class Class(db.Model):
    """Class/Routine model"""
    __tablename__ = 'classes'
    
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    day = db.Column(db.String(20), nullable=False, index=True)  # Monday, Tuesday, etc.
    
    # Foreign Keys
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=True)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.id'), nullable=True)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=True)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'), nullable=False, index=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    room = db.relationship('Room', back_populates='classes')
    instructor = db.relationship('Instructor', back_populates='classes')
    module = db.relationship('Module', back_populates='classes')
    branch = db.relationship('Branch', back_populates='classes')
    
    def __repr__(self):
        return f'<Class {self.subject} ({self.day} {self.start_time}-{self.end_time})>'


def init_db(app):
    """Initialize database with default values"""
    with app.app_context():
        db.create_all()
        
        # Check if data already exists
        if Branch.query.first() is None:
            # Add default branches
            branches = [
                Branch(name='Computer Science', code='CS'),
                Branch(name='Electronics & Communication', code='EC'),
                Branch(name='Civil Engineering', code='CE'),
                Branch(name='Mechanical Engineering', code='ME'),
                Branch(name='Electrical Engineering', code='EE'),
            ]
            db.session.add_all(branches)
            
            # Add default years
            years = [
                Year(name='1st Year'),
                Year(name='2nd Year'),
                Year(name='3rd Year'),
                Year(name='4th Year'),
            ]
            db.session.add_all(years)
            
            # Add default rooms
            rooms = [
                Room(name='101', building='Building A', capacity=60),
                Room(name='102', building='Building A', capacity=60),
                Room(name='103', building='Building A', capacity=40),
                Room(name='201', building='Building B', capacity=60),
                Room(name='202', building='Building B', capacity=60),
                Room(name='228', building='Building B', capacity=50),
                Room(name='Lab 1', building='Building C', capacity=30),
                Room(name='Lab 2', building='Building C', capacity=30),
            ]
            db.session.add_all(rooms)
            
            # Add default admin user (password: admin123)
            admin = User(
                username='admin',
                role='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            
            # Add some sample instructors
            instructors = [
                Instructor(name='Dr. GCR', email='gcr@cit.ac.in', branch_id=1),
                Instructor(name='Dr. PSB', email='psb@cit.ac.in', branch_id=1),
                Instructor(name='Dr. RKS', email='rks@cit.ac.in', branch_id=2),
                Instructor(name='Dr. SKM', email='skm@cit.ac.in', branch_id=3),
            ]
            db.session.add_all(instructors)
            
            # Add default modules
            modules = [
                Module(name='Semester 1', year_id=1),
                Module(name='Semester 2', year_id=1),
                Module(name='Semester 3', year_id=2),
                Module(name='Semester 4', year_id=2),
                Module(name='Semester 5', year_id=3),
                Module(name='Semester 6', year_id=3),
                Module(name='Semester 7', year_id=4),
                Module(name='Semester 8', year_id=4),
            ]
            db.session.add_all(modules)
            
            # Add sample classes
            from datetime import time
            classes = [
                Class(subject='ECONOMICS', start_time=time(10, 0), end_time=time(11, 0), 
                      day='Monday', room_id=6, instructor_id=1, module_id=1, branch_id=1),
                Class(subject='SOFTWARE ENGINEERING', start_time=time(11, 0), end_time=time(12, 0), 
                      day='Monday', room_id=6, instructor_id=2, module_id=1, branch_id=1),
                Class(subject='DATA STRUCTURES', start_time=time(10, 0), end_time=time(11, 0), 
                      day='Tuesday', room_id=7, instructor_id=2, module_id=1, branch_id=1),
            ]
            db.session.add_all(classes)
            
            db.session.commit()
            print("Database initialized with default data!")
        else:
            print("Database already initialized!")
