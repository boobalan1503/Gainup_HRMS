import calendar
from datetime import date, timedelta
from typing import List, Dict, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, and_
import models
from schemas import AttendanceCreate


def get_for_date(db: Session, d: date) -> List[models.Attendance]:
    return (db.query(models.Attendance)
              .options(joinedload(models.Attendance.employee))
              .filter(models.Attendance.date == d).all())


def mark(db: Session, data: AttendanceCreate) -> models.Attendance:
    existing = db.query(models.Attendance).filter(
        and_(models.Attendance.employee_id == data.employee_id,
             models.Attendance.date == data.date)
    ).first()
    if existing:
        for k, v in data.model_dump(exclude_unset=True).items():
            setattr(existing, k, v)
        db.commit(); db.refresh(existing)
        return existing
    rec = models.Attendance(**data.model_dump())
    db.add(rec); db.commit(); db.refresh(rec)
    return rec


def bulk_mark(db: Session, d: date, records: list) -> None:
    for r in records:
        mark(db, AttendanceCreate(
            employee_id=r["employee_id"], date=d,
            status=r["status"],
            check_in=r.get("check_in"), check_out=r.get("check_out"),
        ))


def today_summary(db: Session, d: date) -> Dict:
    recs = get_for_date(db, d)
    total = db.query(func.count(models.Employee.id)).filter(models.Employee.is_active == True).scalar()
    present  = sum(1 for r in recs if r.status == models.AttendanceStatus.PRESENT)
    absent   = sum(1 for r in recs if r.status == models.AttendanceStatus.ABSENT)
    half     = sum(1 for r in recs if r.status in (
        models.AttendanceStatus.HALF_DAY_FIRST, models.AttendanceStatus.HALF_DAY_SECOND))
    not_marked = total - len(recs)
    rate = round((present + half * 0.5) / total * 100, 1) if total else 0
    return {"total": total, "present": present,
            "absent": absent + not_marked, "half_day": half, "rate": rate}


def monthly_records(db: Session, employee_id: int, month: int, year: int) -> List[models.Attendance]:
    start = date(year, month, 1)
    end   = date(year, month, calendar.monthrange(year, month)[1])
    return (db.query(models.Attendance)
              .filter(and_(models.Attendance.employee_id == employee_id,
                           models.Attendance.date >= start,
                           models.Attendance.date <= end))
              .order_by(models.Attendance.date).all())


def monthly_stats(db: Session, employee_id: int, month: int, year: int) -> Dict:
    recs = monthly_records(db, employee_id, month, year)
    total_days   = calendar.monthrange(year, month)[1]
    present      = sum(1 for r in recs if r.status == models.AttendanceStatus.PRESENT)
    absent       = sum(1 for r in recs if r.status == models.AttendanceStatus.ABSENT)
    half_days    = sum(1 for r in recs if r.status in (
        models.AttendanceStatus.HALF_DAY_FIRST, models.AttendanceStatus.HALF_DAY_SECOND))
    leaves       = sum(1 for r in recs if r.status == models.AttendanceStatus.LEAVE)
    holidays     = sum(1 for r in recs if r.status == models.AttendanceStatus.HOLIDAY)
    working_days = total_days - holidays
    eff_present  = present + half_days * 0.5
    lop          = max(0, working_days - eff_present - leaves)
    return dict(total_days=total_days, working_days=working_days,
                present=present, absent=absent, half_days=half_days,
                leaves=leaves, holidays=holidays,
                effective_present=eff_present, lop_days=lop)


def calendar_map(db: Session, employee_id: int, month: int, year: int) -> Dict:
    recs = monthly_records(db, employee_id, month, year)
    return {
        str(r.date): {
            "status": r.status.value if hasattr(r.status, "value") else r.status,
            "check_in": r.check_in, "check_out": r.check_out,
        }
        for r in recs
    }


def attendance_trend(db: Session, today: date, days: int = 7) -> List[Dict]:
    result = []
    for i in range(days - 1, -1, -1):
        d = today - timedelta(days=i)
        if d.weekday() >= 5:
            continue
        s = today_summary(db, d)
        result.append({"date": d.strftime("%d %b"),
                        "present": s["present"], "absent": s["absent"]})
    return result
