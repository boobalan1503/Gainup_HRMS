from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from models import AttendanceStatus


class EmployeeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    department: Optional[str] = None
    gross_salary: float = Field(..., ge=0)
    phone: Optional[str] = None
    joining_date: Optional[date] = None


class EmployeeCreate(EmployeeBase):
    employee_id: str = Field(..., min_length=1, max_length=20)


class EmployeeUpdate(EmployeeBase):
    pass


class AttendanceCreate(BaseModel):
    employee_id: int
    date: date
    status: AttendanceStatus
    check_in: Optional[str] = None
    check_out: Optional[str] = None
    notes: Optional[str] = None
