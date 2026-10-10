# AI-Powered Task Management System

**Submission for**: Kanishka Software Pvt Ltd — Python & AI Integration Intern (24-Hour Assessment)  
**Candidate**: Vishal Sahani  
**Degree**: B.E. Information Technology (Graduation Year: 2027)  
**GitHub Repository**: [https://github.com/vishalsahanipvppcoe/ai-python_developer_intern](https://github.com/vishalsahanipvppcoe/ai-python_developer_intern)  

---

## 1. Project Overview

The **AI-Powered Task Management System** is a robust, production-ready backend service designed and built with **Python**, **FastAPI**, **PostgreSQL**, **SQLAlchemy ORM**, **Alembic**, and **Google Gemini AI**. 

It delivers end-to-end task lifecycle management with fine-grained **Role-Based Access Control (RBAC)**, secure **OAuth2 JWT authentication**, automated **Alembic database migrations**, database **seeding**, and an intelligent **AI task description generator**.

---

## 2. Assessment Requirements Compliance Matrix

| Requirement Area | Specification | Implementation Details | Status |
| :--- | :--- | :--- | :--- |
| **Technology** | Python, FastAPI, PostgreSQL, JWT, LLM API | Python 3.10+, FastAPI, PostgreSQL, `python-jose`, Google Gemini API | **100% Complete** |
| **Users & Auth** | `users` table: id, name, email, password, role, created_at, updated_at | Bcrypt password hashing, registration, login returning JWT, `/api/auth/me` profile | **100% Complete** |
| **Roles** | `user` and `admin` roles | Public registration defaults to `user`; RBAC route guards prevent privilege escalation | **100% Complete** |
| **Tasks** | `tasks` table: id, user_id, title, description, status, created_at, updated_at | FK to users, statuses: `Pending`, `In Progress`, `Testing`, `Completed` | **100% Complete** |
| **Task APIs** | Create, List, View, Update, Update Status | REST endpoints under `/api/tasks` with status codes 201, 200, 401, 403, 404, 422 | **100% Complete** |
| **Access Control** | Users manage own tasks; cannot update status. Admin manages all and updates status. | Enforced in `app/services/task.py` and `app/api/task.py` with 403 HTTP exceptions | **100% Complete** |
| **AI Integration** | `POST /api/tasks/generate-description` | Isolated in `app/ai/gemini.py`, handles 429, 502, 503, 504 errors gracefully | **100% Complete** |
| **Database** | PostgreSQL + Migrations + Seeder (No bare SQL) | Alembic migration (`5bd10a5e9407_init.py`), automated seeder (`seed.py`) | **100% Complete** |
| **API Testing** | Postman collection covering all flows | `ai_task_manager_postman.json` covers auth, tasks, RBAC, AI, and error cases | **100% Complete** |
| **Test Suite** | Automated unit and integration tests | 39 automated tests with in-memory SQLite and mocked Gemini client | **100% Complete (39/39 Passed)** |

---

## 3. Technology Stack

- **Backend Framework**: [FastAPI](https://fastapi.tiangolo.com/) (High-performance ASGI framework)
- **ASGI Server**: [Uvicorn](https://www.uvicorn.org/)
- **Database Engine**: [PostgreSQL](https://www.postgresql.org/) (Production runtime) & SQLite in-memory (Test runner)
- **ORM**: [SQLAlchemy 2.0](https://www.sqlalchemy.org/)
- **Database Migrations**: [Alembic](https://alembic.sqlalchemy.org/)
- **Data Validation & Settings**: [Pydantic v2](https://docs.pydantic.dev/) & [pydantic-settings](https://github.com/pydantic/pydantic-settings)
- **Authentication**: JWT via [python-jose](https://python-jose.readthedocs.io/), Password Hashing via [passlib](https://passlib.readthedocs.io/) and `bcrypt`
- **AI Integration**: [Google Gemini API](https://ai.google.dev/) (`google-generativeai`)
- **Automated Testing**: [pytest](https://pytest.org/) and [HTTPX](https://www.python-httpx.org/)

---

## 4. Project Directory Structure

```text
ai-python_developer_intern/
├── alembic/                      # Alembic schema migrations
│   ├── versions/                 # Versioned database migration scripts
│   │   └── 5bd10a5e9407_init.py  # Initial migration (users & tasks tables)
│   ├── env.py                    # Migration environment and model binding
│   └── script.py.mako            # Migration template
├── app/                          # Core application package
│   ├── ai/                       # AI service layer
│   │   ├── __init__.py
│   │   └── gemini.py             # Google Gemini client and robust error handling
│   ├── api/                      # REST API routing controllers
│   │   ├── __init__.py
│   │   ├── auth.py               # Authentication endpoints (/api/auth)
│   │   └── task.py               # Task management endpoints (/api/tasks)
│   ├── auth/                     # Security, hashing, and token dependencies
│   │   ├── __init__.py
│   │   ├── dependencies.py       # Current user & Admin RBAC route guards
│   │   └── security.py           # Bcrypt password hashing & JWT encoding/decoding
│   ├── database/                 # Database connection & session lifecycle
│   │   ├── __init__.py
│   │   ├── base.py               # Declarative Base
│   │   └── session.py            # Engine, SessionLocal, and get_db dependency
│   ├── models/                   # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── task.py               # Task model & StatusEnum
│   │   └── user.py               # User model & RoleEnum
│   ├── schemas/                  # Pydantic schemas (Request / Response DTOs)
│   │   ├── __init__.py
│   │   ├── task.py               # TaskCreate, TaskUpdate, TaskStatusUpdate, TaskOut
│   │   ├── token.py              # Token schemas
│   │   └── user.py               # UserCreate, UserOut schemas
│   ├── services/                 # Business logic layer
│   │   ├── __init__.py
│   │   ├── task.py               # Task CRUD & authorization validation
│   │   └── user.py               # User creation & credential authentication
│   └── main.py                   # FastAPI application initialization & routing
├── tests/                        # Automated Pytest test suite
│   ├── conftest.py               # Test database fixtures, mock client & tokens
│   ├── test_ai.py                # AI endpoint tests & mocked failure conditions
│   ├── test_auth.py              # Registration, login, and JWT validation tests
│   └── test_task.py              # Task CRUD, ownership, and admin RBAC tests
├── .env.example                  # Environment variable template with placeholders
├── .gitignore                    # Git exclusions (.env, .venv, *.db, caches)
├── alembic.ini                   # Alembic configuration
├── ai_task_manager_postman.json  # Comprehensive Postman API collection
├── requirements.txt              # Project dependencies
├── seed.py                       # Automated database seeder (admin, user, sample tasks)
├── verify_config.py              # Environment configuration audit tool
└── README.md                     # Comprehensive project documentation
```

---

## 5. Prerequisites & Environment Setup

### Prerequisites
- **Python**: Version 3.10, 3.11, or 3.12 recommended
- **PostgreSQL**: Version 13+ running locally or remotely
- **Git**: Installed on your system

### Step 1: Clone Repository
```bash
git clone https://github.com/vishalsahanipvppcoe/ai-python_developer_intern.git
cd ai-python_developer_intern
```

### Step 2: Create & Activate Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
python -m venv .venv
.\.venv\Scripts\activate.bat
```

**Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies
```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

---

## 6. Environment Configuration

Copy the `.env.example` file to create your local `.env`:

```bash
# Windows PowerShell
Copy-Item .env.example .env

# Linux / macOS
cp .env.example .env
```

Open `.env` and fill in your local settings:

```env
# Database Configuration (PostgreSQL)
DATABASE_URL=postgresql+psycopg2://postgres:yourpassword@localhost:5432/ai_task_manager

# Security Configuration
SECRET_KEY=generate_a_random_secure_secret_key_here_at_least_32_characters
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI Integration (Google Gemini)
GEMINI_API_KEY=paste_your_google_gemini_api_key_here
```

> **Security Note**: Never commit your `.env` file or API keys. `.env` is strictly excluded in `.gitignore`.

---

## 7. Database Setup, Migrations & Seeder

### Step 1: Create Database in PostgreSQL
Ensure PostgreSQL is active, then create the database:
```sql
CREATE DATABASE ai_task_manager;
```

### Step 2: Run Alembic Migrations
Apply versioned migrations to generate the schema:
```bash
alembic upgrade head
```

To view the generated SQL without applying it:
```bash
alembic upgrade head --sql
```

### Step 3: Seed Database with Initial Test Data
Run the seeder script to populate default admin, standard user, and sample tasks:
```bash
python seed.py
```

### Seeded Test Credentials
| Account Role | Email | Password | Allowed Capabilities |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin@example.com` | `admin123` | View all tasks across users, edit any task, update task status |
| **Standard User** | `user@example.com` | `user123` | Create tasks, view/edit own tasks only; cannot update status |

---

## 8. Running the Application

Launch the FastAPI application using Uvicorn:
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

The server starts at `http://127.0.0.1:8000`.

- **Health Check**: `GET http://127.0.0.1:8000/health`
- **Interactive Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc Documentation**: `http://127.0.0.1:8000/redoc`

---

## 9. API Reference & Authentication Workflow

All protected endpoints require an `Authorization` header:
```http
Authorization: Bearer <your_access_token>
```

### 1. Authentication Endpoints (`/api/auth`)

| Method | Endpoint | Access | Description |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/auth/register` | Public | Register a new user (`name`, `email`, `password`) |
| `POST` | `/api/auth/login` | Public | OAuth2 Form login (`username`, `password`) returning JWT token |
| `GET` | `/api/auth/me` | Authenticated | Retrieve current user profile |

**Sample Login Request (`POST /api/auth/login`):**
```http
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=user123
```

**Sample Login Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

### 2. Task Management Endpoints (`/api/tasks`)

| Method | Endpoint | Access | Description |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/tasks` | Authenticated | Create a task (`title`, `description`) |
| `GET` | `/api/tasks` | Authenticated | List tasks (User: own tasks; Admin: all tasks) |
| `GET` | `/api/tasks/{task_id}` | Authenticated | Get task by ID (Owner or Admin) |
| `PATCH` | `/api/tasks/{task_id}` | Authenticated | Edit task title and description (Owner or Admin) |
| `PATCH` | `/api/tasks/{task_id}/status` | **Admin Only** | Update task status (`Pending`, `In Progress`, `Testing`, `Completed`) |

**Sample Create Task Request (`POST /api/tasks`):**
```json
{
  "title": "Set up PostgreSQL Connection Pooling",
  "description": "Configure SQLAlchemy pool_size and max_overflow parameters."
}
```

**Sample Create Task Response (201 Created):**
```json
{
  "id": 1,
  "user_id": 2,
  "title": "Set up PostgreSQL Connection Pooling",
  "description": "Configure SQLAlchemy pool_size and max_overflow parameters.",
  "status": "Pending",
  "created_at": "2026-10-10T12:00:00Z",
  "updated_at": null
}
```

**Sample Status Update Request (`PATCH /api/tasks/1/status` - Admin Only):**
```json
{
  "status": "Completed"
}
```

---

### 3. AI Feature (`POST /api/tasks/generate-description`)

Accepts a task title and uses Google Gemini to generate a professional, concise task description.

**Sample Request:**
```json
{
  "title": "Build user notification subsystem"
}
```

**Sample Response (200 OK):**
```json
{
  "description": "Architect and implement an asynchronous notification engine supporting email alerts and event queues with retries and rate limiting."
}
```

**AI Error Handling & Status Codes:**
- `503 Service Unavailable`: Gemini API key not configured or contains placeholder text.
- `429 Too Many Requests`: Upstream Gemini API rate limit exceeded.
- `504 Gateway Timeout`: Upstream AI call timed out.
- `502 Bad Gateway`: Empty response or provider communication error.
- `422 Unprocessable Entity`: Title is empty or whitespace-only.

---

## 10. Role-Based Access Control (RBAC) Matrix

| Operation | Regular User (`role="user"`) | Administrator (`role="admin"`) |
| :--- | :---: | :---: |
| Register account | Allowed (Assigned `user` role) | Admin created via seeder / DB |
| Login & acquire JWT | Allowed | Allowed |
| View own tasks | Allowed | Allowed |
| View other users' tasks | **Denied (403 Forbidden)** | **Allowed** |
| Create new tasks | Allowed | Allowed |
| Edit own task (title/desc) | Allowed | Allowed |
| Edit other users' tasks | **Denied (403 Forbidden)** | **Allowed** |
| Update task status | **Denied (403 Forbidden)** | **Allowed** |
| Call AI description API | Allowed | Allowed |

---

## 11. Automated Test Suite Execution

The automated test suite runs against an isolated in-memory SQLite database (`StaticPool`) and mocks the Google Gemini API, ensuring tests execute quickly without consuming API credits or requiring a running PostgreSQL server.

Run tests:
```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

### Actual Test Results
```text
.......................................                                  [100%]
39 passed, 2 warnings in 26.44s
```

### Test Coverage Breakdown:
1. **`tests/test_auth.py`** (11 tests):
   - User registration (201) & duplicate email prevention (400)
   - Password minimum length (>= 8 chars) & email format validation (422)
   - Correct credentials login & JWT issuance (200)
   - Incorrect password / nonexistent user rejection (401)
   - Missing token, invalid token, and expired token handling (401)
   - `/api/auth/me` user profile extraction
2. **`tests/test_task.py`** (18 tests):
   - Task creation with non-empty title validation (201 & 422)
   - User task listing (isolation) vs. Admin task listing (sees all tasks)
   - Task retrieval by ID (Owner 200, Other User 403, Nonexistent 404)
   - Task title/description editing (Owner 200, Admin 200, Other User 403)
   - Task status update: Admin allows all valid statuses (`Pending`, `In Progress`, `Testing`, `Completed`)
   - Task status update: Regular user strictly forbidden (403)
   - Invalid status values rejected (422)
   - Unauthenticated access rejected (401)
3. **`tests/test_ai.py`** (10 tests):
   - Successful description generation with mocked Gemini responses
   - Empty or whitespace-only title validation (422)
   - Unauthenticated AI endpoint access (401)
   - Unconfigured / placeholder API key handling (503)
   - Rate limit simulation (`ResourceExhausted` -> 429)
   - Timeout simulation (`DeadlineExceeded` -> 504)
   - Provider error simulation (`GoogleAPIError` -> 502)
   - Empty AI response handling (502)

---

## 12. Postman Collection

The repository includes a ready-to-use Postman collection: `ai_task_manager_postman.json`.

### How to Use:
1. Open Postman, click **Import**, and select `ai_task_manager_postman.json`.
2. Ensure the collection variable `base_url` is set to `http://localhost:8000`.
3. Run `1. Authentication -> Login Regular User`. The test script automatically stores `user_token`.
4. Run `1. Authentication -> Login Admin`. The test script automatically stores `admin_token`.
5. Run the requests in:
   - `2. Regular User Tasks`: Creates a task and saves `task_id`.
   - `3. Admin Task Operations`: Demonstrates admin status updates and cross-user task management.
   - `4. AI Integration`: Tests `POST /api/tasks/generate-description`.
   - `5. Authorization & Error Scenarios`: Verifies 403 on user status update, 401 unauthenticated, and 422 validation errors.

---

## 13. Important Architectural Decisions & Assumptions

1. **Separation of Concerns**:
   - `models/`: Database schema representation.
   - `schemas/`: Request and response validation contracts.
   - `services/`: Business logic, domain rules, and RBAC authorization assertions.
   - `api/`: HTTP route handlers and dependency injection.
   - `ai/`: Encapsulated external AI communication and error mapping.
2. **AI SDK Evaluation**:
   - Google recently released the `google.genai` SDK while marking `google.generativeai` with a future migration advisory. The application utilizes `google-generativeai` pinned in `requirements.txt` to preserve verified stability, complete mock coverage, and 100% passing tests.
3. **Strict RBAC Enforcement**:
   - Standard users cannot promote themselves during registration (`role` is omitted from `UserCreate` schema and hardcoded to `user` in service logic).
   - Updating task status is guarded by the `get_current_admin_user` dependency, returning 403 Forbidden to non-admin users.
4. **Data Integrity & Auditability**:
   - Tasks are managed via status transitions (`Pending` -> `In Progress` -> `Testing` -> `Completed`). Hard deletion is intentionally omitted to maintain historical task records.

---

## 14. Verification & Secret Protection

- **No Secrets Tracked**: `.env` is verified untracked by Git; `.env.example` contains placeholders only.
- **No Local Artifacts**: `.venv`, `__pycache__`, `.pytest_cache`, and SQLite databases are strictly ignored.
- **Identity**: Commits are made using the verified author:  
  `Vishal Sahani <vu4f2324152@pvppcoe.ac.in>`.
