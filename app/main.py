from fastapi import FastAPI
from app.cars import register_car_routes
from app.database import engine
from app.models import Base
from app.users import register_user_routes


app = FastAPI()

Base.metadata.create_all(bind=engine)

register_car_routes(app)
register_user_routes(app)