import calendar
from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from database import get_db
from services.auth_service import get_current_admin
from services.attendance_service import (
    get_for_date, bulk_mark, monthly_records,
    calendar_map, monthly_stats,
)
from services.employee_service import get_employees, get_employee
import templates as T

router = APIRouter(prefix="/attendance")


def _auth(request, db):
    admin = get_current_admin(request, db)
    if not admin:
        raise HTTPException(307, headers={"Location": "/login"})
    return admin


def _page(body, admin, active, title, breadcrumb, request):
    return HTMLResponse(T._layout(
        body, active=active, admin_username=admin.username,
        page_title=title, breadcrumb=breadcrumb,
        success=request.query_params.get("success", ""),
        error=request.query_params.get("error", ""),
    ))


# ── Mark attendance ───────────────────────────────────────────────────────────
@router.get("", response_class=HTMLResponse)
async def mark_page(request: Request,
                    selected_date: Optional[str] = None,
                    db: Session = Depends(get_db)):
    admin = _auth(request, db)
    today = date.today()
    att_date = date.fromisoformat(selected_date) if selected_date else today
    employees = get_employees(db)
    existing = get_for_date(db, att_date)
    records_map = {r.employee_id: r for r in existing}

    body = T.render(
        T.ATTENDANCE_MARK_TMPL,
        employees=employees,
        records_map=records_map,
        selected_date=att_date.isoformat(),
        selected_date_fmt=att_date.strftime("%A, %d %B %Y"),
        today=today.isoformat(),
        already_marked=len(existing),
    )
    return _page(body, admin, "attendance", "Mark Attendance",
                 '<a href="/dashboard">Home</a><span>Attendance</span>', request)


@router.post("/bulk-mark")
async def bulk_mark_route(request: Request, db: Session = Depends(get_db)):
    _auth(request, db)
    form = await request.form()
    att_date = date.fromisoformat(form.get("attendance_date"))
    employees = get_employees(db)
    records = []
    for emp in employees:
        status = form.get(f"status_{emp.id}")
        if status:
            records.append({
                "employee_id": emp.id,
                "status": status,
                "check_in":  form.get(f"check_in_{emp.id}") or None,
                "check_out": form.get(f"check_out_{emp.id}") or None,
            })
    bulk_mark(db, att_date, records)
    return RedirectResponse(
        f"/attendance?selected_date={att_date.isoformat()}&success=Attendance saved", 302)


# ── History ───────────────────────────────────────────────────────────────────
@router.get("/history", response_class=HTMLResponse)
async def history_page(
    request: Request,
    employee_id: Optional[int] = None,
    month: Optional[int] = None,
    year:  Optional[int] = None,
    db: Session = Depends(get_db),
):
    admin = _auth(request, db)
    today = date.today()
    month = month or today.month
    year  = year  or today.year

    employees = get_employees(db)
    selected_emp = None
    records      = []
    stats        = {}
    cal_data     = {}
    cal_grid     = []

    if employee_id:
        selected_emp = get_employee(db, employee_id)
        records      = monthly_records(db, employee_id, month, year)
        stats        = monthly_stats(db, employee_id, month, year)
        cal_data     = calendar_map(db, employee_id, month, year)
        cal_grid     = calendar.monthcalendar(year, month)

    body = T.render(
        T.ATTENDANCE_HISTORY_TMPL,
        employees=employees,
        selected_employee=selected_emp,
        employee_id=employee_id,
        records=records,
        stats=stats,
        cal_data=cal_data,
        calendar_grid=cal_grid,
        month=month, year=year,
        month_name=calendar.month_name[month],
    )
    return _page(body, admin, "attendance-history", "Attendance History",
                 '<a href="/dashboard">Home</a>'
                 '<a href="/attendance">Attendance</a><span>History</span>', request)
