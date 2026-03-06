"""CRUD operations for Employee model."""
from sqlalchemy.orm import Session

from . import models, schemas


def create_employee(db: Session, emp: schemas.EmployeeCreate) -> models.Employee:
    """Create a new employee."""
    db_emp = models.Employee(
        full_name=emp.full_name,
        job_title=emp.job_title,
        country=emp.country,
        salary=emp.salary,
    )
    db.add(db_emp)
    db.commit()
    db.refresh(db_emp)
    return db_emp


def get_employee(db: Session, employee_id: int) -> models.Employee | None:
    """Get an employee by ID."""
    return db.query(models.Employee).filter(models.Employee.id == employee_id).first()


def list_employees(db: Session, skip: int = 0, limit: int = 10) -> list[models.Employee]:
    """List employees with pagination."""
    return db.query(models.Employee).offset(skip).limit(limit).all()


def update_employee(
    db: Session, employee_id: int, emp: schemas.EmployeeCreate
) -> models.Employee:
    """Update an entire employee (PUT)."""
    db_emp = get_employee(db, employee_id)
    if not db_emp:
        return None
    db_emp.full_name = emp.full_name
    db_emp.job_title = emp.job_title
    db_emp.country = emp.country
    db_emp.salary = emp.salary
    db.commit()
    db.refresh(db_emp)
    return db_emp


def patch_employee(
    db: Session, employee_id: int, emp: schemas.EmployeeUpdate
) -> models.Employee:
    """Update an employee partially (PATCH)."""
    db_emp = get_employee(db, employee_id)
    if not db_emp:
        return None
    # Only update non-None fields
    if emp.full_name is not None:
        db_emp.full_name = emp.full_name
    if emp.job_title is not None:
        db_emp.job_title = emp.job_title
    if emp.country is not None:
        db_emp.country = emp.country
    if emp.salary is not None:
        db_emp.salary = emp.salary
    db.commit()
    db.refresh(db_emp)
    return db_emp


def delete_employee(db: Session, employee_id: int) -> bool:
    """Delete an employee."""
    db_emp = get_employee(db, employee_id)
    if not db_emp:
        return False
    db.delete(db_emp)
    db.commit()
    return True


def get_country_metrics(db: Session, country: str) -> dict:
    """Get salary metrics for a country."""
    employees = (
        db.query(models.Employee)
        .filter(models.Employee.country.ilike(country))
        .all()
    )
    if not employees:
        return {"count": 0, "min": None, "max": None, "avg": None}
    
    salaries = [e.salary for e in employees]
    return {
        "count": len(salaries),
        "min": min(salaries),
        "max": max(salaries),
        "avg": sum(salaries) / len(salaries),
    }


def get_job_metrics(db: Session, job_title: str) -> dict:
    """Get salary metrics for a job title."""
    employees = (
        db.query(models.Employee)
        .filter(models.Employee.job_title.ilike(job_title))
        .all()
    )
    if not employees:
        return {"count": 0, "min": None, "max": None, "avg": None}
    
    salaries = [e.salary for e in employees]
    return {
        "count": len(salaries),
        "min": min(salaries),
        "max": max(salaries),
        "avg": sum(salaries) / len(salaries),
    }


def calculate_salary(employee: models.Employee) -> schemas.SalaryDetail:
    """Calculate salary with deductions based on country."""
    from .config import get_deduction_rate
    
    gross = employee.salary
    deduction_rate = get_deduction_rate(employee.country)
    
    deductions = {}
    if deduction_rate > 0:
        tds = gross * deduction_rate
        deductions["tds"] = tds
    
    total_deductions = sum(deductions.values())
    net = gross - total_deductions
    
    return schemas.SalaryDetail(
        gross=gross,
        deductions=deductions,
        total_deductions=total_deductions,
        net=net,
    )

