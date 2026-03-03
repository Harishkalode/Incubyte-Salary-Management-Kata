"""Test configuration and fixtures."""
import os
import pytest
from pathlib import Path
from fastapi.testclient import TestClient

# Set test database before importing app
os.environ["DATABASE_URL"] = "sqlite:///./test.db"


@pytest.fixture(scope="function", autouse=True)
def cleanup_test_db():
    """Clean up test database before and after each test."""
    db_file = Path("./test.db")
    
    # Remove before test
    if db_file.exists():
        db_file.unlink()
    
    yield
    
    # Remove after test  
    if db_file.exists():
        db_file.unlink()


@pytest.fixture(scope="function")
def client():
    """Provide FastAPI test client."""
    # Re-initialize app with test database
    from importlib import reload
    import app.database
    import app.models  
    import app.main
    
    # Reload to pick up environment variable
    reload(app.database)
    reload(app.models)
    reload(app.main)
    
    # Initialize database
    app.database.init_db()
    
    from app.main import app as fastapi_app
    from app.database import get_db
    
    # Create test client
    test_client = TestClient(fastapi_app)
    
    yield test_client





