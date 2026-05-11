from fastapi import FastAPI, HTTPException, status
from app.schemas import CarCreate, CarResponse
from app.database import SessionLocal
from app.models import Car
from app.logger_config import logger

def register_car_routes(app: FastAPI):
    
    @app.get("/")
    def root() -> dict:
        return {"message": "API is running"}


    @app.get("/cars", response_model=list[CarResponse])
    def get_cars() -> list[CarResponse]:
        db = SessionLocal()

        try:
            cars = db.query(Car).all()
            return cars
        finally:
            db.close()

    @app.get("/cars/{car_id}", response_model=CarResponse)
    def get_car(car_id: int) -> CarResponse:
        db = SessionLocal()

        try:
            car = db.query(Car).filter(Car.id == car_id).first()
            if car:
                return car
            logger.warning(f"Car not found: id={car_id}")
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car not found"
            )
        finally: 
            db.close()

    
    @app.post("/cars")
    def create_car(car: CarCreate) -> dict:
        db = SessionLocal()

        try:
            existing_car = db.query(Car).filter(Car.id == car.id).first()

            if existing_car:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Car with this id already exists"
                )
               
            new_car = Car(
                id=car.id,
                brand=car.brand,
                model=car.model,
                year=car.year,
                available=car.available
            )
            db.add(new_car)
            db.commit()
            logger.info(f"Car created: {car.brand} {car.model} (id={car.id})")
            return {"message": f"New car {car.brand}: {car.model} added"}
        finally:
            db.close()

        

    @app.delete("/cars/{car_id}")
    def delete_car(car_id: int) -> dict:
        db = SessionLocal()

        try:
            car = db.query(Car).filter(Car.id == car_id).first()

            if car:
                db.delete(car)
                db.commit()
                logger.info(f"Car deleted: id={car_id}")
                return {"message": "Car deleted"}
            
            logger.warning(f"Delete failed, car not found: id={car_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Car not found"
                )
        finally:
            db.close()
