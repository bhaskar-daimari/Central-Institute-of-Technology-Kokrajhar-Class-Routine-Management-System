# Entity Relationship (ER) Diagram
## CIT Class Routine Management System

---

## 1. ER Diagram Overview

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                          CIT CLASS ROUTINE MANAGEMENT SYSTEM                             │
│                                ER DIAGRAM                                                │
└─────────────────────────────────────────────────────────────────────────────────────────┘

                                    ┌─────────────┐
                                    │    USER     │
                                    ├─────────────┤
                                    │ PK  id      │
                                    │    username │
                                    │    password │
                                    │ FK  role    │──────────┐
                                    │ FK  branch_id   │          │
                                    │ FK  year_id     │          │
                                    └─────────────┘          │
                                           │                  │
                                           │                  │
                      ┌────────────────────┼──────────────────┘
                      │                    │
                      │                    │
                      ▼                    ▼
              ┌───────────────┐    ┌─────────────────┐
              │    BRANCH     │    │      YEAR       │
              ├───────────────┤    ├─────────────────┤
              │ PK  id        │    │ PK  id          │
              │    name       │    │    name         │
              │    code       │    └─────────────────┘
              └───────────────┘              │
                      │                       │
                      │                       │
                      │                       │
                      ▼                       ▼
              ┌───────────────┐    ┌─────────────────┐
              │   INSTRUCTOR  │    │     MODULE      │
              ├───────────────┤    ├─────────────────┤
              │ PK  id        │    │ PK  id          │
              │    name       │    │    name         │
              │    email      │────│ FK  year_id    │
              │    phone      │    └─────────────────┘
              │ FK  branch_id │              │
              └───────────────┘              │
                      │                      │
                      │                      │
                      ▼                      ▼
              ┌───────────────┐    ┌─────────────────┐
              │     ROOM      │    │     CLASS       │
              ├───────────────┤    ├─────────────────┤
              │ PK  id        │    │ PK  id          │
              │    name       │    │    subject      │
              │    building   │    │    start_time   │
              │    capacity   │    │    end_time     │
              └───────────────┘    │    day          │
                                   │ FK  room_id     │
                                   │ FK  instructor_id│
                                   │ FK  module_id   │
                                   │ FK  branch_id   │
                                   └─────────────────┘
```

---

## 2. Entity Descriptions

### 2.1 USER Entity
| Attribute | Type | Description |
|-----------|------|-------------|
| id | Integer | Primary Key, Auto-increment |
| username | String(50) | Unique, Not Null |
| password | String(255) | Hashed password |
| role | String(20) | admin, teacher, cr, student |
| branch_id | Integer | Foreign Key (references Branch) |
| year_id | Integer | Foreign Key (references Year) |

**Relationships:**
- Many-to-One with BRANCH (a user belongs to one branch)
- Many-to-One with YEAR (a user belongs to one year)

---

### 2.2 BRANCH Entity
| Attribute | Type | Description |
|-----------|------|-------------|
| id | Integer | Primary Key, Auto-increment |
| name | String(100) | Branch name (e.g., Computer Science) |
| code | String(20) | Branch code (e.g., CS, EC, CE) |

**Relationships:**
- One-to-Many with USER (a branch can have many users)
- One-to-Many with INSTRUCTOR (a branch can have many instructors)
- One-to-Many with CLASS (a branch can have many classes)

---

### 2.3 YEAR Entity
| Attribute | Type | Description |
|-----------|------|-------------|
| id | Integer | Primary Key, Auto-increment |
| name | String(50) | Year name (e.g., 1st Year, 2nd Year) |

**Relationships:**
- One-to-Many with USER (a year can have many users)
- One-to-Many with MODULE (a year can have many modules)

---

### 2.4 MODULE Entity
| Attribute | Type | Description |
|-----------|------|-------------|
| id | Integer | Primary Key, Auto-increment |
| name | String(100) | Module/Semester name |
| year_id | Integer | Foreign Key (references Year) |

**Relationships:**
- Many-to-One with YEAR (a module belongs to one year)
- One-to-Many with CLASS (a module can have many classes)

---

### 2.5 INSTRUCTOR Entity
| Attribute | Type | Description |
|-----------|------|-------------|
| id | Integer | Primary Key, Auto-increment |
| name | String(100) | Instructor name |
| email | String(100) | Instructor email |
| phone | String(20) | Phone number |
| branch_id | Integer | Foreign Key (references Branch) |

**Relationships:**
- Many-to-One with BRANCH (an instructor belongs to one branch)
- One-to-Many with CLASS (an instructor can teach many classes)

---

### 2.6 ROOM Entity
| Attribute | Type | Description |
|-----------|------|-------------|
| id | Integer | Primary Key, Auto-increment |
| name | String(50) | Room name/number |
| building | String(100) | Building name |
| capacity | Integer | Seating capacity |

**Relationships:**
- One-to-Many with CLASS (a room can have many classes)

---

### 2.7 CLASS Entity
| Attribute | Type | Description |
|-----------|------|-------------|
| id | Integer | Primary Key, Auto-increment |
| subject | String(100) | Subject name |
| start_time | Time | Class start time |
| end_time | Time | Class end time |
| day | String(20) | Day of week (Monday, Tuesday, etc.) |
| room_id | Integer | Foreign Key (references Room) |
| instructor_id | Integer | Foreign Key (references Instructor) |
| module_id | Integer | Foreign Key (references Module) |
| branch_id | Integer | Foreign Key (references Branch) |

**Relationships:**
- Many-to-One with ROOM (a class is in one room)
- Many-to-One with INSTRUCTOR (a class is taught by one instructor)
- Many-to-One with MODULE (a class belongs to one module)
- Many-to-One with BRANCH (a class is for one branch)

---

## 3. Relationship Cardinalities

| Relationship | Type | Description |
|--------------|------|-------------|
| User - Branch | Many-to-One | Many users belong to one branch |
| User - Year | Many-to-One | Many users belong to one year |
| Instructor - Branch | Many-to-One | Many instructors belong to one branch |
| Module - Year | Many-to-One | Many modules belong to one year |
| Class - Room | Many-to-One | Many classes use one room |
| Class - Instructor | Many-to-One | Many classes taught by one instructor |
| Class - Module | Many-to-One | Many classes in one module |
| Class - Branch | Many-to-One | Many classes for one branch |

---

## 4. Entity-Relationship Matrix

|           | User | Branch | Year | Module | Instructor | Room | Class |
|-----------|------|--------|------|--------|------------|------|-------|
| User      | -    | M:1    | M:1  | -      | -          | -    | -     |
| Branch    | 1:M  | -      | -    | -      | 1:M        | -    | 1:M   |
| Year      | 1:M  | -      | -    | 1:M    | -          | -    | -     |
| Module    | -    | -      | 1:M  | -      | -          | -    | 1:M   |
| Instructor| -    | 1:M    | -    | -      | -          | -    | 1:M   |
| Room      | -    | -      | -    | -      | -          | -    | 1:M   |
| Class     | -    | 1:M    | -    | M:1    | M:1        | M:1  | -     |

---

## 5. Key Business Rules

1. **User Roles:**
   - Admin: Can perform all CRUD operations on all entities
   - Teacher: Can only manage classes where they are the instructor
   - CR: Can only manage classes for their assigned branch and year
   - Student: Can only view classes for their assigned branch and year

2. **Class Scheduling:**
   - A room cannot be double-booked at the same time and day
   - An instructor cannot teach two classes at the same time
   - Class times should fall within valid time ranges

3. **Data Integrity:**
   - All foreign keys must reference valid primary keys
   - User must have either branch_id (for students/CR) or null (for admin)
   - Year must be associated with modules

---

## 6. ER Diagram Notation

This ER diagram uses the **Crow's Foot notation**:

```
┌─────┐       ┌─────┐
│  1  │───<   │  N  │  = One-to-Many
└─────┘       └─────┘

┌─────┐       ┌─────┐
│  N  │>──<   │  M  │  = Many-to-Many
└─────┘       └─────┘

┌─────┐       ┌─────┐
│  1  │───<   │  0  │  = One-to-Zero
└─────┘       └─────┘
```

---

**Document Version:** 1.0
**Date:** 2024
