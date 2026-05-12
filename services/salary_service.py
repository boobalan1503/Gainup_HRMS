import calendar
from datetime import date
from typing import Dict, List

from fastapi import HTTPException
from sqlalchemy import and_, func
from sqlalchemy.orm import Session, joinedload

import models
from services.attendance_service import monthly_stats
from services.employee_service import get_employee


def _working_days(month: int, year: int) -> int:
    total_days = calendar.monthrange(year, month)[1]
    return sum(
        1
        for day in range(1, total_days + 1)
        if date(year, month, day).weekday() < 5
    )


def _salary_parts(gross_salary: float) -> Dict[str, float]:
    basic_pay = gross_salary * 0.40
    hra = gross_salary * 0.20
    transport_allowance = min(1600.0, gross_salary * 0.05)
    medical_allowance = min(1250.0, gross_salary * 0.05)
    special_allowance = max(
        0.0,
        gross_salary - basic_pay - hra - transport_allowance - medical_allowance,
    )
    pf_deduction = basic_pay * 0.12
    esi_deduction = gross_salary * 0.0075 if gross_salary <= 21000 else 0.0
    return {
        "basic_pay": basic_pay,
        "hra": hra,
        "transport_allowance": transport_allowance,
        "medical_allowance": medical_allowance,
        "special_allowance": special_allowance,
        "pf_deduction": pf_deduction,
        "esi_deduction": esi_deduction,
    }


def get_month_records(db: Session, month: int, year: int) -> List[models.SalaryRecord]:
    return (
        db.query(models.SalaryRecord)
        .options(joinedload(models.SalaryRecord.employee))
        .filter(
            and_(
                models.SalaryRecord.month == month,
                models.SalaryRecord.year == year,
            )
        )
        .order_by(models.SalaryRecord.id.desc())
        .all()
    )


def get_record(db: Session, salary_id: int) -> models.SalaryRecord:
    record = (
        db.query(models.SalaryRecord)
        .options(joinedload(models.SalaryRecord.employee))
        .filter(models.SalaryRecord.id == salary_id)
        .first()
    )
    if not record:
        raise HTTPException(status_code=404, detail="Salary record not found")
    return record


def generate(
    db: Session,
    employee_id: int,
    month: int,
    year: int,
    other_deductions: float = 0.0,
) -> models.SalaryRecord:
    existing = (
        db.query(models.SalaryRecord)
        .filter(
            and_(
                models.SalaryRecord.employee_id == employee_id,
                models.SalaryRecord.month == month,
                models.SalaryRecord.year == year,
            )
        )
        .first()
    )
    if existing:
        return existing

    employee = get_employee(db, employee_id)
    stats = monthly_stats(db, employee_id, month, year)
    working_days = stats.get("working_days") or _working_days(month, year)
    days_present = min(float(stats.get("effective_present", 0.0)), float(working_days))
    days_absent = max(0.0, float(working_days) - days_present)

    gross_salary = float(employee.gross_salary)
    parts = _salary_parts(gross_salary)
    per_day = gross_salary / working_days if working_days else 0.0
    lop_deduction = round(per_day * days_absent, 2)
    total_deductions = (
        parts["pf_deduction"]
        + parts["esi_deduction"]
        + other_deductions
        + lop_deduction
    )
    net_salary = max(0.0, gross_salary - total_deductions)

    record = models.SalaryRecord(
        employee_id=employee.id,
        month=month,
        year=year,
        gross_salary=gross_salary,
        total_working_days=working_days,
        days_present=days_present,
        days_absent=days_absent,
        half_days=int(stats.get("half_days", 0)),
        other_deductions=other_deductions,
        lop_deduction=lop_deduction,
        net_salary=round(net_salary, 2),
        **parts,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def slip_data(db: Session, salary_id: int) -> Dict:
    record = get_record(db, salary_id)
    total_earnings = (
        record.basic_pay
        + record.hra
        + record.transport_allowance
        + record.medical_allowance
        + record.special_allowance
    )
    total_deductions = (
        record.pf_deduction
        + record.esi_deduction
        + record.other_deductions
        + record.lop_deduction
    )
    return {
        "record": record,
        "employee": record.employee,
        "month_name": calendar.month_name[record.month],
        "total_earnings": total_earnings,
        "total_deductions": total_deductions,
    }


def mark_paid(db: Session, salary_id: int) -> models.SalaryRecord:
    record = get_record(db, salary_id)
    record.is_paid = True
    record.paid_date = date.today()
    db.commit()
    db.refresh(record)
    return record


def month_total(db: Session, month: int, year: int) -> float:
    total = (
        db.query(func.sum(models.SalaryRecord.net_salary))
        .filter(
            and_(
                models.SalaryRecord.month == month,
                models.SalaryRecord.year == year,
            )
        )
        .scalar()
    )
    return total or 0.0
