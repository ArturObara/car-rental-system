from sqlalchemy.orm import Session
from app.db import models
from datetime import date, timedelta

def create_new_rental(db: Session, car_id: int, user_id: int, days: int = 7):
    car = db.query(models.Car).filter(models.Car.id == car_id).with_for_update().first()
    
    if not car or not car.available:
        return None

    car.available = False
    
    new_rental = models.Rental(
        user_id=user_id,
        car_id=car_id,
        start_date=date.today(),
        end_date=date.today() + timedelta(days=days)
    )
    
    db.add(new_rental)
    db.commit()
    db.refresh(new_rental)
    
    return new_rental