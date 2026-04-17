from fastapi import FastAPI, HTTPException
from app.schemas import CarCreate,CarResponse

cars = [
    {
    "id" : 1, 
    "brand": "Audi",
    "model": "A5",
    "year": 2020,
    "available": True
    },
    {
    "id" : 2, 
    "brand": "BMW",
    "model": "M2",
    "year": 2023,
    "available": False
    },
    {
    "id" : 3, 
    "brand": "Mercedes",
    "model": "CLA",
    "year": 2018,
    "available": True
    },
    {
    "id" : 4, 
    "brand": "Audi",
    "model": "A4",
    "year": 2024,
    "available": False
    }
]

def register_car_routes(app: FastAPI):
    @app.get("/cars")
    def cars_root():
        return cars

    @app.get("/cars/{car_id}", response_model=CarResponse)
    def get_car_root(car_id: int):
        for car in cars:
            if car["id"] == car_id:
                return car 
        raise HTTPException(status_code=404, detail="Car not found")
        
    @app.post("/cars")
    def add_car_root(car: CarCreate):
        cars.append(car.model_dump())
        return {"message": f"New car {car.brand}: {car.model} added"}

    @app.delete("/cars/{car_id}")
    def delete_car_root(car_id: int):
        for car in cars:
            if car["id"] == car_id:
                cars.remove(car)
                return {"message": "Car deleted"}
        raise HTTPException(status_code=404, detail="Car not found")
