# Gainup HRMS

FastAPI HRMS application for employee management, attendance, and salary processing.

## Run locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Open `http://localhost:8000`.

## Database

Use Supabase Postgres by setting `DATABASE_URL`.

Example:

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@YOUR_SUPABASE_HOST:5432/postgres?sslmode=require
```

The app creates required tables on startup and seeds the first admin account from:

```env
ADMIN_USERNAME=admin
ADMIN_PASSWORD=change-this-password
ADMIN_EMAIL=admin@company.com
```

## Render

Render should use:

```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port $PORT
```

Health check path:

```text
/healthz
```

Set these Render environment variables:

```text
DATABASE_URL
SECRET_KEY
ADMIN_USERNAME
ADMIN_PASSWORD
ADMIN_EMAIL
```

## GitHub Pages

GitHub Pages only serves static HTML, CSS, and JavaScript. This Python app must run on a backend host such as Render, Railway, Fly.io, PythonAnywhere, or a VPS. You can still use GitHub Pages for a static frontend that calls the hosted backend API.
