"""Metrics endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import get_db
from .. import schemas
from .. import crud as crud_module

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get("/country/{country}", response_model=schemas.MetricResponse)
def get_metrics_by_country(country: str, db: Session = Depends(get_db)):
    """Get salary metrics for employees in a country."""
    metrics = crud_module.get_country_metrics(db, country)
    if metrics["count"] == 0:
        raise HTTPException(status_code=404, detail="No employees found in this country")
    return metrics


@router.get("/job/{job_title}", response_model=schemas.JobMetricResponse)
def get_metrics_by_job(job_title: str, db: Session = Depends(get_db)):
    """Get salary metrics for employees with a job title."""
    metrics = crud_module.get_job_metrics(db, job_title)
    if metrics["count"] == 0:
        raise HTTPException(status_code=404, detail="No employees found with this job title")
    return metrics
