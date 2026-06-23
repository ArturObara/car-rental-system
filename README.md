# Car Rental System

A backend REST API built with FastAPI for a car rental service. This project serves as an **Internal Back-Office System**, allowing authorized rental employees to manage the vehicle fleet, track physical availability, and handle reservations securely.

## Tech Stack
* **Language:** Python 3.12
* **Framework:** FastAPI, Uvicorn
* **Database:** PostgreSQL, SQLAlchemy (ORM), Psycopg
* **Validation & Config:** Pydantic, python-dotenv
* **Authentication:** python-jose (JWT), Passlib (bcrypt)
* **Testing & Deployment:** Pytest, Docker, Docker Compose

## Key Features
* **Employee Authentication & Management:** Secure registration and login flow for staff members, featuring unique email validation, password hashing (bcrypt), and JWT-based session handling.
* **Fleet Management:** Dedicated, secured endpoints to manage the vehicle database (adding/removing cars) and browse the current fleet inventory.
* **Smart Reservation Engine:** Booking system that prevents double-booking conflicts via strict date overlap validation at the database query level. The system also utilizes an `available` flag to manually mark vehicles as physically out of service (e.g., for maintenance or repairs).

## Getting Started

The easiest way to run this project locally is by using Docker.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ArturObara/car-rental-system.git
   cd car-rental-system
   ```

2. **Configure environment variables:**
   Create a copy of the environment template file and adjust it to your local setup:
   ```bash
   cp env.example .env
   ```

3. **Build and start the containers:**
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