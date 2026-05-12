import os


def _database_url() -> str:
    url = os.getenv(
        "DATABASE_URL",
        "postgresql://hrms_user:hrms_pass@localhost:5432/hrms_db",
    )
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql://", 1)
    return url

class Settings:
    APP_NAME: str = "AttendPro HRMS"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "hrms-super-secret-key-2024-change-in-prod")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480  # 8 hours

    DATABASE_URL: str = _database_url()

    ADMIN_USERNAME: str = os.getenv("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "admin123")
    ADMIN_EMAIL: str = os.getenv("ADMIN_EMAIL", "admin@company.com")

settings = Settings()
