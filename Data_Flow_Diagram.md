# Data Flow Diagram (DFD)
## CIT Class Routine Management System

---

## 1. Overview

The Data Flow Diagram shows how data moves through the Class Routine Management System. It illustrates the processes, data stores, external entities, and data flows.

---

## 2. Level 0 - Context Diagram

```
                                    ┌──────────────────────────────────────┐
                                    │                                      │
                                    │     CIT CLASS ROUTINE MANAGEMENT     │
                                    │              SYSTEM                  │
                                    │                                      │
         ┌──────────────────────────┤                                      ├──────────────────────────┐
         │                          │                                      │                          │
         │                          │                                      │                          │
         ▼                          ▼                                      ▼                          ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│      ADMIN      │    │     TEACHER      │    │       CR       │    │     STUDENT     │    │   INSTRUCTOR    │
│   (External     │    │   (External     │    │   (External     │    │   (External     │    │   (External     │
│    Entity)      │    │    Entity)      │    │    Entity)      │    │    Entity)      │    │    Entity)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
        │                      │                      │                      │                      │
        │   Admin Actions      │   Teacher Actions   │    CR Actions       │  Student Actions    │  View Classes
        │   & Management       │   & Management     │   & Management     │   & Viewing         │
        ▼                      ▼                      ▼                      ▼                      ▼
```

---

## 3. Level 1 - Main Processes

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                              SYSTEM BOUNDARY                                               │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐   │
│  │                                                                                                      │   │
│  │    ┌─────────────┐         ┌─────────────┐         ┌─────────────┐         ┌─────────────┐        │   │
│  │    │   BROWSER   │         │   BROWSER   │         │   BROWSER   │         │   BROWSER   │        │   │
│  │    │  (Client)   │         │  (Client)   │         │  (Client)   │         │  (Client)   │        │   │
│  │    └──────┬──────┘         └──────┬──────┘         └──────┬──────┘         └──────┬──────┘        │   │
│  │           │                        │                        │                        │              │   │
│  │           ▼                        ▼                        ▼                        ▼              │   │
│  │    ┌──────────────────────────────────────────────────────────────────────────────────────────┐     │   │
│  │    │                              FLASK APPLICATION                                            │     │   │
│  │    │  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐        │     │   │
│  │    │  │    AUTH        │  │   DASHBOARD    │  │    ROUTINE    │  │   MANAGEMENT  │        │     │   │
│  │    │  │   MODULE      │  │    MODULE      │  │    MODULE     │  │    MODULE     │        │     │   │
│  │    │  │                │  │                │  │                │  │                │        │     │   │
│  │    │  │  - Login      │  │  - Admin View │  │  - View       │  │  - Branch CRUD│        │     │   │
│  │    │  │  - Register   │  │  - Teacher View│ │  - Filter    │  │  - Year CRUD │        │     │   │
│  │    │  │  - Logout     │  │  - CR View     │  │  - Search    │  │  - Module CRUD│        │     │   │
│  │    │  │  - Sessions   │  │  - Student View│  │              │  │  - Room CRUD  │        │     │   │
│  │    │  │                │  │                │  │              │  │  - Instructor  │        │     │   │
│  │    │  │                │  │                │  │              │  │    CRUD        │        │     │   │
│  │    │  │                │  │                │  │              │  │  - Class CRUD  │        │     │   │
│  │    │  └───────┬────────┘  └───────┬────────┘  └───────┬────────┘  └───────┬────────┘        │     │   │
│  │    │          │                    │                    │                    │                │     │   │
│  │    └──────────┼────────────────────┼────────────────────┼────────────────────┼────────────────┘     │   │
│  │               │                    │                    │                    │                      │   │
│  │               ▼                    ▼                    ▼                    ▼                      │   │
│  │    ┌────────────────────────────────────────────────────────────────────────────────────────────┐   │   │
│  │    │                              SQLALCHEMY (ORM)                                             │   │   │
│  │    └─────────────────────────────────┬──────────────────────────────────────────────────────────┘   │   │
│  │                                      │                                                               │   │
│  │                                      ▼                                                               │   │
│  │    ┌────────────────────────────────────────────────────────────────────────────────────────────┐   │   │
│  │    │                              SQLITE DATABASE                                               │   │   │
│  │    │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │   │   │
│  │    │  │  Users   │  │ Branches │  │  Years   │  │ Modules  │  │ Instructors│ │  Rooms   │  │   │   │
│  │    │  └──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │   │   │
│  │    │                                                                                             │   │   │
│  │    │  ┌──────────────────────────────────────────────────────────────────────────────────┐      │   │   │
│  │    │  │                              Classes                                              │      │   │   │
│  │    │  └──────────────────────────────────────────────────────────────────────────────────┘      │   │   │
│  │    └────────────────────────────────────────────────────────────────────────────────────────────┘   │   │
│  └────────────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                              │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Level 2 - Authentication Process

```
┌────────────────────────────────────────────────────────────────┐
│                    AUTHENTICATION PROCESS                       │
│                                                                │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐ │
│  │  User    │    │  Login   │    │ Validate │    │  Create │ │
│  │  Enters  │───▶│   Form   │───▶│   User   │───▶│ Session │ │
│  │ Credentials    │          │    │ Credentials    │          │ │
│  └──────────┘    └──────────┘    └──────┬─────┘    └──────────┘ │
│                                          │                       │
│                                          ▼                       │
│                                   ┌──────────────┐               │
│                                   │   DATABASE   │               │
│                                   │  (Check      │               │
│                                   │   Password)  │               │
│                                   └──────────────┘               │
└────────────────────────────────────────────────────────────────┘
```

**Data Flow:**
1. User enters username and password
2. Form submits to Flask server
3. Server validates credentials against database
4. If valid, create session and redirect to dashboard
5. If invalid, show error message

---

## 5. Level 2 - Class Management Process

```
┌────────────────────────────────────────────────────────────────────────────┐
│                        CLASS MANAGEMENT PROCESS                             │
│                                                                            │
│   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐│
│   │  Admin/CR/  │    │    Form     │    │   Validate │    │   Save to   ││
│   │  Teacher    │───▶│  Submission │───▶│   Input    │───▶│  Database   ││
│   │  Enters     │    │             │    │             │    │             ││
│   │  Class Info │    │             │    │             │    │             ││
│   └─────────────┘    └──────┬──────┘    └──────┬──────┘    └──────┬──────┘│
│                             │                   │                   │        │
│                             ▼                   ▼                   ▼        │
│                      ┌─────────────────────────────────────────────────┐    │
│                      │              CLASSES TABLE                       │    │
│                      │  - subject      - start_time                   │    │
│                      │  - end_time     - day                          │    │
│                      │  - room_id      - instructor_id                │    │
│                      │  - module_id    - branch_id                    │    │
│                      └─────────────────────────────────────────────────┘    │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Level 2 - View Routine Process

```
┌────────────────────────────────────────────────────────────────┐
│                      VIEW ROUTINE PROCESS                       │
│                                                                │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐        │
│  │  Student/   │    │   Filter   │    │  Generate  │        │
│  │  User       │───▶│   Request  │───▶│   Query    │        │
│  │  Selects    │    │   (Branch, │    │            │        │
│  │  Options    │    │   Year,    │    │            │        │
│  │             │    │   Day)     │    │            │        │
│  └─────────────┘    └──────┬──────┘    └──────┬──────┘        │
│                            │                   │                │
│                            ▼                   ▼                │
│                     ┌─────────────────────────────────┐         │
│                     │        DATABASE QUERIES         │         │
│                     │                                 │         │
│                     │ SELECT * FROM classes           │         │
│                     │ WHERE branch_id = ?             │         │
│                     │   AND module_id = ?             │         │
│                     │   AND day = ?                   │         │
│                     │ ORDER BY start_time              │         │
│                     └───────────────┬─────────────────┘         │
│                                     │                             │
│                                     ▼                             │
│                      ┌──────────────────────────┐               │
│                      │    Return Class Data     │               │
│                      │    to Frontend           │               │
│                      └────────────┬─────────────┘               │
│                                   │                             │
│                                   ▼                             │
│                      ┌──────────────────────────┐               │
│                      │   Display in Table      │               │
│                      │   Format                │               │
│                      └──────────────────────────┘               │
└────────────────────────────────────────────────────────────────┘
```

---

## 7. User Roles and Data Access

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    ROLE-BASED ACCESS MATRIX                                │
├──────────────────┬──────────────┬──────────────┬──────────────┬──────────────┬────────────┤
│     Feature      │    Admin     │   Teacher    │      CR      │   Student    │  Anonymous │
├──────────────────┼──────────────┼──────────────┼──────────────┼──────────────┼────────────┤
│ Login/Register   │      ✓       │      ✓       │      ✓       │      ✓       │     ✓      │
│ View All Routines│      ✓       │      ✓       │      ✓       │      ✓       │     ✗      │
│ Add Class        │      ✓       │    Own       │    Own       │      ✗       │     ✗      │
│ Edit Class       │      ✓       │    Own       │    Own       │      ✗       │     ✗      │
│ Delete Class     │      ✓       │    Own       │    Own       │      ✗       │     ✗      │
│ Manage Branches  │      ✓       │      ✗       │      ✗       │      ✗       │     ✗      │
│ Manage Years     │      ✓       │      ✗       │      ✗       │      ✗       │     ✗      │
│ Manage Modules   │      ✓       │      ✗       │      ✗       │      ✗       │     ✗      │
│ Manage Rooms     │      ✓       │      ✗       │      ✗       │      ✗       │     ✗      │
│ Manage Instructors│     ✓       │      ✗       │      ✗       │      ✗       │     ✗      │
│ Manage Users     │      ✓       │      ✗       │      ✗       │      ✗       │     ✗      │
└──────────────────┴──────────────┴──────────────┴──────────────┴──────────────┴────────────┘
```

---

## 8. Data Flow Summary

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            DATA FLOW SUMMARY                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1. USER INPUT → FORM VALIDATION → DATABASE → RESPONSE                     │
│                                                                             │
│     Example: Add New Class                                                 │
│     ┌────────┐    ┌────────┐    ┌──────────┐    ┌─────────┐               │
│     │ User   │───▶│ Form   │───▶│ Validate │───▶│ Insert  │───▶ Success   │
│     │ Input  │    │ Data   │    │  Data   │    │  Query  │    Message    │
│     └────────┘    └────────┘    └──────────┘    └─────────┘               │
│                                                                             │
│  2. USER REQUEST → FILTER → QUERY → PROCESS → DISPLAY                     │
│                                                                             │
│     Example: View Routine                                                  │
│     ┌────────┐    ┌────────┐    ┌──────────┐    ┌─────────┐               │
│     │ Select │───▶│ Build  │───▶│ Execute  │───▶│ Render  │───▶ HTML      │
│     │ Filter │    │  Query │    │  Query   │    │  Data   │    Table      │
│     └────────┘    └────────┘    └──────────┘    └─────────┘               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 9. API Endpoints (Data Flow)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              API ENDPOINTS                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  AUTHENTICATION                                                            │
│  ─────────────────                                                          │
│  POST   /auth/register    - Register new user                             │
│  POST   /auth/login       - Login user                                    │
│  POST   /auth/logout      - Logout user                                   │
│                                                                             │
│  CLASSES                                                                   │
│  ────────                                                                  │
│  GET    /api/classes          - Get all classes (filtered by role)        │
│  POST   /api/classes          - Add new class (admin/cr/teacher only)     │
│  PUT    /api/classes/<id>     - Update class (admin/cr/teacher only)      │
│  DELETE /api/classes/<id>     - Delete class (admin/cr/teacher only)     │
│                                                                             │
│  BRANCHES                                                                  │
│  ────────                                                                  │
│  GET    /api/branches        - Get all branches                           │
│  POST   /api/branches        - Add new branch (admin only)                 │
│  PUT    /api/branches/<id>   - Update branch (admin only)                 │
│  DELETE /api/branches/<id>   - Delete branch (admin only)                 │
│                                                                             │
│  YEARS                                                                     │
│  ──────                                                                     │
│  GET    /api/years          - Get all years                               │
│  POST   /api/years          - Add new year (admin only)                   │
│  PUT    /api/years/<id>     - Update year (admin only)                    │
│  DELETE /api/years/<id>     - Delete year (admin only)                    │
│                                                                             │
│  MODULES                                                                   │
│  ────────                                                                  │
│  GET    /api/modules        - Get all modules                             │
│  POST   /api/modules        - Add new module (admin only)                 │
│  PUT    /api/modules/<id>   - Update module (admin only)                  │
│  DELETE /api/modules/<id>    - Delete module (admin only)                  │
│                                                                             │
│  INSTRUCTORS                                                               │
│  ───────────                                                               │
│  GET    /api/instructors    - Get all instructors                         │
│  POST   /api/instructors    - Add new instructor (admin only)              │
│  PUT    /api/instructors/<id> - Update instructor (admin only)            │
│  DELETE /api/instructors/<id> - Delete instructor (admin only)            │
│                                                                             │
│  ROOMS                                                                     │
│  ──────                                                                    │
│  GET    /api/rooms          - Get all rooms                               │
│  POST   /api/rooms          - Add new room (admin only)                    │
│  PUT    /api/rooms/<id>    - Update room (admin only)                      │
│  DELETE /api/rooms/<id>    - Delete room (admin only)                      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

**Document Version:** 1.0
**Date:** 2024
