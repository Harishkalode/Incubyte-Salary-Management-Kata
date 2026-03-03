"""CRUD operations for employees."""
from sqlalchemy.orm import Session
from sqlalchemy import func

from . import models, schemas
from .config import get_deduction_rate


def create_employee(db: Session, emp: schemas.EmployeeCreate) -> models.Employee:
    """Create a new employee."""
    db_emp = models.Employee(**emp.model_dump())
    db.add(db_emp)
    db.commit()
    db.refresh(db_emp)
    return db_emp


def list_employees(
    db: Session,
    skip: int = 0,
    limit: int = 10,
) -> list[models.Employee]:
    """List employees with pagination."""
    return db.query(models.Employee).offset(skip).limit(limit).all()


def get_employee(db: Session, employee_id: int) -> models.Employee | None:
    """Get an employee by ID."""
    return db.query(models.Employee).filter(models.Employee.id == employee_id).first()


def update_employee(
    db: Session,
    employee_id: int,
    emp: schemas.EmployeeCreate,
) -> models.Employee:
    """Update an employee (full replacement)."""
    db_emp = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if db_emp:
        for key, value in emp.model_dump().items():
            setattr(db_emp, key, value)
        db.commit()
        db.refresh(db_emp)
    return db_emp


def patch_employee(
    db: Session,
    employee_id: int,
    emp: schemas.EmployeeUpdate,
) -> models.Employee:
    """Update an employee (partial update)."""
    db_emp = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if db_emp:
        update_data = emp.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_emp, key, value)
        db.commit()
        db.refresh(db_emp)
    return db_emp


def delete_employee(db: Session, employee_id: int) -> None:
    """Delete an employee."""
    db_emp = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if db_emp:
        db.delete(db_emp)
        db.commit()


def calculate_salary(emp: models.Employee) -> schemas.SalaryDetail:
    """Calculate salary with deductions based on country."""
    gross = emp.salary
    tds_rate = get_deduction_rate(emp.country)
    tds_amount = gross * tds_rate
    
    deductions = {"tds": tds_amount}
    total_deductions = tds_amount
    net = gross - total_deductions
    
    return schemas.SalaryDetail(
        gross=gross,
        deductions=deductions,
        total_deductions=total_deductions,
        net=net,
    )


def get_country_metrics(db: Session, country: str) -> schemas.MetricResponse:
    """Get salary metrics for a country."""
    employees = db.query(models.Employee).filter(
        func.lower(models.Employee.country) == func.lower(country)
    ).all()
    
    if not employees:
        return schemas.MetricResponse(count=0)
    
    salaries = [e.salary for e in employees]
    return schemas.MetricResponse(
        min=min(salaries),
        max=max(salaries),
        avg=sum(salaries) / len(salaries),
        count=len(salaries),
    )


def get_job_metrics(db: Session, job_title: str) -> schemas.MetricResponse:
    """Get salary metrics for a job title."""
    employees = db.query(models.Employee).filter(
        func.lower(models.Employee.job_title) == func.lower(job_title)
    ).all()
    
    if not employees:
        return schemas.MetricResponse(count=0)
    
    salaries = [e.salary for e in employees]
    return schemas.MetricResponse(
        min=min(salaries),
        max=max(salaries),
        avg=sum(salaries) / len(salaries),
        count=len(salaries),
    )

