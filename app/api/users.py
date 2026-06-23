from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services import user_service
from app.schemas.schemas import UserCreate, UserLogin
from app.config.security import decode_access_token, create_access_token, get_current_user
from app.config.logger_config import logger

security = HTTPBearer()

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)) -> dict:
    new_user = user_service.create_user(db, user)

    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )
    logger.info(f"User created: {user.email}")
    return {"message": f"User {user.email} created"}


@router.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)) -> dict:
    authenticator_user = user_service.authenticate_user(db, user)

    if authenticator_user is None:
        logger.warning(f"Failed login attempt for email: {user.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
        
    access_token = create_access_token(data={"sub": authenticator_user.email})

    logger.info(f"User logged in successfully: {user.email}")
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me")
def get_me(current_user = Depends(get_current_user)) -> dict:
    return {
        "email": current_user.email,
        "name": current_user.name
    }