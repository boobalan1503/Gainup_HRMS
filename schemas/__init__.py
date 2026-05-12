import enum
from sqlalchemy import (
    Column, Integer, String, Float, Date, DateTime,
    Enum, Boolean, ForeignKey, Text
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class AttendanceStatus(str, enum.Enum):
    PRESENT          = "Present"
    ABSENT           = "Absent"
    HALF_DAY_FIRST   = "Half Day (First Half)"
    HALF_DAY_SECOND  = "Half Day (Second Half)"
    LEAVE            = "Leave"
    HOLIDAY          = "Holiday"


# ─── Admin ────────────────────────────────────────────────────────────────────
class Admin(Base):
    __tablename__ = "admins"

    id              = Column(Integer, primary_key=True, index=True)
    username        = Column(String(50),  unique=True, nullable=False, index=True)
    email           = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active       = Column(Boolean, default=True)
    created_at      = Column(DateTime(timezone=True), server_default=func.now())


# ─── Employee ─────────────────────────────────────────────────────────────────
class Employee(Base):
    __tablename__ = "employees"

    id            = Column(Integer, primary_key=True, index=True)
    employee_id   = Column(String(20),  unique=True, nullable=False, index=True)
    name          = Column(String(100), nullable=False)
    email         = Column(String(100), unique=True, nullable=True)
    role          = Column(String(100), nullable=True)
    department    = Column(String(100), nullable=True)
    gross_salary  = Column(Float,       nullable=False)
    phone         = Column(String(20),  nullable=True)
    joining_date  = Column(Date,        nullable=True)
    is_active     = Column(Boolean, default=True)
    created_at    = Column(DateTime(timezone=True), server_default=func.now())
    updated_at    = Column(DateTime(timezone=True), onupdate=func.now())

    attendances    = relationship("Attendance",    back_populates="employee", cascade="all, delete-orphan")
    salary_records = relationship("SalaryRecord",  back_populates="employee", cascade="all, delete-orphan")


# ─── Attendance ───────────────────────────────────────────────────────────────
class Attendance(Base):
    __tablename__ = "attendances"

    id          = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    date        = Column(Date, nullable=False)
    status      = Column(Enum(AttendanceStatus), nullable=False, default=AttendanceStatus.ABSENT)
    check_in    = Column(String(10), nullable=True)
    check_out   = Column(String(10), nullable=True)
    notes       = Column(Text, nullable=True)
    created_at  = Column(DateTime(timezone=True), server_default=func.now())
    updated_at  = Column(DateTime(timezone=True), onupdate=func.now())

    employee = relationship("Employee", back_populates="attendances")


# ─── SalaryRecord ─────────────────────────────────────────────────────────────
class SalaryRecord(Base):
    __tablename__ = "salary_records"

    id          = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    month       = Column(Integer, nullable=False)
    year        = Column(Integer, nullable=False)

    # Earnings
    gross_salary         = Column(Float, nullable=False)
    basic_pay            = Column(Float, nullable=False)
    hra                  = Column(Float, nullable=False)
    transport_allowance  = Column(Float, default=0)
    medical_allowance    = Column(Float, default=0)
    special_allowance    = Column(Float, default=0)

    # Deductions
    pf_deduction         = Column(Float, default=0)
    esi_deduction        = Column(Float, default=0)
    other_deductions     = Column(Float, default=0)
    lop_deduction        = Column(Float, default=0)

    # Attendance snapshot
    total_working_days   = Column(Integer, nullable=False)
    days_present         = Column(Float,   nullable=False)
    days_absent          = Column(Float,   default=0)
    half_days            = Column(Integer, default=0)

    net_salary           = Column(Float,   nullable=False)
    is_paid              = Column(Boolean, default=False)
    paid_date            = Column(Date,    nullable=True)
    notes                = Column(Text,    nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    employee = relationship("Employee", back_populates="salary_records")
