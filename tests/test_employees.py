"""Tests for Employee CRUD endpoints."""


def test_create_employee(client):
    """Test creating an employee."""
    payload = {
        "full_name": "John Doe",
        "job_title": "Software Engineer",
        "country": "India",
        "salary": 100000,
    }
    resp = client.post("/employees", json=payload)
    assert resp.status_code == 201
    body = resp.json()
    assert body["full_name"] == "John Doe"
    assert body["job_title"] == "Software Engineer"
    assert body["country"] == "India"
    assert body["salary"] == 100000
    assert "id" in body


def test_get_employees(client):
    """Test listing employees."""
    # Create an employee first
    client.post("/employees", json={
        "full_name": "Alice",
        "job_title": "Developer",
        "country": "USA",
        "salary": 80000,
    })
    
    resp = client.get("/employees")
    assert resp.status_code == 200
    body = resp.json()
    assert isinstance(body, list)
    assert len(body) >= 1
    assert any(e.get("full_name") == "Alice" for e in body)


def test_get_employee_by_id(client):
    """Test getting a single employee."""
    # Create an employee
    create_resp = client.post("/employees", json={
        "full_name": "Bob",
        "job_title": "Manager",
        "country": "UK",
        "salary": 120000,
    })
    emp_id = create_resp.json()["id"]
    
    resp = client.get(f"/employees/{emp_id}")
    assert resp.status_code == 200
    body = resp.json()
    assert body["id"] == emp_id
    assert body["full_name"] == "Bob"


def test_get_employee_not_found(client):
    """Test getting non-existent employee."""
    resp = client.get("/employees/9999")
    assert resp.status_code == 404


def test_update_employee(client):
    """Test updating an employee."""
    # Create an employee
    create_resp = client.post("/employees", json={
        "full_name": "Charlie",
        "job_title": "Analyst",
        "country": "Canada",
        "salary": 75000,
    })
    emp_id = create_resp.json()["id"]
    
    # Update with PUT (full update)
    resp = client.put(f"/employees/{emp_id}", json={
        "full_name": "Charles",
        "job_title": "Senior Analyst",
        "country": "Canada",
        "salary": 85000,
    })
    assert resp.status_code == 200
    body = resp.json()
    assert body["full_name"] == "Charles"
    assert body["job_title"] == "Senior Analyst"
    assert body["salary"] == 85000


def test_patch_employee(client):
    """Test partial update of an employee."""
    # Create an employee
    create_resp = client.post("/employees", json={
        "full_name": "David",
        "job_title": "Intern",
        "country": "India",
        "salary": 30000,
    })
    emp_id = create_resp.json()["id"]
    
    # Partial update with PATCH
    resp = client.patch(f"/employees/{emp_id}", json={
        "job_title": "Junior Developer",
        "salary": 40000,
    })
    assert resp.status_code == 200
    body = resp.json()
    assert body["full_name"] == "David"  # unchanged
    assert body["job_title"] == "Junior Developer"  # changed
    assert body["salary"] == 40000  # changed


def test_delete_employee(client):
    """Test deleting an employee."""
    # Create an employee
    create_resp = client.post("/employees", json={
        "full_name": "Eve",
        "job_title": "Designer",
        "country": "Netherlands",
        "salary": 65000,
    })
    emp_id = create_resp.json()["id"]
    
    # Delete
    resp = client.delete(f"/employees/{emp_id}")
    assert resp.status_code == 204
    
    # Verify it's gone
    resp = client.get(f"/employees/{emp_id}")
    assert resp.status_code == 404


def test_list_employees_pagination(client):
    """Test pagination in list employees."""
    # Create 5 employees
    for i in range(5):
        client.post("/employees", json={
            "full_name": f"Employee {i}",
            "job_title": "Developer",
            "country": "India",
            "salary": 50000 + i * 1000,
        })
    
    # Test default pagination
    resp = client.get("/employees")
    assert resp.status_code == 200
    body = resp.json()
    assert len(body) <= 10  # default per_page
    
    # Test with per_page param
    resp = client.get("/employees?per_page=2")
    assert resp.status_code == 200
    body = resp.json()
    assert len(body) == 2
    
    # Test with page param
    resp = client.get("/employees?page=2&per_page=2")
    assert resp.status_code == 200


def test_create_employee_invalid_salary(client):
    """Test creating employee with negative salary (should fail)."""
    payload = {
        "full_name": "Invalid",
        "job_title": "Developer",
        "country": "India",
        "salary": -1000,  # Invalid
    }
    resp = client.post("/employees", json=payload)
    assert resp.status_code == 422  # Validation error


def test_create_employee_missing_fields(client):
    """Test creating employee with missing required fields."""
    payload = {
        "full_name": "Incomplete",
        # Missing job_title, country, salary
    }
    resp = client.post("/employees", json=payload)
    assert resp.status_code == 422  # Validation error
