from sqlalchemy.orm import Session

from . import models, schemas


def create_employee(db: Session, emp: schemas.EmployeeCreate) -> models.Employee:
    db_emp = models.Employee(name=emp.name, salary=emp.salary)
    db.add(db_emp)
    db.commit()
    db.refresh(db_emp)
    return db_emp


def list_employees(db: Session) -> list[models.Employee]:
    return db.query(models.Employee).all()
