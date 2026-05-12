from fastapi import APIRouter, Depends, Form, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from database import get_db
from services.auth_service import create_admin, get_current_admin, list_admins
import templates as T


router = APIRouter(prefix="/admin")


def _auth(request: Request, db: Session):
    admin = get_current_admin(request, db)
    if not admin:
        raise HTTPException(status_code=307, headers={"Location": "/login"})
    return admin


def _page(body: str, admin, request: Request):
    return HTMLResponse(T._layout(
        body,
        active="admin-users",
        admin_username=admin.username,
        page_title="Admin Users",
        breadcrumb='<a href="/dashboard">Home</a><span>Admin Users</span>',
        success=request.query_params.get("success", ""),
        error=request.query_params.get("error", ""),
    ))


@router.get("/users", response_class=HTMLResponse)
async def users_page(request: Request, db: Session = Depends(get_db)):
    admin = _auth(request, db)
    body = T.render(
        T.ADMIN_USERS_TMPL,
        admins=list_admins(db),
        form_error="",
        fd=None,
        current_admin_id=admin.id,
    )
    return _page(body, admin, request)


@router.post("/users")
async def create_user(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    admin = _auth(request, db)
    try:
        create_admin(db, username=username, email=email, password=password)
    except HTTPException as exc:
        body = T.render(
            T.ADMIN_USERS_TMPL,
            admins=list_admins(db),
            form_error=exc.detail,
            fd=type("fd", (), {"username": username, "email": email})(),
            current_admin_id=admin.id,
        )
        return _page(body, admin, request)
    return RedirectResponse("/admin/users?success=User created successfully", 302)
