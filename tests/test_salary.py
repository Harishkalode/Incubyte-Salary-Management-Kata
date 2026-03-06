"""Tests for salary calculation endpoints."""


def test_get_salary_india_tds(client):
    """Test salary calculation for India (10% TDS)."""
    create_resp = client.post("/employees", json={
        "full_name": "Raj",
        "job_title": "Developer",
        "country": "India",
        "salary": 100000,
    })
    emp_id = create_resp.json()["id"]

    resp = client.get(f"/employees/{emp_id}/salary")
    assert resp.status_code == 200
    data = resp.json()

    assert data["gross"] == 100000
    assert "tds" in data["deductions"]
    assert data["deductions"]["tds"] == 10000  # 10% of 100000
    assert data["total_deductions"] == 10000
    assert data["net"] == 90000  # 100000 - 10000


def test_get_salary_usa_tds(client):
    """Test salary calculation for USA (12% TDS)."""
    create_resp = client.post("/employees", json={
        "full_name": "John",
        "job_title": "Engineer",
        "country": "United States",
        "salary": 100000,
    })
    emp_id = create_resp.json()["id"]

    resp = client.get(f"/employees/{emp_id}/salary")
    assert resp.status_code == 200
    data = resp.json()

    assert data["gross"] == 100000
    assert data["deductions"]["tds"] == 12000  # 12% of 100000
    assert data["total_deductions"] == 12000
    assert data["net"] == 88000


def test_get_salary_usa_short_form(client):
    """Test salary calculation for USA (USA/US variations)."""
    for country_name in ["USA", "US", "usa", "us"]:
        create_resp = client.post("/employees", json={
            "full_name": "Test",
            "job_title": "Dev",
            "country": country_name,
            "salary": 100000,
        })
        emp_id = create_resp.json()["id"]

        resp = client.get(f"/employees/{emp_id}/salary")
        assert resp.status_code == 200
        data = resp.json()
        assert data["deductions"]["tds"] == 12000, f"Failed for {country_name}"


def test_get_salary_other_country_no_tds(client):
    """Test salary calculation for country with no TDS."""
    create_resp = client.post("/employees", json={
        "full_name": "Nick",
        "job_title": "Designer",
        "country": "Canada",
        "salary": 100000,
    })
    emp_id = create_resp.json()["id"]

    resp = client.get(f"/employees/{emp_id}/salary")
    assert resp.status_code == 200
    data = resp.json()

    assert data["gross"] == 100000
    assert data["deductions"] == {}  # No deductions
    assert data["total_deductions"] == 0
    assert data["net"] == 100000


def test_get_salary_not_found(client):
    """Test salary for non-existent employee."""
    resp = client.get("/employees/9999/salary")
    assert resp.status_code == 404


def test_get_salary_zero_salary(client):
    """Test salary calculation with zero salary."""
    create_resp = client.post("/employees", json={
        "full_name": "Zero",
        "job_title": "Intern",
        "country": "India",
        "salary": 0,
    })
    emp_id = create_resp.json()["id"]

    resp = client.get(f"/employees/{emp_id}/salary")
    assert resp.status_code == 200
    data = resp.json()

    assert data["gross"] == 0
    assert data["deductions"]["tds"] == 0
    assert data["total_deductions"] == 0
    assert data["net"] == 0
