# Car Rental System

A backend REST API built with FastAPI for a car rental service. The system provides a secure client facing interface for browsing available vehicles and making reservations while also serving as a core foundation for internal fleet management.

## Tech Stack
* **Language:** Python 3.12
* **Framework:** FastAPI, Uvicorn
* **Database:** PostgreSQL, SQLAlchemy (ORM), Psycopg
* **Validation & Config:** Pydantic, python-dotenv
* **Authentication:** python-jose (JWT), Passlib (bcrypt)
* **Testing & Deployment:** Pytest, Docker, Docker Compose

## Key Features
* **User Authentication & Management:** Secure registration and login flow with unique email validation, password hashing (bcrypt), and JWT-based session handling.
* **Fleet Inventory & Browsing:** Dedicated endpoints to populate and manage the vehicle database, coupled with a RESTful `GET /cars` route for users to browse the fleet.
* **Smart Reservation Engine:** Booking system that verifies vehicle status via an `available` database flag and employs strict date overlap validation at the database query level to prevent double booking conflicts.

## Getting Started

The easiest way to run this project locally is by using Docker.

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/ArturObara/car-rental-system.git](https://github.com/ArturObara/car-rental-system.git)
   cd car-rental-system
   ```

2. **Build and start the containers:**
   ```bash
   docker compose up --build
   ```
The application and the PostgreSQL database will start automatically.

## API Documentation

FastAPI automatically generates interactive API documentation. Once the containers are running, you can explore and test all endpoints directly from your browser:

* **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
* **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Running Tests

The project includes a test suite covering business logic, database interactions, and API endpoints. 

Thanks to the pre-configured `pytest.ini` file, you don't need to manually set the Python path. To run the tests, ensure your virtual environment is active and execute:

```bash
pytest -v
```