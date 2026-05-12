from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from database import Base, engine
import models  # noqa: F401 - registers all ORM models
from routes import attendance, auth, dashboard, employees, salary


logger = logging.getLogger("gainup_hrms")


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.database_ready = False
    try:
        Base.metadata.create_all(bind=engine)
        from database import SessionLocal
        from services.seed_service import seed

        db = SessionLocal()
        try:
            seed(db)
            app.state.database_ready = True
            logger.info("Database initialization completed.")
        finally:
            db.close()
    except Exception:
        logger.exception(
            "Database initialization failed. Check DATABASE_URL, Supabase password, host, and sslmode=require."
        )
    yield


app = FastAPI(
    title="AttendPro HRMS",
    description="Employee Attendance & Salary Management System",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(employees.router)
app.include_router(attendance.router)
app.include_router(salary.router)


@app.get("/")
async def root():
    return RedirectResponse(url="/login")


@app.get("/healthz")
async def healthz():
    return {
        "status": "ok",
        "database_ready": getattr(app.state, "database_ready", False),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
