# Final Assignment Verification Checklist

## Stage 1: Project Setup
- [x] Use Python, FastAPI, PostgreSQL, SQLAlchemy, JWT, and Gemini AI.
- [x] Create a clean Python backend project structure.
- [x] Create app folders: `api`, `auth`, `models`, `schemas`, `services`, `ai`, and `database`.
- [x] Create `app/main.py` with FastAPI and `/health` endpoint.
- [x] Create `requirements.txt` with initial dependencies.
- [x] Create `.gitignore` to exclude `.env`, venvs, pycache, secrets, test db.
- [x] Create `.env.example` with placeholders only.
- [x] Create `README.md` with setup overview.

## Stage 2: Database Setup
- [x] Configure SQLAlchemy with PostgreSQL `DATABASE_URL`.
- [x] Create `app/database/session.py`.
- [x] Create `app/database/base.py`.
- [x] Create `User` model (`id`, `name`, `email`, `hashed_password`, `role`, `created_at`, `updated_at`).
- [x] Create `Task` model (`id`, `user_id`, `title`, `description`, `status`, `created_at`, `updated_at`).
- [x] Define task-to-user foreign key relationship.
- [x] Restrict user roles to `user` and `admin`, statuses to Enums.
- [x] Add Alembic, PostgreSQL driver (`psycopg2-binary`) to `requirements.txt`.
- [x] Initialize Alembic. *(Note: Actual DB migration against PostgreSQL must be done manually by user once credentials are valid).*

## Stage 3: Authentication
- [x] Create Pydantic schemas for auth.
- [x] Implement registration with validation.
- [x] Hash passwords securely (Passlib bcrypt).
- [x] Prevent duplicate email registrations.
- [x] Implement login with email and password.
- [x] Generate JWT token.
- [x] Implement reusable auth dependencies (`get_current_user`).
- [x] Return appropriate HTTP status codes.
- [x] Endpoints: `POST /api/auth/register`, `POST /api/auth/login`, `GET /api/auth/me`.
- [x] Public registration always creates a regular user.

## Stage 4: Task Management APIs & RBAC
- [x] Implement task schemas and service logic.
- [x] Endpoints: `POST /api/tasks`, `GET /api/tasks`, `GET /api/tasks/{task_id}`, `PATCH /api/tasks/{task_id}`, `PATCH /api/tasks/{task_id}/status`.
- [x] Allowed statuses verified via Enums.
- [x] Regular users cannot update status or access others' tasks.
- [x] Admins can view, edit, and update status of any task.
- [x] Use existing dependencies (`get_current_user`, `get_db`).
- [x] Add automated tests using SQLite mock db. Tests verified and passed.

## Stage 5: Gemini AI Integration
- [x] Implement `POST /api/tasks/generate-description`.
- [x] Generate useful task description using Gemini API.
- [x] Read `GEMINI_API_KEY` securely from environment variables.
- [x] AI logic separated in `app/ai/gemini.py`.
- [x] Input validation and error handling for 429, 503, 504.
- [x] No database record required for description generation.
- [x] Does not break existing endpoints.
- [x] Add automated tests mocking the Gemini API.

## Stage 6: Final Verification
- [x] Run full test suite (`python -m pytest tests/`): 39/39 passed.
- [x] Create Postman Collection JSON.
- [x] Postman saves JWT token.
- [x] Verify README.md contains instructions, python versions, etc.
- [x] Verify `.env.example` has no secrets.
- [x] Create this checklist.

### Remaining Manual Steps
1. Create a real PostgreSQL database instance.
2. Provide valid credentials in your `.env` file for `DATABASE_URL` and `GEMINI_API_KEY`.
3. Apply the initial database schema via: `alembic upgrade head` (migration `5bd10a5e9407_init.py` is included and verified).
4. Run `python seed.py` or manually update a registered user in PostgreSQL to be an `admin` via SQL update.
