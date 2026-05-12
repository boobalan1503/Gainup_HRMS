import random
from datetime import date, timedelta
from sqlalchemy.orm import Session
import models
from services.auth_service import hash_password
from config import settings


def seed(db: Session) -> None:
    if db.query(models.Admin).first():
        return  # already seeded

    # Admin
    db.add(models.Admin(
        username=settings.ADMIN_USERNAME,
        email=settings.ADMIN_EMAIL,
        hashed_password=hash_password(settings.ADMIN_PASSWORD),
    ))
    db.commit()

    # Sample employees
    employees_data = [
        ("EMP001", "Arjun Sharma",   "arjun@company.com",   "Senior Developer",  "Engineering",      85000, "9876543210", date(2022, 3, 15)),
        ("EMP002", "Priya Nair",     "priya@company.com",   "UI/UX Designer",    "Design",           72000, "9876543211", date(2022, 6,  1)),
        ("EMP003", "Rahul Verma",    "rahul@company.com",   "Product Manager",   "Product",          95000, "9876543212", date(2021,11, 20)),
        ("EMP004", "Sneha Reddy",    "sneha@company.com",   "QA Engineer",       "Engineering",      68000, "9876543213", date(2023, 1, 10)),
        ("EMP005", "Karan Mehta",    "karan@company.com",   "DevOps Engineer",   "Infrastructure",   90000, "9876543214", date(2022, 8,  5)),
        ("EMP006", "Ananya Iyer",    "ananya@company.com",  "HR Manager",        "Human Resources",  78000, "9876543215", date(2021, 5, 12)),
        ("EMP007", "Vikram Singh",   "vikram@company.com",  "Backend Developer", "Engineering",      80000, "9876543216", date(2023, 4, 18)),
        ("EMP008", "Deepa Krishnan", "deepa@company.com",   "Data Analyst",      "Analytics",        75000, "9876543217", date(2022,12,  1)),
    ]

    employees = []
    for eid, name, email, role, dept, sal, ph, jdate in employees_data:
        e = models.Employee(employee_id=eid, name=name, email=email, role=role,
                            department=dept, gross_salary=sal, phone=ph, joining_date=jdate)
        db.add(e); employees.append(e)
    db.commit()
    for e in employees:
        db.refresh(e)

    # Attendance for last 30 weekdays
    pool = [
        models.AttendanceStatus.PRESENT,
        models.AttendanceStatus.PRESENT,
        models.AttendanceStatus.PRESENT,
        models.AttendanceStatus.PRESENT,
        models.AttendanceStatus.ABSENT,
        models.AttendanceStatus.HALF_DAY_FIRST,
    ]
    today = date.today()
    for emp in employees:
        for i in range(30):
            d = today - timedelta(days=i)
            if d.weekday() >= 5:
                continue
            status = random.choice(pool)
            check_in  = "09:15" if status != models.AttendanceStatus.ABSENT else None
            check_out = ("18:30" if status == models.AttendanceStatus.PRESENT
                         else ("13:00" if status == models.AttendanceStatus.HALF_DAY_FIRST else None))
            db.add(models.Attendance(employee_id=emp.id, date=d,
                                     status=status, check_in=check_in, check_out=check_out))
    db.commit()
    print("✅  Seed data inserted.")
