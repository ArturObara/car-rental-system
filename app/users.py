from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.database import SessionLocal
from app.models import User
from app.schemas import UserCreate, UserLogin
from app.security import hash_password, verify_password, create_access_token, decode_access_token

security = HTTPBearer()

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
    
    @app.post("/login")
    def login_user(user: UserLogin):
        db = SessionLocal()

        existing_user = db.query(User).filter(User.email == user.email).first()

        if not existing_user:
            db.close()
            raise HTTPException(status_code=401, detail="Invalid email or password")

        if not verify_password(user.password, existing_user.hashed_password):
            db.close()
            raise HTTPException(status_code=401, detail="Invalid email or password")

        access_token = create_access_token(data={"sub": existing_user.email})

        db.close()
        return {"access_token": access_token, "token_type": "bearer"}
    

    @app.get("/me")
    def get_me(credentials: HTTPAuthorizationCredentials = Depends(security)):
        token = credentials.credentials

        try:
            payload = decode_access_token(token)
        except ValueError:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        user_email = payload.get("sub")

        if not user_email:
            raise HTTPException(status_code=401, detail="Invalid token payload")

        return {"email": user_email}