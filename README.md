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
python -m uvicorn main:app --host 0.0.0.0 --port $PORT
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

Render path:

```text
Render Dashboard -> gainup-hrms -> Environment -> Add Environment Variable
```

Use your live app URL only for viewing the app:

```text
https://gainup-hrms.onrender.com
```

For GitHub auto-deploy, create a Render deploy hook and save it as a GitHub secret:

```text
Render Dashboard -> gainup-hrms -> Settings -> Deploy Hook -> Create/Copy hook URL
GitHub repository -> Settings -> Secrets and variables -> Actions -> New repository secret
Name: RENDER_DEPLOY_HOOK_URL
Value: the Render deploy hook URL, not https://gainup-hrms.onrender.com
```

## GitHub Pages

GitHub Pages only serves static HTML, CSS, and JavaScript. This Python app must run on a backend host such as Render, Railway, Fly.io, PythonAnywhere, or a VPS. You can still use GitHub Pages for a static frontend that calls the hosted backend API.
