from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.schemas.schemas import CarCreate, CarResponse
from app.db.database import get_db
from app.services import car_service
from app.config.logger_config import logger

router = APIRouter(
    prefix="/cars",
    tags=["Cars"]
)

@router.get("", response_model=list[CarResponse])
def get_cars(db: Session = Depends(get_db)) -> list[CarResponse]:
    return car_service.get_all_cars(db)


@router.get("/{car_id}", response_model=CarResponse)
def get_car(car_id: int, db: Session = Depends(get_db)) -> CarResponse:
    car = car_service.get_car_by_id(db, car_id)

    if car:
        return car
    
    logger.warning(f"Car not found: id={car_id}")
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Car not found"
    )


@router.post("", status_code=status.HTTP_201_CREATED)
def create_car(car: CarCreate, db: Session = Depends(get_db)) -> dict:
    new_car = car_service.create_car(db, car)
    
    if not new_car:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Car with this id already exists"
        )
        
    logger.info(f"Car created: {car.brand} {car.model}")
    return {"message": f"New car {car.brand}: {car.model} added"}
    

@router.delete("/{car_id}", status_code=status.HTTP_200_OK)
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