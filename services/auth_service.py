from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import Request
import models
from config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode["exp"] = expire
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        return None


def authenticate_admin(db: Session, username: str, password: str) -> Optional[models.Admin]:
    admin = db.query(models.Admin).filter(models.Admin.username == username).first()
    if not admin or not verify_password(password, admin.hashed_password):
        return None
    return admin


def list_admins(db: Session):
    return db.query(models.Admin).order_by(models.Admin.created_at.desc()).all()


def create_admin(db: Session, username: str, email: str, password: str) -> models.Admin:
    username = username.strip()
    email = email.strip().lower()
    if db.query(models.Admin).filter(models.Admin.username == username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    if db.query(models.Admin).filter(models.Admin.email == email).first():
        raise HTTPException(status_code=400, detail="Email already exists")
    admin = models.Admin(
        username=username,
        email=email,
        hashed_password=hash_password(password),
        is_active=True,
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin


def get_current_admin(request: Request, db: Session) -> Optional[models.Admin]:
    token = request.cookies.get("access_token")
    if not token:
        return None
    payload = decode_token(token)
    if not payload:
        return None
    username = payload.get("sub")
    if not username:
        return None
    return db.query(models.Admin).filter(models.Admin.username == username).first()
