"""Test configuration and fixtures."""
import os
import sys
import tempfile
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker


@pytest.fixture(scope="function")
def client(monkeypatch):
    """Provide FastAPI test client with isolated test database."""
    # Create a temporary database file
    fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    os.unlink(db_path)
    
    db_url = f"sqlite:///{db_path}"
    
    # Set up test database  
    test_engine = create_engine(
        db_url,
        connect_args={"check_same_thread": False},
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    
    # Import models and Base
    from app import models  # noqa: F401
    from app.database import Base
    
    # Create tables on test engine
    Base.metadata.create_all(bind=test_engine)
    
    # Verify tables were created
    insp = inspect(test_engine)
    tables = insp.get_table_names()
    assert "employees" in tables, f"employees table not created. Tables: {tables}"
    
    # Import database module
    from app import database
    
    # Create a new get_db that uses the test database
    def test_get_db():
        """Override get_db to use test database."""
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    # Clear any cached router module imports to ensure fresh imports with patched get_db
    for module_name in list(sys.modules.keys()):
        if module_name.startswith('app.routers'):
            del sys.modules[module_name]
    
    # Monkeypatch the get_db function BEFORE app factory is called
    monkeypatch.setattr(database, "get_db", test_get_db)
    
    # Create the app (it will import routers which will use the patched get_db)
    from app.main import create_app
    app = create_app()
    
    # Create test client
    test_client = TestClient(app)
    
    yield test_client
    
    # Cleanup
    test_engine.dispose()
    if os.path.exists(db_path):
        os.unlink(db_path)







