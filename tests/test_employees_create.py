"""Test for POST /employees endpoint (TDD red phase)."""


def test_create_employee_valid_payload(client):
    """
    Test that POST /employees returns 201 with the created employee.

    Given: A valid employee payload
    When: POST /employees is called
    Then: Returns 201 status code and the created employee with all fields
    """
    payload = {
        "full_name": "John Doe",
        "job_title": "Software Engineer",
        "country": "India",
        "salary": 100000.0,
    }

    response = client.post("/employees", json=payload)

    # Assert status code
    assert response.status_code == 201, f"Expected 201, got {response.status_code}"

    # Assert response body
    data = response.json()
    assert data["id"] is not None, "Response should include employee ID"
    assert data["full_name"] == "John Doe"
    assert data["job_title"] == "Software Engineer"
    assert data["country"] == "India"
    assert data["salary"] == 100000.0


def test_create_employee_minimal_valid_payload(client):
    """Test creating employee with minimal valid data."""
    payload = {
        "full_name": "Jane Smith",
        "job_title": "Developer",
        "country": "USA",
        "salary": 85000.0,
    }

    response = client.post("/employees", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["full_name"] == "Jane Smith"


def test_create_employee_zero_salary(client):
    """Test creating employee with zero salary (edge case)."""
    payload = {
        "full_name": "Unpaid Intern",
        "job_title": "Intern",
        "country": "Canada",
        "salary": 0.0,
    }

    response = client.post("/employees", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["salary"] == 0.0


def test_create_employee_invalid_negative_salary(client):
    """Test that negative salary is rejected."""
    payload = {
        "full_name": "Invalid Employee",
        "job_title": "Invalid Role",
        "country": "Invalid Country",
        "salary": -5000.0,
    }

    response = client.post("/employees", json=payload)

    assert response.status_code == 422  # Validation error


def test_create_employee_missing_full_name(client):
    """Test that missing full_name is rejected."""
    payload = {
        "job_title": "Developer",
        "country": "India",
        "salary": 50000.0,
    }

    response = client.post("/employees", json=payload)

    assert response.status_code == 422


def test_create_employee_missing_job_title(client):
    """Test that missing job_title is rejected."""
    payload = {
        "full_name": "John Doe",
        "country": "India",
        "salary": 50000.0,
    }

    response = client.post("/employees", json=payload)

    assert response.status_code == 422


def test_create_employee_missing_country(client):
    """Test that missing country is rejected."""
    payload = {
        "full_name": "John Doe",
        "job_title": "Developer",
        "salary": 50000.0,
    }

    response = client.post("/employees", json=payload)

    assert response.status_code == 422


def test_create_employee_missing_salary(client):
    """Test that missing salary is rejected."""
    payload = {
        "full_name": "John Doe",
        "job_title": "Developer",
        "country": "India",
    }

    response = client.post("/employees", json=payload)

    assert response.status_code == 422
