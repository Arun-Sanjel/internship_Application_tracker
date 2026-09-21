from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_and_get_application():
    response = client.post(
        "/applications",
        json={
            "company": "Example Company",
            "position": "Software Engineering Intern",
            "location": "Dallas, TX",
            "date_applied": "2026-09-21",
            "status": "Applied",
            "notes": "Applied through company website",
        },
    )

    assert response.status_code == 201
    application_id = response.json()["id"]

    get_response = client.get(f"/applications/{application_id}")

    assert get_response.status_code == 200
    assert get_response.json()["company"] == "Example Company"


def test_missing_company_is_rejected():
    response = client.post(
        "/applications",
        json={
            "position": "Software Engineering Intern",
            "status": "Applied",
        },
    )

    assert response.status_code == 422
