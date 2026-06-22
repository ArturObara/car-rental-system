from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services import rentals as rental_service
from app.schemas import schemas
from app.config.security import get_current_user
from app.db import models

router = APIRouter(prefix="/rentals", tags=["Rentals"])

@router.post("", status_code=status.HTTP_201_CREATED)
def rent_car(
    rental_in: schemas.RentalCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    result = rental_service.create_new_rental(
        db=db,
        car_id=rental_in.car_id, 
        user_id=current_user.id,
        start_date=rental_in.start_date,
        days=rental_in.days 
    )
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Car is currently unavailable for rent"
        )
        
    return result