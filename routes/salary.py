import calendar
from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from database import get_db
from services.auth_service import get_current_admin
from services.salary_service import (
    generate, get_month_records, slip_data, mark_paid, month_total,
)
from services.employee_service import get_employees
import templates as T

router = APIRouter(prefix="/salary")


def _auth(request, db):
    admin = get_current_admin(request, db)
    if not admin:
        raise HTTPException(307, headers={"Location": "/login"})
    return admin


def _page(body, admin, title, breadcrumb, request):
    return HTMLResponse(T._layout(
        body, active="salary", admin_username=admin.username,
        page_title=title, breadcrumb=breadcrumb,
        success=request.query_params.get("success", ""),
        error=request.query_params.get("error", ""),
    ))


@router.get("", response_class=HTMLResponse)
async def salary_list(
    request: Request,
    month: Optional[int] = None,
    year:  Optional[int] = None,
    db: Session = Depends(get_db),
):
    admin = _auth(request, db)
    today = date.today()
    month = month or today.month
    year  = year  or today.year

    records    = get_month_records(db, month, year)
    employees  = get_employees(db)
    existing_ids = {r.employee_id for r in records}
    unprocessed  = [e for e in employees if e.id not in existing_ids]
    total_net    = sum(r.net_salary for r in records)
    total_gross  = sum(r.gross_salary for r in records)
    paid_count   = sum(1 for r in records if r.is_paid)

    body = T.render(
        T.SALARY_LIST_TMPL,
        records=records, unprocessed=unprocessed,
        month=month, year=year,
        month_name=calendar.month_name[month],
        total_net=total_net, total_gross=total_gross,
        paid_count=paid_count,
    )
    return _page(body, admin, "Salary Management",
                 '<a href="/dashboard">Home</a><span>Salary</span>', request)


@router.post("/generate")
async def gen_salary(
    request: Request,
    employee_id:      int   = Form(...),
    month:            int   = Form(...),
    year:             int   = Form(...),
    other_deductions: float = Form(0),
    db: Session = Depends(get_db),
):
    _auth(request, db)
    generate(db, employee_id, month, year, other_deductions)
    return RedirectResponse(f"/salary?month={month}&year={year}&success=Salary generated", 302)


@router.post("/generate-all")
async def gen_all(
    request: Request,
    month: int = Form(...),
    year:  int = Form(...),
    db: Session = Depends(get_db),
):
    _auth(request, db)
    for emp in get_employees(db):
        generate(db, emp.id, month, year)
    return RedirectResponse(
        f"/salary?month={month}&year={year}&success=All salaries generated", 302)


@router.get("/slip/{salary_id}", response_class=HTMLResponse)
async def salary_slip(request: Request, salary_id: int,
                      db: Session = Depends(get_db)):
    admin = _auth(request, db)
    data = slip_data(db, salary_id)
    body = T.render(T.SALARY_SLIP_TMPL, **data)
    return _page(body, admin, "Salary Slip",
                 f'<a href="/dashboard">Home</a>'
                 f'<a href="/salary">Salary</a><span>Slip</span>', request)


@router.post("/mark-paid/{salary_id}")
async def pay_salary(
    request: Request, salary_id: int,
    month: int = Form(...), year: int = Form(...),
    db: Session = Depends(get_db),
):
    _auth(request, db)
    mark_paid(db, salary_id)
    return RedirectResponse(
        f"/salary?month={month}&year={year}&success=Marked as paid", 302)
