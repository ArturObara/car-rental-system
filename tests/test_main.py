from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "API is running"}



def test_get_cars() -> None:
    response = client.get("/cars")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_missing_car() -> None:
    response = client.get("/cars/999999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Car not found"}



def test_create_user() -> None:
    unique_email = "test_new_user_60@example.com"

    response = client.post(
        "/users",
        json={
            "name": "NEW Test User2",
            "email": unique_email,
            "password": "abc4321"
        }
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": f"User {unique_email} created"
    }

def test_login_user() -> None:
    email = "test_new_user1@example.com"
    password = "abc4321"

    client.post(
        "/users",
        json={
            "name": "Login New User",
            "email": email,
            "password": password
        }
    )

    response = client.post(
        "/login",
        json={
            "email": email,
            "password": password
        }
    )

    assert response.status_code == 200
    response_data = response.json()
    assert "access_token" in response_data
    assert response_data["token_type"] == "bearer"