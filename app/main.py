"""Salary Management Kata FastAPI application."""
from contextlib import asynccontextmanager
from fastapi import FastAPI

from .database import init_db
from .routers import employees, metrics


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage app startup and shutdown."""
    # Startup
    init_db()
    yield
    # Shutdown


app = FastAPI(
    title="Salary Management Kata",
    description="API for managing employees and calculating salaries",
    version="1.0.0",
    lifespan=lifespan,
)

# Register routers
app.include_router(employees.router)
app.include_router(metrics.router)


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok"}

