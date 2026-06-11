from sqlalchemy.orm import Session
from app.db.models import Car
from app.schemas.schemas import CarCreate

def get_all_cars(db: Session) -> list[Car]:
    return db.query(Car).all()


def get_car_by_id(db: Session, car_id: int) -> Car | None:
    return db.query(Car).filter(Car.id == car_id).first()


def create_car(db: Session, car_data: CarCreate) -> Car:
    new_car = Car(**car_data.model_dump())
    
    db.add(new_car)
    db.commit()
    db.refresh(new_car)

    return new_car


def delete_car(db: Session, car_id: int) -> bool:
    car = get_car_by_id(db, car_id)

    if not car:
        return False
    
    db.delete(car)
    db.commit()
    return True