"""Salary Management Kata FastAPI application."""
from contextlib import asynccontextmanager
from fastapi import FastAPI

from .database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage app startup and shutdown."""
    # Startup - commented out for tests
    # init_db()
    yield
    # Shutdown


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    from .routers import employees, metrics  # Import here for app factory pattern
    
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
    
    return app


# Create the default app instance for production
app = create_app()
