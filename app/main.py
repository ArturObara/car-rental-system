from fastapi import FastAPI
from app.cars import register_car_routes


app = FastAPI()

register_car_routes(app)