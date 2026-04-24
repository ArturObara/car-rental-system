from fastapi import FastAPI, HTTPException
from app.schemas import CarCreate, CarResponse
from app.database import SessionLocal
from app.models import Car
from app.logger_config import logger

def register_car_routes(app: FastAPI):
    
    @app.get("/")
    def root() -> dict:
        return {"message": "API is running"}


    @app.get("/cars")
    def get_cars() -> list:
        db = SessionLocal()
        cars = db.query(Car).all()
        db.close()
        return cars
    
    @app.get("/cars/{car_id}", response_model=CarResponse)
    def get_car(car_id: int) -> CarResponse:
        db = SessionLocal()
        car = db.query(Car).filter(Car.id == car_id).first()
        db.close()

        if car:
            return car
        logger.warning(f"Car not found: id={car_id}")
        raise HTTPException(status_code=404, detail="Car not found")
    
    @app.post("/cars")
    def create_car(car: CarCreate) -> dict:
        db = SessionLocal()

        new_car = Car(
            id=car.id,
            brand=car.brand,
            model=car.model,
            year=car.year,
            available=car.available
        )

        db.add(new_car)
        db.commit()
        db.close()

        logger.info(f"Car created: {car.brand} {car.model} (id={car.id})")
        return {"message": f"New car {car.brand}: {car.model} added"}

    @app.delete("/cars/{car_id}")
    def delete_car(car_id: int) -> dict:
        db = SessionLocal()
        car = db.query(Car).filter(Car.id == car_id).first()

        if car:
            db.delete(car)
            db.commit()
            db.close()
            logger.info(f"Car deleted: id={car_id}")
            return {"message": "Car deleted"}

        db.close()
        logger.warning(f"Delete failed, car not found: id={car_id}")
        raise HTTPException(status_code=404, detail="Car not found")
