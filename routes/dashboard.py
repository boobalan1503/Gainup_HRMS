import json
import calendar
from datetime import date
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from database import get_db
from services.auth_service import get_current_admin
from services.employee_service import count_employees, total_payroll
from services.attendance_service import today_summary, attendance_trend
from services.salary_service import month_total
import templates as T

router = APIRouter()


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    admin = get_current_admin(request, db)
    if not admin:
        return RedirectResponse("/login", 302)

    today = date.today()
    month, year = today.month, today.year

    body = T.render(
        T.DASHBOARD_TMPL,
        total_employees=count_employees(db),
        today_summary=today_summary(db, today),
        total_payroll=total_payroll(db),
        monthly_processed=month_total(db, month, year),
        today_str=today.strftime("%d %B, %Y"),
        month_name=calendar.month_name[month],
        year=year,
        trend_json=json.dumps(attendance_trend(db, today)),
    )
    return HTMLResponse(T._layout(
        body, active="dashboard", admin_username=admin.username,
        page_title="Dashboard",
        breadcrumb='<a href="/dashboard">Home</a>',
        success=request.query_params.get("success", ""),
        error=request.query_params.get("error", ""),
    ))
