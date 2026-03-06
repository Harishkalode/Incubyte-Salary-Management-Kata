"""Tests for metrics endpoints."""


def test_metrics_by_country(client):
    """Test metrics for a specific country."""
    # Create employees in India
    client.post("/employees", json={
        "full_name": "Emp1",
        "job_title": "Dev",
        "country": "India",
        "salary": 100000,
    })
    client.post("/employees", json={
        "full_name": "Emp2",
        "job_title": "Dev",
        "country": "India",
        "salary": 120000,
    })
    # Create employee in USA
    client.post("/employees", json={
        "full_name": "Emp3",
        "job_title": "Dev",
        "country": "USA",
        "salary": 150000,
    })
    
    # Get India metrics
    resp = client.get("/metrics/country/India")
    assert resp.status_code == 200
    data = resp.json()
    
    assert data["min"] == 100000
    assert data["max"] == 120000
    assert data["avg"] == 110000  # (100000 + 120000) / 2
    assert data["count"] == 2


def test_metrics_by_country_not_found(client):
    """Test metrics for country with no employees."""
    resp = client.get("/metrics/country/NonExistent")
    # Should return 404 or empty result based on requirements
    # We'll test for 404
    assert resp.status_code == 404


def test_metrics_by_job_title(client):
    """Test metrics for a specific job title."""
    # Create employees with same job title
    client.post("/employees", json={
        "full_name": "Emp1",
        "job_title": "Developer",
        "country": "India",
        "salary": 80000,
    })
    client.post("/employees", json={
        "full_name": "Emp2",
        "job_title": "Developer",
        "country": "USA",
        "salary": 120000,
    })
    # Create employee with different job title
    client.post("/employees", json={
        "full_name": "Emp3",
        "job_title": "Manager",
        "country": "India",
        "salary": 150000,
    })
    
    # Get Developer metrics
    resp = client.get("/metrics/job/Developer")
    assert resp.status_code == 200
    data = resp.json()
    
    assert data["avg"] == 100000  # (80000 + 120000) / 2
    assert data["count"] == 2


def test_metrics_by_job_title_not_found(client):
    """Test metrics for job title with no employees."""
    resp = client.get("/metrics/job/NonExistent")
    assert resp.status_code == 404


def test_metrics_case_insensitive(client):
    """Test that metrics are case-insensitive."""
    client.post("/employees", json={
        "full_name": "Emp1",
        "job_title": "Senior Developer",
        "country": "India",
        "salary": 100000,
    })
    
    # Try different cases
    resp1 = client.get("/metrics/job/Senior Developer")
    resp2 = client.get("/metrics/job/senior developer")
    
    assert resp1.status_code == 200
    assert resp2.status_code == 200
    assert resp1.json()["count"] == resp2.json()["count"]
