from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from datetime import timedelta

from database import get_db
from services.auth_service import authenticate_admin, create_access_token, get_current_admin
from config import settings
import templates as T

router = APIRouter()


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, db: Session = Depends(get_db)):
    if get_current_admin(request, db):
        return RedirectResponse("/dashboard", 302)
    html = T.render(T.LOGIN_TMPL, CSS=T.CSS, error="")
    return HTMLResponse(html)


@router.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    admin = authenticate_admin(db, username, password)
    if not admin:
        html = T.render(T.LOGIN_TMPL, CSS=T.CSS, error="Invalid username or password")
        return HTMLResponse(html, status_code=401)
    token = create_access_token({"sub": admin.username},
                                timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    resp = RedirectResponse("/dashboard", 302)
    resp.set_cookie("access_token", token, httponly=True,
                    max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60, samesite="lax")
    return resp


@router.get("/logout")
async def logout():
    resp = RedirectResponse("/login", 302)
    resp.delete_cookie("access_token")
    return resp
