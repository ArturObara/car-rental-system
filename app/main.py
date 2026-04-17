from fastapi import FastAPI
from app.cars import register_car_routes
from app.database import engine
from app.models import Base


app = FastAPI()

Base.metadata.create_all(bind=engine)

register_car_routes(app)