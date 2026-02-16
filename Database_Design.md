# Database Design
## CIT Class Routine Management System

---

## 1. Database Overview

**Database Name:** `cit_routine.db`
**Database Type:** SQLite
**ORM:** SQLAlchemy

---

## 2. Table Structures

### 2.1 Users Table
```
sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK(role IN ('admin', 'teacher', 'cr', 'student')),
    branch_id INTEGER,
    year_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (branch_id) REFERENCES branches(id) ON DELETE SET NULL,
    FOREIGN KEY (year_id) REFERENCES years(id) ON DELETE SET NULL
);
```

**Indexes:**
- `idx_username` on `username`
- `idx_role` on `role`
- `idx_branch_id` on `branch_id`
- `idx_year_id` on `year_id`

---

### 2.2 Branches Table
```
sql
CREATE TABLE branches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Indexes:**
- `idx_branch_code` on `code`
- `idx_branch_name` on `name`

---

### 2.3 Years Table
```
sql
CREATE TABLE years (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Default Values:**
- 1st Year
- 2nd Year
- 3rd Year
- 4th Year

---

### 2.4 Modules Table
```
sql
CREATE TABLE modules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    year_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (year_id) REFERENCES years(id) ON DELETE CASCADE
);
```

**Indexes:**
- `idx_module_year` on `year_id`

---

### 2.5 Instructors Table
```
sql
CREATE TABLE instructors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    branch_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (branch_id) REFERENCES branches(id) ON DELETE SET NULL
);
```

**Indexes:**
- `idx_instructor_branch` on `branch_id`
- `idx_instructor_email` on `email`

---

### 2.6 Rooms Table
```
sql
CREATE TABLE rooms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL,
    building VARCHAR(100),
    capacity INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Indexes:**
- `idx_room_name` on `name`

---

### 2.7 Classes Table
```
sql
CREATE TABLE classes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject VARCHAR(100) NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    day VARCHAR(20) NOT NULL CHECK(day IN ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')),
    room_id INTEGER,
    instructor_id INTEGER,
    module_id INTEGER,
    branch_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE SET NULL,
    FOREIGN KEY (instructor_id) REFERENCES instructors(id) ON DELETE SET NULL,
    FOREIGN KEY (module_id) REFERENCES modules(id) ON DELETE SET NULL,
    FOREIGN KEY (branch_id) REFERENCES branches(id) ON DELETE CASCADE
);
```

**Indexes:**
- `idx_class_branch` on `branch_id`
- `idx_class_room` on `room_id`
- `idx_class_instructor` on `instructor_id`
- `idx_class_module` on `module_id`
- `idx_class_day` on `day`
- `idx_class_time` on `start_time`, `end_time`

---

## 3. Default Data

### 3.1 Default Branches
```
sql
INSERT INTO branches (name, code) VALUES 
('Computer Science', 'CS'),
('Electronics & Communication', 'EC'),
('Civil Engineering', 'CE'),
('Mechanical Engineering', 'ME'),
('Electrical Engineering', 'EE');
```

### 3.2 Default Years
```
sql
INSERT INTO years (name) VALUES 
('1st Year'),
('2nd Year'),
('3rd Year'),
('4th Year');
```

### 3.3 Default Modules
```
sql
-- For 1st Year
INSERT INTO modules (name, year_id) VALUES 
('Semester 1', 1),
('Semester 2', 1);

-- For 2nd Year
INSERT INTO modules (name, year_id) VALUES 
('Semester 3', 2),
('Semester 4', 2);

-- For 3rd Year
INSERT INTO modules (name, year_id) VALUES 
('Semester 5', 3),
('Semester 6', 3);

-- For 4th Year
INSERT INTO modules (name, year_id) VALUES 
('Semester 7', 4),
('Semester 8', 4);
```

### 3.4 Default Rooms
```
sql
INSERT INTO rooms (name, building, capacity) VALUES 
('101', 'Building A', 60),
('102', 'Building A', 60),
('103', 'Building A', 40),
('201', 'Building B', 60),
('202', 'Building B', 60),
('228', 'Building B', 50),
('Lab 1', 'Building C', 30),
('Lab 2', 'Building C', 30);
```

### 3.5 Default Admin User
```
sql
-- Username: admin
-- Password: admin123 (will be hashed)
INSERT INTO users (username, password, role) VALUES 
('admin', '$2b$12$hashed_password_here', 'admin');
```

---

## 4. Database Relationships (Foreign Keys)

```
┌─────────────┐       ┌─────────────┐
│   USERS     │       │   BRANCHES  │
├─────────────┤       ├─────────────┤
│ branch_id ──┼───────┤     id      │
│ year_id   ──┼───────┤     id      │
└─────────────┘       └─────────────┘

┌─────────────┐       ┌─────────────┐
│    YEAR     │       │   MODULES   │
├─────────────┤       ├─────────────┤
│     id      │<──────│  year_id    │
└─────────────┘       └─────────────┘

┌─────────────┐       ┌─────────────┐
│   BRANCHES  │       │ INSTRUCTORS │
├─────────────┤       ├─────────────┤
│     id      │<──────│ branch_id   │
└─────────────┘       └─────────────┘

┌─────────────┐       ┌─────────────┐
│    ROOMS    │       │   CLASSES   │
├─────────────┤       ├─────────────┤
│     id      │<──────│  room_id    │
└─────────────┘       └─────────────┘

┌─────────────┐       ┌─────────────┐
│ INSTRUCTORS │       │   CLASSES   │
├─────────────┤       ├─────────────┤
│     id      │<──────│instructor_id│
└─────────────┘       └─────────────┘

┌─────────────┐       ┌─────────────┐
│   MODULES   │       │   CLASSES   │
├─────────────┤       ├─────────────┤
│     id      │<──────│ module_id   │
└─────────────┘       └─────────────┘

┌─────────────┐       ┌─────────────┐
│   BRANCHES  │       │   CLASSES   │
├─────────────┤       ├─────────────┤
│     id      │<──────│ branch_id   │
└─────────────┘       └─────────────┘
```

---

## 5. Query Examples

### 5.1 Get all classes for a branch and year
```
sql
SELECT c.*, r.name as room_name, i.name as instructor_name, m.name as module_name
FROM classes c
LEFT JOIN rooms r ON c.room_id = r.id
LEFT JOIN instructors i ON c.instructor_id = i.id
LEFT JOIN modules m ON c.module_id = m.id
WHERE c.branch_id = ? AND m.year_id = ?
ORDER BY c.day, c.start_time;
```

### 5.2 Get instructor's classes
```
sql
SELECT c.*, m.name as module_name, b.name as branch_name
FROM classes c
LEFT JOIN modules m ON c.module_id = m.id
LEFT JOIN branches b ON c.branch_id = b.id
WHERE c.instructor_id = ?
ORDER BY c.day, c.start_time;
```

### 5.3 Check room availability
```
sql
SELECT * FROM classes 
WHERE room_id = ? 
AND day = ? 
AND (
    (start_time <= ? AND end_time > ?) 
    OR (start_time < ? AND end_time >= ?)
    OR (start_time >= ? AND end_time <= ?)
);
```

---

## 6. Database Initialization Script

```
python
def init_db():
    """Initialize database with default values"""
    # Create tables
    db.create_all()
    
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
        Room(name='228', building='Building B', capacity=50),
        Room(name='Lab 1', building='Building C', capacity=30),
    ]
    db.session.add_all(rooms)
    
    # Add admin user (password: admin123)
    admin = User(
        username='admin',
        password=generate_password_hash('admin123'),
        role='admin'
    )
    db.session.add(admin)
    
    db.session.commit()
```

---

**Document Version:** 1.0
**Date:** 2024
