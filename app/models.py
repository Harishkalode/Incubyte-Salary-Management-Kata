from sqlalchemy import Column, Integer, String, Float

from .database import Base


class Employee(Base):
    """Employee model."""
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    job_title = Column(String(255), nullable=False)
    country = Column(String(100), nullable=False)
    salary = Column(Float, nullable=False)  # Using float; Decimal recommended for production
