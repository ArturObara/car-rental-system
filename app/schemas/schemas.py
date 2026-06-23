from pydantic import BaseModel, Field, EmailStr, field_validator
from datetime import date

class CarBase(BaseModel):
    brand: str = Field(min_length=1)
    model: str = Field(min_length=1)
    year: int = Field(ge=1900, le=2100)
    available: bool

class CarCreate(CarBase):
    pass

class CarResponse(CarBase):
    id: int
    
    model_config = {"from_attributes": True}


class UserCreate(BaseModel):
    name: str = Field(min_length=1)
    email: EmailStr
    password: str = Field(min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1)


class RentalCreate(BaseModel):
    car_id: int
    start_date: date
    days: int = Field(ge=1)

    @field_validator("start_date")
    @classmethod
    def start_date_not_in_past(cls, val: date) -> date:
        if val < date.today():
            raise ValueError("Data rozpoczęcia rezerwacji (start_date) nie może być w przeszłości")
        return val

class RentalResponse(BaseModel):
    id: int
    car_id: int
    user_id: int
    start_date: date
    end_date: date

    model_config = {"from_attributes": True}