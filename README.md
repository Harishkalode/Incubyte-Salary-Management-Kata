# Salary Management Kata

Minimal FastAPI application demonstrating TDD with SQLAlchemy and SQLite.

Getting started

- Python: 3.11+ (this workspace uses a virtualenv)
- Install deps:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

- Run the app:

```bash
uvicorn app.main:app --reload
```

Run tests

```bash
source .venv/bin/activate
python -m pytest -q
```

Database Migrations

This project uses Alembic for database schema migrations.

To apply all pending migrations (create tables):

```bash
source .venv/bin/activate
alembic upgrade head
```

To create a new migration after changing models:

```bash
source .venv/bin/activate
alembic revision --autogenerate -m "describe your changes"
```

API

- POST /employees
  - Request JSON: {"name": "Alice", "salary": 5000}
  - Response 201 JSON: {"id": 1, "name": "Alice", "salary": 5000}

- GET /employees
  - Response 200 JSON: [{"id":1, "name":"Alice", "salary":5000}, ...]

JSON schemas

- EmployeeCreate
  - name: string
  - salary: integer

- Employee
  - id: integer
  - name: string
  - salary: integer

Implementation Details

- TDD approach: I created failing tests first (`tests/test_employees.py`), then implemented the minimal code to make them pass (models, DB setup, CRUD, and endpoints), then ran tests until green.
- Tools used: I created files using automated edits and executed tests in the dev container to verify behavior.
- Files added/modified by this change:
  - `app/main.py` (API + DB wiring)
  - `app/db.py` (SQLAlchemy setup)
  - `app/models.py` (Employee model)
  - `app/schemas.py` (Pydantic schemas)
  - `app/crud.py` (CRUD helpers)
  - `tests/test_employees.py` (TDD tests)
  - `pytest.ini`, `requirements.txt`

How I was used

- Prompts and automated steps: I followed the user's instruction to use TDD and created the failing tests first, then iteratively implemented code and re-ran tests until they passed. All file edits were done programmatically in small focused patches.
- Manual edits: none beyond the programmatic patches and running test/install commands in the dev environment.

Git commit plan (suggested)

- feat(tdd): add failing tests for employee endpoints (TDD red)
- feat(api): implement Employee model, CRUD and endpoints (TDD green)
- fix(db): ensure DB tables created at import/startup
- docs: add README and usage instructions
# Incubyte-Salary-Management-Kata