from sqlalchemy.orm import Session
from app.db.models import User
from app.schemas.schemas import UserCreate, UserLogin
from app.config.security import hash_password
from app.config.security import  verify_password


def create_user(db: Session, user_data: UserCreate):
    existing_user = db.query(User).filter(User.email == user_data.email).first()

    if existing_user:
        return None
    
    
    new_user = User(
    name=user_data.name,
    email=user_data.email,
    hashed_password=hash_password(user_data.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def authenticate_user(db: Session, login_data: UserLogin):
    existing_user = db.query(User).filter(User.email == login_data.email).first()

    if not existing_user:
        return None
    if not verify_password(login_data.password, existing_user.hashed_password):
            return None
    
    return existing_user