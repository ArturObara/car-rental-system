from fastapi.testclient import TestClient
import uuid
from app.main import app
from app.db.database import get_db
from app.db.models import Car

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
    unique_email = f"test_{uuid.uuid4()}@example.com"
    
    response = client.post(
        "/users",
        json={
            "name": "NEW Test User",
            "email": unique_email,
            "password": "abc4321"
        }
    )
    assert response.status_code == 201

def test_login_user() -> None:
    unique_email = f"test_{uuid.uuid4()}@example.com"
    password = "abc4321"

    client.post(
        "/users",
        json={
            "name": "Login New User",
            "email": unique_email,
            "password": password
        }
    )

    response = client.post(
        "/users/login", 
        json={
            "email": unique_email,
            "password": password
        }
    )

    assert response.status_code == 200 
    response_data = response.json()
    assert "access_token" in response_data
    assert response_data["token_type"] == "bearer"

def test_rental_collision() -> None:
    db = next(get_db())

    test_car = Car(id=1, brand="Toyota", model="Corolla", year=2022, available=True)
    db.merge(test_car)
    db.commit()

    email = f"test_{uuid.uuid4()}@example.com"
    password = "password123"
    
    client.post("/users", json={"name": "Test User", "email": email, "password": password})
    
    login_response = client.post("/users/login", json={"email": email, "password": password})
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response1 = client.post(
        "/rentals",
        json={"car_id": 1, "start_date": "2026-07-01", "days": 3},
        headers=headers
    )
    assert response1.status_code == 201

    response2 = client.post(
        "/rentals",
        json={"car_id": 1, "start_date": "2026-07-02", "days": 3},
        headers=headers
    )
    assert response2.status_code == 400
    assert response2.json()["detail"] == "Car is currently unavailable for rent"