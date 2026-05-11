from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.schemas.schemas import CarCreate, CarResponse
from app.db.database import get_db
from app.services import car_service
from app.config.logger_config import logger

def register_car_routes(app: FastAPI):
    
    @app.get("/")
    def root() -> dict:
        return {"message": "API is running"}


    @app.get("/cars", response_model=list[CarResponse])
    def get_cars(db: Session = Depends(get_db)) -> list[CarResponse]:
        return car_service.get_all_cars(db)


    @app.get("/cars/{car_id}", response_model=CarResponse)
    def get_car(car_id: int, db: Session = Depends(get_db)) -> CarResponse:
        
        car = car_service.get_car_by_id(db, car_id)

        if car:
            return car
        
        logger.warning(f"Car not found: id={car_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car not found"
        )
    
    @app.post("/cars")
    def create_car(car: CarCreate, db: Session = Depends(get_db)) -> dict:
            
        new_car = car_service.create_car(db, car)
        if not new_car:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Car with this id already exists"
            )
        logger.info(f"Car created: {car.brand} {car.model} (id={car.id})")
        return {"message": f"New car {car.brand}: {car.model} added"}
        

    @app.delete("/cars/{car_id}")
    def delete_car(car_id: int, db: Session = Depends(get_db)) -> dict:

        result = car_service.delete_car(db, car_id)
            
        if result is None:
            logger.warning(f"Delete failed, car not found: id={car_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Car not found"
            )
        logger.info(f"Car deleted: id={car_id}")
        return {"message": "Car deleted"}