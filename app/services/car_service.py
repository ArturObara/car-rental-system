from sqlalchemy.orm import Session
from app.db.models import Car
from app.schemas.schemas import CarCreate

def get_all_cars(db: Session):
    return db.query(Car).all()

def get_car_by_id(db: Session, car_id: int):
    return db.query(Car).filter(Car.id == car_id).first()

def create_car(db: Session, car_data: CarCreate):
    existing_car = db.query(Car).filter(Car.id == car_data.id).first()
    if existing_car:
        return None
    
    new_car = Car(
        id=car_data.id,
        brand=car_data.brand,
        model=car_data.model,
        year=car_data.year,
        available=car_data.available
    )
    db.add(new_car)
    db.commit()
    db.refresh(new_car)

    return new_car

def delete_car(db: Session, car_id: int):
    car = db.query(Car).filter(Car.id == car_id).first()

    if not car:
        return None
    
    db.delete(car)
    db.commit()
    return True
    