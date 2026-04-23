from pydantic import BaseModel, Field


class CarBase(BaseModel):
    brand: str = Field(min_length=1)
    model: str = Field(min_length=1)
    year: int = Field(ge=1900, le=2100)
    available: bool


class CarCreate(CarBase):
    id: int


class CarResponse(CarBase):
    id: int

class UserCreate(BaseModel):
    name: str = Field(min_length=1)
    email: str = Field(min_length=1)
    password: str = Field(min_length=1)