from sqlalchemy.orm import Session
from app.db import models
from datetime import date, timedelta

def create_new_rental(db: Session, car_id: int, user_id: int, start_date: date, days: int):
    car = db.query(models.Car).filter(models.Car.id == car_id).first()
    
    if not car or not car.available:
        return None

    calculated_end_date = start_date + timedelta(days=days)

    overlapping_rental = db.query(models.Rental).filter(
        models.Rental.car_id == car_id,
        models.Rental.start_date <= calculated_end_date,
        models.Rental.end_date >= start_date
    ).first()

    if overlapping_rental:
        return None 
    
    new_rental = models.Rental(
        user_id=user_id,
        car_id=car_id,
        start_date=start_date,
        end_date=calculated_end_date
    )
    
    db.add(new_rental)
    db.commit()
    db.refresh(new_rental)
    
    return new_rental