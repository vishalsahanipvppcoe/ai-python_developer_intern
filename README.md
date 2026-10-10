# AI-Powered Task Management System

A production-grade Python backend built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, **Alembic**, and **Google Gemini AI**. The application provides secure user authentication, role-based access control (RBAC), task lifecycle management, and automated task description generation powered by AI.

---

## 1. Technology Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python 3.10+)
- **Server**: [Uvicorn](https://www.uvicorn.org/) (ASGI server)
- **Database**: [PostgreSQL](https://www.postgresql.org/) (Production) & SQLite (In-Memory for unit/integration testing)
- **ORM & Migrations**: [SQLAlchemy 2.0](https://www.sqlalchemy.org/) & [Alembic](https://alembic.sqlalchemy.org/)
- **Data Validation & Settings**: [Pydantic v2](https://docs.pydantic.dev/) & [pydantic-settings](https://github.com/pydantic/pydantic-settings)
- **Authentication & Security**: JWT (`python-jose`), Password Hashing (`passlib` + `bcrypt`)
- **AI Integration**: [Google Gemini API](https://ai.google.dev/) (`google-generativeai`)
- **Testing**: [Pytest](https://pytest.org/) & [HTTPX](https://www.python-httpx.org/)

---

## 2. Feature List

- **User Authentication**:
  - Secure registration with email validation and minimum password complexity (>= 8 characters).
  - Password hashing with Bcrypt.
  - OAuth2 Password Bearer flow issuing JSON Web Tokens (JWT).
  - Protected current-user endpoint (`GET /api/auth/me`).
- **Role-Based Access Control (RBAC)**:
  - Users are assigned `user` (default) or `admin` roles.
  - Regular users can view, create, and update only their own tasks.
  - Administrators can inspect all tasks across all users and modify any task.
  - Task status transition (`Pending`, `In Progress`, `Testing`, `Completed`) is strictly restricted to administrator privileges.
- **AI-Powered Task Descriptions**:
  - `POST /api/tasks/generate-description` creates concise, professional task descriptions using Google Gemini.
  - Robust exception handling for rate limits (429), timeouts (504), upstream failures (502), and unconfigured keys (503).
  - Generated descriptions are returned directly without creating persistent task records unless requested.
- **Automated Database Migrations**:
  - Version-controlled schema migrations using Alembic.
  - Offline SQL generation supported.
- **Comprehensive Automated Testing**:
  - 39 automated tests covering authentication, RBAC, CRUD operations, edge cases, validation, and Gemini AI mocking.
  - 100% isolated test database using in-memory SQLite with `StaticPool`.

---

## 3. Project Structure

```text
ai-task-manager/
├── alembic/                      # Alembic migration environment
│   ├── versions/                 # Versioned migration scripts
│   │   └── 5bd10a5e9407_init.py  # Initial database schema migration
│   ├── env.py                    # Migration runtime configuration
│   └── script.py.mako            # Template for new migrations
├── app/                          # Core application package
│   ├── ai/                       # AI integrations
│   │   └── gemini.py             # Google Gemini client and error handling
│   ├── api/                      # FastAPI route controllers
│   │   ├── auth.py               # Authentication routes (/api/auth)
│   │   └── task.py               # Task management routes (/api/tasks)
│   ├── auth/                     # Security and authorization layer
│   │   ├── dependencies.py       # Auth dependencies (get_current_user, get_current_admin_user)
│   │   └── security.py           # Password hashing & JWT generation/verification
│   ├── database/                 # Database connection and session management
│   │   ├── base.py               # Declarative Base
│   │   └── session.py            # Engine and SessionLocal session factory
│   ├── models/                   # SQLAlchemy ORM models
│   │   ├── task.py               # Task model & StatusEnum
│   │   └── user.py               # User model & RoleEnum
│   ├── schemas/                  # Pydantic schemas (request/response validation)
│   │   ├── task.py               # TaskCreate, TaskUpdate, TaskStatusUpdate, TaskOut
│   │   ├── token.py              # Token, TokenData schemas
│   │   └── user.py               # UserCreate, UserOut schemas
│   ├── services/                 # Business logic service layer
│   │   ├── task.py               # Task CRUD & authorization checks
│   │   └── user.py               # User creation & authentication logic
│   └── main.py                   # FastAPI application initialization & routing
├── tests/                        # Automated test suite
│   ├── conftest.py               # Pytest fixtures, mock DB setup, shared auth tokens
│   ├── test_ai.py                # AI endpoint tests with Gemini mocks
│   ├── test_auth.py              # User registration, login, and JWT tests
│   └── test_task.py              # Task CRUD, ownership, and RBAC tests
├── .env.example                  # Environment configuration template (placeholders only)
├── .gitignore                    # Git exclusions (.env, .venv, *.db, pycache)
├── alembic.ini                   # Alembic configuration
├── ai_task_manager_postman.json  # Postman API Collection
├── requirements.txt              # Production and development dependencies
├── seed.py                       # Database seeder (admin, user, sample tasks)
└── README.md                     # Project documentation
```

---

## 4. Prerequisites

- **Python**: Version 3.10 to 3.14
- **PostgreSQL**: Version 13+ (or another running instance)
- **Git**: Installed and configured on your system

---

## 5. Setup and Installation

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd ai-task-manager
```

### Step 2: Create and Activate Virtual Environment

**On Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**On Windows (Command Prompt):**
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

**On Linux / macOS:**
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

1. Copy `.env.example` to `.env`:

   ```bash
   # Windows PowerShell
   Copy-Item .env.example .env

   # Linux / macOS
   cp .env.example .env
   ```

2. Open `.env` in your text editor and update the placeholders with your actual local configuration:

```env
# Database Configuration (PostgreSQL)
DATABASE_URL=postgresql+psycopg2://<DB_USER>:<DB_PASSWORD>@localhost:5432/<DB_NAME>

# Security Configuration
SECRET_KEY=<GENERATE_A_SECURE_RANDOM_SECRET_KEY>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI Integration
GEMINI_API_KEY=<YOUR_GOOGLE_GEMINI_API_KEY>
```

> **Security Note**: Never commit `.env` to Git. The `.gitignore` file is configured to strictly exclude `.env`.

---

## 7. Database Setup & Migrations

### Create the Database
Ensure your PostgreSQL server is running, then create the database (e.g., via `psql` or pgAdmin):
```sql
CREATE DATABASE ai_task_manager;
```

### Apply Database Migrations
Run Alembic to apply schema migrations:
```bash
alembic upgrade head
```

To inspect the generated SQL offline without connecting to PostgreSQL:
```bash
alembic upgrade head --sql
```

### Seed the Database
Populate the database with default admin, standard user, and sample tasks:
```bash
python seed.py
```

**Default Seed Credentials:**
- **Administrator**: `admin@example.com` | Password: `admin123`
- **Standard User**: `user@example.com` | Password: `user123`

---

## 8. Running the Application

Start the development server with Uvicorn:
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

The application will be accessible at `http://127.0.0.1:8000`.

- **Health Check**: `GET http://127.0.0.1:8000/health`
- **Interactive Swagger Docs**: `http://127.0.0.1:8000/docs`
- **Alternative ReDoc UI**: `http://127.0.0.1:8000/redoc`

---

## 9. API Reference & Authentication

All protected endpoints require an HTTP `Authorization` header formatted as:
```http
Authorization: Bearer <your_access_token>
```

### 1. Authentication Endpoints (`/api/auth`)

| Method | Endpoint | Access | Description |
|---|---|---|---|
| `POST` | `/api/auth/register` | Public | Register new account (`name`, `email`, `password`) |
| `POST` | `/api/auth/login` | Public | OAuth2 Form login (`username`, `password`) returning JWT token |
| `GET` | `/api/auth/me` | Authenticated | Retrieve current user profile |

### 2. Task Management Endpoints (`/api/tasks`)

| Method | Endpoint | Access | Description |
|---|---|---|---|
| `POST` | `/api/tasks` | Authenticated | Create a new task (`title`, `description`) |
| `GET` | `/api/tasks` | Authenticated | List tasks (Users view their own; Admins view all) |
| `GET` | `/api/tasks/{task_id}` | Authenticated | Retrieve a specific task by ID (Owner or Admin) |
| `PATCH` | `/api/tasks/{task_id}` | Authenticated | Update task `title` and/or `description` (Owner or Admin) |
| `PATCH` | `/api/tasks/{task_id}/status` | **Admin Only** | Update task status (`Pending`, `In Progress`, `Testing`, `Completed`) |

### 3. AI Endpoint (`/api/tasks/generate-description`)

| Method | Endpoint | Access | Description |
|---|---|---|---|
| `POST` | `/api/tasks/generate-description` | Authenticated | Generate a professional task description using Gemini AI |

**Request Body:**
```json
{
  "title": "Build user notification subsystem"
}
```

**Response Body:**
```json
{
  "description": "Design and implement a real-time notification subsystem supporting email and push notifications, including queue-backed event processing and rate limiting."
}
```

---

## 10. Automated Testing

The automated test suite runs independently of a live PostgreSQL database and does not require an active Gemini API key. It uses in-memory SQLite (`StaticPool`) and mocks the Gemini client.

Run tests using Pytest:
```bash
python -m pytest tests/ -v
```

### Test Coverage Highlights:
- **`tests/test_auth.py`**:
  - Successful registration and duplicate email rejection (400)
  - Password minimum length and email format validation (422)
  - Successful login and invalid credentials handling (401)
  - Missing, invalid, or malformed JWT token access checks (401)
- **`tests/test_task.py`**:
  - Task creation with non-empty/non-whitespace title validation
  - Ownership restrictions: users can only view and update their own tasks (403 for unauthorized users)
  - Admin privileges: admin can list all tasks, view any task, edit any task, and update task status
  - Task status restriction: regular users cannot update task status (403)
  - Status validation: invalid statuses rejected (422)
  - Non-existent task handling (404)
- **`tests/test_ai.py`**:
  - Successful description generation with mocked Gemini responses
  - Unauthenticated access rejection (401)
  - Unconfigured or placeholder API key handling (503)
  - Title input validation (empty and whitespace-only rejected with 422)
  - Rate limit handling (429 `ResourceExhausted`)
  - Upstream timeout handling (504 `DeadlineExceeded`)
  - Upstream Google API errors (502 `GoogleAPIError`)
  - Empty response handling (502)

---

## 11. Postman Collection

A complete Postman collection is included in the project root:
- File: `ai_task_manager_postman.json`

### Using the Collection:
1. Open Postman and click **Import**.
2. Select `ai_task_manager_postman.json`.
3. Set the collection variable `base_url` to `http://localhost:8000`.
4. Execute `Authentication -> Login User`. The Postman test script automatically captures the `access_token` and populates the `token` collection variable for all protected requests.

---

## 12. Troubleshooting

1. **`passlib` / `bcrypt` compatibility error (`ValueError: password cannot be longer than 72 bytes`)**:
   - The project pins `bcrypt<4.0.0` in `requirements.txt` to maintain compatibility with `passlib`.
2. **`could not connect to server: Connection refused`**:
   - Verify that your PostgreSQL service is running and `DATABASE_URL` in `.env` points to the correct host, port, user, password, and database.
3. **`503 Service Unavailable: Gemini API key is not configured`**:
   - Ensure you have added a valid API key from [Google AI Studio](https://aistudio.google.com/) to `GEMINI_API_KEY` in `.env`.
4. **Elevating a User to Admin in PostgreSQL**:
   - Public registration assigns the `user` role by default. To make a user an administrator directly in the database:
     ```sql
     UPDATE users SET role = 'admin' WHERE email = 'user@example.com';
     ```

---

## 13. Known Limitations

- **Email Verification & Password Reset**: The current version implements core JWT authentication without an email verification or reset token workflow.
- **Asynchronous DB Drivers**: The current implementation uses synchronous SQLAlchemy sessions with psycopg2. High-throughput deployments can migrate to `asyncpg` and SQLAlchemy async sessions if required.
- **Task Deletion**: Tasks can be updated and transitioned across statuses; explicit hard delete endpoints are intentionally omitted to maintain audit logs.
