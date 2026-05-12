from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from fastapi import HTTPException
import models
from schemas import EmployeeCreate, EmployeeUpdate


def get_employees(db: Session, skip: int = 0, limit: int = 100, search: str = "") -> List[models.Employee]:
    q = db.query(models.Employee).filter(models.Employee.is_active == True)
    if search:
        q = q.filter(
            models.Employee.name.ilike(f"%{search}%") |
            models.Employee.employee_id.ilike(f"%{search}%") |
            models.Employee.role.ilike(f"%{search}%") |
            models.Employee.department.ilike(f"%{search}%")
        )
    return q.order_by(models.Employee.name).offset(skip).limit(limit).all()


def count_employees(db: Session) -> int:
    return db.query(func.count(models.Employee.id)).filter(models.Employee.is_active == True).scalar()


def get_employee(db: Session, eid: int) -> models.Employee:
    emp = db.query(models.Employee).filter(models.Employee.id == eid).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp


def create_employee(db: Session, data: EmployeeCreate) -> models.Employee:
    if db.query(models.Employee).filter(models.Employee.employee_id == data.employee_id).first():
        raise HTTPException(status_code=400, detail=f"Employee ID '{data.employee_id}' already exists")
    if data.email and db.query(models.Employee).filter(models.Employee.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email already in use")
    emp = models.Employee(**data.model_dump())
    db.add(emp); db.commit(); db.refresh(emp)
    return emp


def update_employee(db: Session, eid: int, data: EmployeeUpdate) -> models.Employee:
    emp = get_employee(db, eid)
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(emp, k, v)
    db.commit(); db.refresh(emp)
    return emp


def delete_employee(db: Session, eid: int) -> None:
    emp = get_employee(db, eid)
    emp.is_active = False
    db.commit()


def total_payroll(db: Session) -> float:
    r = db.query(func.sum(models.Employee.gross_salary)).filter(models.Employee.is_active == True).scalar()
    return r or 0.0
