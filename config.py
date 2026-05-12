import os
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


def _database_url() -> str:
    url = os.getenv(
        "DATABASE_URL",
        "sqlite:///./hrms.db",
    )
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    if "supabase" in url and "sslmode=" not in url:
        parts = urlsplit(url)
        query = dict(parse_qsl(parts.query, keep_blank_values=True))
        query["sslmode"] = "require"
        url = urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))
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
