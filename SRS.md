# Software Requirements Specification (SRS)
## CIT Class Routine Management System

---

## 1. Introduction

### 1.1 Purpose
The purpose of this document is to provide a detailed description of the CIT Class Routine Management System. This system will allow educational institutions to manage class schedules, instructors, rooms, and branches efficiently with role-based access control.

### 1.2 Scope
The system is a web-based application that manages class routines for an entire institution. It supports multiple branches, years, semesters, rooms, and instructors with different user roles providing varying levels of access.

### 1.3 Definitions, Acronyms, and Abbreviations
- **CIT** - Central Institute of Technology (Kokrajhar)
- **CR** - Class Representative
- **Admin** - System Administrator
- **SRS** - Software Requirements Specification
- **ER** - Entity Relationship
- **DFD** - Data Flow Diagram
- **SQLite** - Lightweight database
- **ORM** - Object-Relational Mapping

---

## 2. Overall Description

### 2.1 User Characteristics
The system has four types of users:
1. **Admin** - Full access to all features and data
2. **Teacher** - Can manage classes they are assigned to
3. **CR (Class Representative)** - Can manage classes for their branch and year
4. **Student** - View-only access to class routines

### 2.2 Product Perspective
This is a web-based application built using:
- Flask (Python web framework)
- SQLite (Database)
- SQLAlchemy (ORM)
- Bootstrap 5 (UI Framework)
- Flask-Login (Authentication)

### 2.3 Functional Requirements

#### 2.3.1 Authentication System
- User registration with role selection
- Login with username and password
- Logout functionality
- Password hashing for security

#### 2.3.2 Branch Management
- Add/Edit/Delete branches
- View list of all branches
- Each branch has: name, code

#### 2.3.3 Year Management
- Add/Edit/Delete academic years
- View list of all years
- Each year has: name (e.g., 1st Year, 2nd Year)

#### 2.3.4 Module/Semester Management
- Add/Edit/Delete modules/semesters
- Assign modules to years
- Each module has: name, year_id

#### 2.3.5 Instructor Management
- Add/Edit/Delete instructors
- Assign instructors to branches
- Each instructor has: name, email, phone, branch_id

#### 2.3.6 Room Management
- Add/Edit/Delete rooms
- Each room has: name, building, capacity

#### 2.3.7 Class Routine Management
- Add/Edit/Delete class schedules
- Assign class to: subject, time, day, room, instructor, module, branch
- Filter by: branch, year, module, day

#### 2.3.8 User Management
- Admin can manage all users
- Assign roles to users
- Link users to branch and year (for CR and students)

---

## 3. Specific Requirements

### 3.1 User Interface

#### Login Page
- Username input field
- Password input field
- Login button
- Link to register new account

#### Registration Page
- Username field
- Password field
- Confirm password field
- Role selection (Teacher, CR, Student)
- Branch selection
- Year selection (for CR and Student)

#### Dashboard Pages (Role-based)

**Admin Dashboard:**
- Overview statistics
- Manage all branches, years, modules, instructors, rooms
- Manage all users
- View all class routines

**Teacher Dashboard:**
- View assigned classes
- Add/Edit/Delete their own classes
- View instructor profile

**CR Dashboard:**
- View classes for their branch and year
- Add/Edit/Delete classes for their branch and year
- View branch information

**Student Dashboard:**
- View classes for their branch and year
- Filter by day

### 3.2 Data Flow

```
User → Login → Dashboard (Role-based)
                ↓
        ┌───────┼───────┐
        ↓       ↓       ↓
    Admin    Teacher   Student
        ↓       ↓       ↓
    All DB   Own DB   View Only
    Operations Operations
```

### 3.3 Database Design

See separate `Database_Design.md` document.

### 3.4 ER Diagram

See separate `ER_Diagram.md` document.

---

## 4. Acceptance Criteria

### 4.1 Authentication
- [ ] Users can register with valid credentials
- [ ] Users can login with correct username and password
- [ ] Invalid login shows appropriate error message
- [ ] Users can logout successfully

### 4.2 Role-based Access
- [ ] Admin can access all features
- [ ] Teachers can only manage their assigned classes
- [ ] CRs can only manage classes for their branch and year
- [ ] Students can only view routines

### 4.3 CRUD Operations
- [ ] All entities can be created, read, updated, and deleted
- [ ] Proper validation on all input forms
- [ ] Success/Error messages displayed after operations

### 4.4 Search and Filter
- [ ] Users can filter routines by branch
- [ ] Users can filter routines by year
- [ ] Users can filter routines by module/semester
- [ ] Users can filter routines by day

---

## 5. Non-Functional Requirements

### 5.1 Performance
- System should respond within 2 seconds
- Support multiple concurrent users

### 5.2 Security
- Passwords stored with hashing (bcrypt)
- Session management
- Role-based access control

### 5.3 Usability
- Clean, intuitive user interface
- Responsive design for mobile devices
- Clear error messages

---

## 6. Appendix

### A. Technology Stack
- Python 3.x
- Flask 2.x
- SQLite
- SQLAlchemy
- Flask-Login
- Bootstrap 5

### B. File Structure
```
/
├── app.py              # Main application
├── config.py           # Configuration
├── models.py           # Database models
├── templates/          # HTML templates
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── index.html
└── static/             # CSS and JS files
    ├── styles.css
    └── script.js
```

---

**Document Version:** 1.0
**Date:** 2024
**Author:** CIT Development Team
