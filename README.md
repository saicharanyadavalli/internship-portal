# Internship Portal

Backend: FastAPI (async) + SQLite. Frontend: Vanilla HTML/CSS/JS.

## Run locally

1) Create venv and install deps

```bash
cd backend
python -m venv .venv
. .venv/Scripts/activate  # Windows PowerShell: .venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
```

2) Start API

```bash
uvicorn main:app --reload --port 8000
```

3) Open frontend

Use a static server from `frontend/` or open `index.html` with Live Server (recommended) so CORS origins match `http://localhost:5500`.

## API base

- Base: `/api`
- Health: `GET /api/health`

## Auth

- Register: `POST /api/auth/register` { email, password, role: student|company }
- Login: `POST /api/auth/login` (form: username, password) → bearer token
- Me: `GET /api/auth/me` with Authorization: Bearer token

## Students

- Upsert profile: `POST /api/students/profile`
- Upload resume: `POST /api/students/resume` (multipart)
- Apply: `POST /api/students/applications`
- My applications: `GET /api/students/applications`

## Companies

- Upsert profile: `POST /api/companies/profile`
- Create internship: `POST /api/companies/internships`
- List internships: `GET /api/companies/internships`

## Deploy

Vercel config in `backend/vercel.json`. Frontend can be deployed to any static host.

## PostgreSQL

Set `DATABASE_URL` to a PostgreSQL async URL (uses asyncpg):

```bash
# Windows PowerShell example
$env:DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/internships"
uvicorn main:app --reload --port 8000
```

Ensure the database exists (create DB `internships`). Tables are auto-created on startup.

