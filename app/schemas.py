from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class EmployeeCreate(BaseModel):
    """Schema for creating an employee."""
    full_name: str = Field(..., min_length=1, max_length=255)
    job_title: str = Field(..., min_length=1, max_length=255)
    country: str = Field(..., min_length=1, max_length=100)
    salary: float = Field(..., ge=0, description="Salary must be >= 0")


class EmployeeUpdate(BaseModel):
    """Schema for updating an employee."""
    full_name: Optional[str] = Field(None, min_length=1, max_length=255)
    job_title: Optional[str] = Field(None, min_length=1, max_length=255)
    country: Optional[str] = Field(None, min_length=1, max_length=100)
    salary: Optional[float] = Field(None, ge=0)


class Employee(EmployeeCreate):
    """Schema for employee response."""
    id: int
    model_config = ConfigDict(from_attributes=True)


class SalaryDetail(BaseModel):
    """Salary calculation response."""
    gross: float
    deductions: dict[str, float]
    total_deductions: float
    net: float


class MetricResponse(BaseModel):
    """Metrics response."""
    min: Optional[float] = None
    max: Optional[float] = None
    avg: Optional[float] = None
    count: int


class JobMetricResponse(BaseModel):
    """Job metrics response (only avg and count)."""
    avg: Optional[float] = None
    count: int
