from fastapi import FastAPI
from app.api.cars import register_car_routes
from app.db.database import engine
from app.db.models import Base
from app.api.users import register_user_routes


app = FastAPI()

Base.metadata.create_all(bind=engine)

register_car_routes(app)
register_user_routes(app)