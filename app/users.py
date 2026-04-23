from fastapi import FastAPI
from app.database import SessionLocal
from app.models import User
from app.schemas import UserCreate
from app.security import hash_password


def register_user_routes(app: FastAPI):
    @app.post("/users")
    def create_user(user: UserCreate):
        db = SessionLocal()

        new_user = User(
            name=user.name,
            email=user.email,
            hashed_password=hash_password(user.password)
        )

        db.add(new_user)
        db.commit()
        db.close()

        return {"message": f"User {user.email} created"}