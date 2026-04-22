from fastapi import FastAPI, HTTPException
from app.schemas import CarCreate,CarResponse
from app.database import SessionLocal
from app.models import Car

def register_car_routes(app: FastAPI):
    
    @app.get("/")
    def root():
        return {"message": "API is running"}


    @app.get("/cars")
    def cars_root():
        db = SessionLocal()
        cars = db.query(Car).all()
        db.close()
        return cars
    
    @app.get("/cars/{car_id}", response_model=CarResponse)
    def get_car_root(car_id: int):
        db = SessionLocal()
        car = db.query(Car).filter(Car.id == car_id).first()
        db.close()

        if car:
            return car
        raise HTTPException(status_code=404, detail="Car not found")
    
    @app.post("/cars")
    def add_car_root(car: CarCreate):
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

        return {"message": f"New car {car.brand}: {car.model} added"}

    @app.delete("/cars/{car_id}")
    def delete_car_root(car_id: int):
        db = SessionLocal()
        car = db.query(Car).filter(Car.id == car_id).first()

        if car:
            db.delete(car)
            db.commit()
            db.close()
            return {"message": "Car deleted"}

        db.close()
        raise HTTPException(status_code=404, detail="Car not found")
