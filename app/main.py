from fastapi import FastAPI

from app.db.database import engine
from app.db.models import Base
from app.api import cars, users, rentals 


app = FastAPI(
    title="Car Rental System API",
    description="Backend API for managing car rentals, inventory, and users.",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

app.include_router(cars.router)
app.include_router(users.router)
app.include_router(rentals.router)