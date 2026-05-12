from datetime import date as date_type
from typing import Optional
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from database import get_db
from services.auth_service import get_current_admin
from services.employee_service import (
    get_employees, count_employees, get_employee,
    create_employee, update_employee, delete_employee,
)
from schemas import EmployeeCreate, EmployeeUpdate
import templates as T

router = APIRouter(prefix="/employees")


def _auth(request, db):
    admin = get_current_admin(request, db)
    if not admin:
        raise HTTPException(status_code=307, headers={"Location": "/login"})
    return admin


def _page(body, admin, active, title, breadcrumb, request):
    return HTMLResponse(T._layout(
        body, active=active, admin_username=admin.username,
        page_title=title, breadcrumb=breadcrumb,
        success=request.query_params.get("success", ""),
        error=request.query_params.get("error", ""),
    ))


# ── List ──────────────────────────────────────────────────────────────────────
@router.get("", response_class=HTMLResponse)
async def emp_list(request: Request, search: str = "", page: int = 1,
                   db: Session = Depends(get_db)):
    admin = _auth(request, db)
    per_page = 10
    skip = (page - 1) * per_page
    employees = get_employees(db, skip=skip, limit=per_page, search=search)
    total = count_employees(db)
    body = T.render(
        T.EMPLOYEE_LIST_TMPL,
        employees=employees, search=search, page=page,
        total=total, per_page=per_page,
        total_pages=(total + per_page - 1) // per_page,
    )
    return _page(body, admin, "employees", "Employees",
                 '<a href="/dashboard">Home</a><span>Employees</span>', request)


# ── Add form ──────────────────────────────────────────────────────────────────
@router.get("/add", response_class=HTMLResponse)
async def add_form(request: Request, db: Session = Depends(get_db)):
    admin = _auth(request, db)
    body = T.render(T.EMPLOYEE_FORM_TMPL, employee=None, fd=None, form_error="")
    return _page(body, admin, "employees", "Add Employee",
                 '<a href="/dashboard">Home</a><a href="/employees">Employees</a><span>Add</span>', request)


@router.post("/add")
async def add_employee(
    request: Request,
    employee_id: str       = Form(...),
    name:        str       = Form(...),
    email:       Optional[str]  = Form(None),
    role:        Optional[str]  = Form(None),
    department:  Optional[str]  = Form(None),
    gross_salary: float    = Form(...),
    phone:       Optional[str]  = Form(None),
    joining_date: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    admin = _auth(request, db)
    try:
        data = EmployeeCreate(
            employee_id=employee_id, name=name,
            email=email or None, role=role or None,
            department=department or None,
            gross_salary=gross_salary, phone=phone or None,
            joining_date=date_type.fromisoformat(joining_date) if joining_date else None,
        )
        create_employee(db, data)
        return RedirectResponse("/employees?success=Employee added successfully", 302)
    except HTTPException as e:
        body = T.render(T.EMPLOYEE_FORM_TMPL, employee=None,
                        fd=type("fd", (), {"employee_id": employee_id, "name": name,
                                           "email": email, "role": role,
                                           "department": department,
                                           "gross_salary": gross_salary})(),
                        form_error=e.detail)
        return HTMLResponse(T._layout(body, "employees", admin.username,
                                      "Add Employee", '<a href="/employees">Employees</a><span>Add</span>'))


# ── Edit form ─────────────────────────────────────────────────────────────────
@router.get("/{eid}/edit", response_class=HTMLResponse)
async def edit_form(request: Request, eid: int, db: Session = Depends(get_db)):
    admin = _auth(request, db)
    emp = get_employee(db, eid)
    body = T.render(T.EMPLOYEE_FORM_TMPL, employee=emp, fd=None, form_error="")
    return _page(body, admin, "employees", "Edit Employee",
                 '<a href="/dashboard">Home</a><a href="/employees">Employees</a><span>Edit</span>', request)


@router.post("/{eid}/edit")
async def edit_employee(
    request: Request, eid: int,
    name:         str            = Form(...),
    email:        Optional[str]  = Form(None),
    role:         Optional[str]  = Form(None),
    department:   Optional[str]  = Form(None),
    gross_salary: float          = Form(...),
    phone:        Optional[str]  = Form(None),
    joining_date: Optional[str]  = Form(None),
    db: Session = Depends(get_db),
):
    _auth(request, db)
    update_employee(db, eid, EmployeeUpdate(
        name=name, email=email or None, role=role or None,
        department=department or None, gross_salary=gross_salary,
        phone=phone or None,
        joining_date=date_type.fromisoformat(joining_date) if joining_date else None,
    ))
    return RedirectResponse("/employees?success=Employee updated successfully", 302)


# ── Delete ────────────────────────────────────────────────────────────────────
@router.post("/{eid}/delete")
async def del_employee(request: Request, eid: int, db: Session = Depends(get_db)):
    _auth(request, db)
    delete_employee(db, eid)
    return RedirectResponse("/employees?success=Employee removed", 302)
