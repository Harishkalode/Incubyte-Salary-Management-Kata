"""Employee CRUD endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..db import get_db
from .. import models, schemas
from .. import crud as crud_module

router = APIRouter(prefix="/employees", tags=["employees"])


@router.post("", response_model=schemas.Employee, status_code=201)
def create_employee(
    employee: schemas.EmployeeCreate,
    db: Session = Depends(get_db),
):
    """Create a new employee."""
    return crud_module.create_employee(db, employee)


@router.get("", response_model=list[schemas.Employee])
def list_employees(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """List all employees with pagination."""
    skip = (page - 1) * per_page
    return crud_module.list_employees(db, skip=skip, limit=per_page)


@router.get("/{employee_id}", response_model=schemas.Employee)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    """Get an employee by ID."""
    emp = crud_module.get_employee(db, employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp


@router.put("/{employee_id}", response_model=schemas.Employee)
def update_employee(
    employee_id: int,
    employee: schemas.EmployeeCreate,
    db: Session = Depends(get_db),
):
    """Update an employee (full replacement)."""
    emp = crud_module.get_employee(db, employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return crud_module.update_employee(db, employee_id, employee)


@router.patch("/{employee_id}", response_model=schemas.Employee)
def patch_employee(
    employee_id: int,
    employee: schemas.EmployeeUpdate,
    db: Session = Depends(get_db),
):
    """Update an employee (partial update)."""
    emp = crud_module.get_employee(db, employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return crud_module.patch_employee(db, employee_id, employee)


@router.delete("/{employee_id}", status_code=204)
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    """Delete an employee."""
    emp = crud_module.get_employee(db, employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    crud_module.delete_employee(db, employee_id)


@router.get("/{employee_id}/salary", response_model=schemas.SalaryDetail)
def get_salary_detail(employee_id: int, db: Session = Depends(get_db)):
    """Get salary details for an employee (with deductions)."""
    emp = crud_module.get_employee(db, employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return crud_module.calculate_salary(emp)
