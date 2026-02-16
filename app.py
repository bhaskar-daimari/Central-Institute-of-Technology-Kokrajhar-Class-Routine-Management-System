from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config import config
from models import db, User, Branch, Year, Module, Instructor, Room, Class, init_db
from datetime import time

app = Flask(__name__)
app.config.from_object(config['development'])

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Initialize database with default data
with app.app_context():
    db.create_all()
    init_db(app)

# ==================== AUTH ROUTES ====================

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    branches = Branch.query.all()
    years = Year.query.all()
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        branch_id = request.form.get('branch_id')
        year_id = request.form.get('year_id')
        
        # Check if username exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('register'))
        
        # Create new user
        user = User(
            username=username,
            role=role,
            branch_id=int(branch_id) if branch_id else None,
            year_id=int(year_id) if year_id else None
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', branches=branches, years=years)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# ==================== DASHBOARD ROUTES ====================

@app.route('/dashboard')
@login_required
def dashboard():
    # Get filter parameters
    branch_id = request.args.get('branch_id')
    year_id = request.args.get('year_id')
    day = request.args.get('day')
    
    # Base query
    query = Class.query
    
    # Apply role-based filtering
    if current_user.is_student() or current_user.is_cr():
        query = query.filter_by(branch_id=current_user.branch_id)
        if current_user.year_id:
            query = query.join(Module).filter(Module.year_id == current_user.year_id)
    
    # Apply additional filters
    if branch_id and current_user.is_admin():
        query = query.filter_by(branch_id=int(branch_id))
    if year_id and current_user.is_admin():
        query = query.join(Module).filter(Module.year_id == int(year_id))
    if day:
        query = query.filter_by(day=day)
    
    # Order by day and time
    classes = query.order_by(Class.day, Class.start_time).all()
    
    branches = Branch.query.all()
    years = Year.query.all()
    
    return render_template('dashboard.html', 
                         classes=classes, 
                         branches=branches, 
                         years=years,
                         current_branch_id=branch_id,
                         current_year_id=year_id,
                         current_day=day)

# ==================== API ROUTES ====================

@app.route('/api/classes', methods=['GET'])
@login_required
def get_classes():
    branch_id = request.args.get('branch_id')
    year_id = request.args.get('year_id')
    day = request.args.get('day')
    
    query = Class.query
    
    # Role-based filtering
    if current_user.is_student() or current_user.is_cr():
        query = query.filter_by(branch_id=current_user.branch_id)
        if current_user.year_id:
            query = query.join(Module).filter(Module.year_id == current_user.year_id)
    
    if branch_id:
        query = query.filter_by(branch_id=int(branch_id))
    if year_id:
        query = query.join(Module).filter(Module.year_id == int(year_id))
    if day:
        query = query.filter_by(day=day)
    
    classes = query.order_by(Class.day, Class.start_time).all()
    
    return jsonify([{
        'id': c.id,
        'subject': c.subject,
        'start_time': c.start_time.strftime('%H:%M'),
        'end_time': c.end_time.strftime('%H:%M'),
        'day': c.day,
        'room': c.room.name if c.room else None,
        'instructor': c.instructor.name if c.instructor else None,
        'module': c.module.name if c.module else None,
        'branch': c.branch.name if c.branch else None
    } for c in classes])

@app.route('/api/classes', methods=['POST'])
@login_required
def add_class():
    if current_user.is_student():
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    
    # Role-based validation
    branch_id = data.get('branch_id')
    if current_user.is_cr() and branch_id != current_user.branch_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Parse time strings to time objects
    start_time_str = data.get('start_time')
    end_time_str = data.get('end_time')
    
    try:
        start_time = time.fromisoformat(start_time_str) if ':' in start_time_str else time(int(start_time_str.split(':')[0]), int(start_time_str.split(':')[1]))
        end_time = time.fromisoformat(end_time_str) if ':' in end_time_str else time(int(end_time_str.split(':')[0]), int(end_time_str.split(':')[1]))
    except:
        return jsonify({'error': 'Invalid time format'}), 400
    
    new_class = Class(
        subject=data.get('subject'),
        start_time=start_time,
        end_time=end_time,
        day=data.get('day'),
        room_id=data.get('room_id'),
        instructor_id=data.get('instructor_id'),
        module_id=data.get('module_id'),
        branch_id=branch_id
    )
    
    db.session.add(new_class)
    db.session.commit()
    
    return jsonify({'message': 'Class added successfully!'}), 201

@app.route('/api/classes/<int:cls_id>', methods=['PUT'])
@login_required
def update_class(cls_id):
    if current_user.is_student():
        return jsonify({'error': 'Unauthorized'}), 403
    
    class_obj = Class.query.get_or_404(cls_id)
    
    # Role-based validation
    if current_user.is_cr() and class_obj.branch_id != current_user.branch_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    
    class_obj.subject = data.get('subject', class_obj.subject)
    class_obj.day = data.get('day', class_obj.day)
    class_obj.room_id = data.get('room_id', class_obj.room_id)
    class_obj.instructor_id = data.get('instructor_id', class_obj.instructor_id)
    class_obj.module_id = data.get('module_id', class_obj.module_id)
    class_obj.branch_id = data.get('branch_id', class_obj.branch_id)
    
    # Parse times
    if 'start_time' in data:
        parts = data['start_time'].split(':')
        class_obj.start_time = time(int(parts[0]), int(parts[1]))
    if 'end_time' in data:
        parts = data['end_time'].split(':')
        class_obj.end_time = time(int(parts[0]), int(parts[1]))
    
    db.session.commit()
    
    return jsonify({'message': 'Class updated successfully!'})

@app.route('/api/classes/<int:cls_id>', methods=['DELETE'])
@login_required
def delete_class(cls_id):
    if current_user.is_student():
        return jsonify({'error': 'Unauthorized'}), 403
    
    class_obj = Class.query.get_or_404(cls_id)
    
    # Role-based validation
    if current_user.is_cr() and class_obj.branch_id != current_user.branch_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    db.session.delete(class_obj)
    db.session.commit()
    
    return jsonify({'message': 'Class deleted successfully!'})

# ==================== ADMIN API ROUTES ====================

@app.route('/api/branches', methods=['GET', 'POST'])
@login_required
def manage_branches():
    if not current_user.is_admin():
        return jsonify({'error': 'Unauthorized'}), 403
    
    if request.method == 'GET':
        branches = Branch.query.all()
        return jsonify([{'id': b.id, 'name': b.name, 'code': b.code} for b in branches])
    
    data = request.json
    new_branch = Branch(name=data['name'], code=data['code'])
    db.session.add(new_branch)
    db.session.commit()
    return jsonify({'message': 'Branch added!'}), 201

@app.route('/api/years', methods=['GET', 'POST'])
@login_required
def manage_years():
    if not current_user.is_admin():
        return jsonify({'error': 'Unauthorized'}), 403
    
    if request.method == 'GET':
        years = Year.query.all()
        return jsonify([{'id': y.id, 'name': y.name} for y in years])
    
    data = request.json
    new_year = Year(name=data['name'])
    db.session.add(new_year)
    db.session.commit()
    return jsonify({'message': 'Year added!'}), 201

@app.route('/api/modules', methods=['GET', 'POST'])
@login_required
def manage_modules():
    if not current_user.is_admin():
        return jsonify({'error': 'Unauthorized'}), 403
    
    if request.method == 'GET':
        modules = Module.query.all()
        return jsonify([{
            'id': m.id, 
            'name': m.name, 
            'year_id': m.year_id,
            'year_name': m.year.name if m.year else None
        } for m in modules])
    
    data = request.json
    new_module = Module(name=data['name'], year_id=data['year_id'])
    db.session.add(new_module)
    db.session.commit()
    return jsonify({'message': 'Module added!'}), 201

@app.route('/api/instructors', methods=['GET', 'POST'])
@login_required
def manage_instructors():
    if not current_user.is_admin():
        return jsonify({'error': 'Unauthorized'}), 403
    
    if request.method == 'GET':
        instructors = Instructor.query.all()
        return jsonify([{
            'id': i.id, 
            'name': i.name, 
            'email': i.email,
            'phone': i.phone,
            'branch_id': i.branch_id,
            'branch_name': i.branch.name if i.branch else None
        } for i in instructors])
    
    data = request.json
    new_instructor = Instructor(
        name=data['name'],
        email=data.get('email'),
        phone=data.get('phone'),
        branch_id=data.get('branch_id')
    )
    db.session.add(new_instructor)
    db.session.commit()
    return jsonify({'message': 'Instructor added!'}), 201

@app.route('/api/rooms', methods=['GET', 'POST'])
@login_required
def manage_rooms():
    if not current_user.is_admin():
        return jsonify({'error': 'Unauthorized'}), 403
    
    if request.method == 'GET':
        rooms = Room.query.all()
        return jsonify([{
            'id': r.id, 
            'name': r.name, 
            'building': r.building,
            'capacity': r.capacity
        } for r in rooms])
    
    data = request.json
    new_room = Room(
        name=data['name'],
        building=data.get('building'),
        capacity=data.get('capacity', 0)
    )
    db.session.add(new_room)
    db.session.commit()
    return jsonify({'message': 'Room added!'}), 201

@app.route('/api/users', methods=['GET'])
@login_required
def manage_users():
    if not current_user.is_admin():
        return jsonify({'error': 'Unauthorized'}), 403
    
    users = User.query.all()
    return jsonify([{
        'id': u.id,
        'username': u.username,
        'role': u.role,
        'branch_id': u.branch_id,
        'branch_name': u.branch.name if u.branch else None,
        'year_id': u.year_id,
        'year_name': u.year.name if u.year else None
    } for u in users])


# Admin DELETE endpoints
@app.route('/api/branches/<int:branch_id>', methods=['DELETE'])
@login_required
def delete_branch(branch_id):
    if not current_user.is_admin():
        return jsonify({'error': 'Unauthorized'}), 403
    branch = Branch.query.get_or_404(branch_id)
    db.session.delete(branch)
    db.session.commit()
    return jsonify({'message': 'Branch deleted!'})


@app.route('/api/years/<int:year_id>', methods=['DELETE'])
@login_required
def delete_year(year_id):
    if not current_user.is_admin():
        return jsonify({'error': 'Unauthorized'}), 403
    year = Year.query.get_or_404(year_id)
    db.session.delete(year)
    db.session.commit()
    return jsonify({'message': 'Year deleted!'})


@app.route('/api/modules/<int:module_id>', methods=['DELETE'])
@login_required
def delete_module(module_id):
    if not current_user.is_admin():
        return jsonify({'error': 'Unauthorized'}), 403
    module = Module.query.get_or_404(module_id)
    db.session.delete(module)
    db.session.commit()
    return jsonify({'message': 'Module deleted!'})


@app.route('/api/instructors/<int:instructor_id>', methods=['DELETE'])
@login_required
def delete_instructor(instructor_id):
    if not current_user.is_admin():
        return jsonify({'error': 'Unauthorized'}), 403
    instr = Instructor.query.get_or_404(instructor_id)
    db.session.delete(instr)
    db.session.commit()
    return jsonify({'message': 'Instructor deleted!'})


@app.route('/api/rooms/<int:room_id>', methods=['DELETE'])
@login_required
def delete_room(room_id):
    if not current_user.is_admin():
        return jsonify({'error': 'Unauthorized'}), 403
    room = Room.query.get_or_404(room_id)
    db.session.delete(room)
    db.session.commit()
    return jsonify({'message': 'Room deleted!'})


@app.route('/api/users/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin():
        return jsonify({'error': 'Unauthorized'}), 403
    if user_id == current_user.id:
        return jsonify({'error': 'Cannot delete yourself'}), 400
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted!'})

# ==================== DATA ROUTES FOR DROPDOWNS ====================

@app.route('/api/dropdown-data')
@login_required
def get_dropdown_data():
    branches = Branch.query.all()
    years = Year.query.all()
    modules = Module.query.all()
    instructors = Instructor.query.all()
    rooms = Room.query.all()
    
    return jsonify({
        'branches': [{'id': b.id, 'name': b.name, 'code': b.code} for b in branches],
        'years': [{'id': y.id, 'name': y.name} for y in years],
        'modules': [{'id': m.id, 'name': m.name, 'year_id': m.year_id} for m in modules],
        'instructors': [{'id': i.id, 'name': i.name} for i in instructors],
        'rooms': [{'id': r.id, 'name': r.name, 'building': r.building} for r in rooms]
    })

if __name__ == '__main__':
    app.run(debug=True)
