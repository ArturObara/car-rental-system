from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.database import SessionLocal
from app.models import User
from app.schemas import UserCreate, UserLogin
from app.security import hash_password, verify_password, create_access_token, decode_access_token
from app.logger_config import logger

security = HTTPBearer()

def register_user_routes(app: FastAPI):
    @app.post("/users")
    def create_user(user: UserCreate) -> dict:
        db = SessionLocal()

        try:
            existing_user = db.query(User).filter(User.email == user.email).first()
            
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="User with this email already exists"
                )

            new_user = User(
                name=user.name,
                email=user.email,
                hashed_password=hash_password(user.password)
            )

            db.add(new_user)
            db.commit()

            logger.info(f"User created: {user.email}")
            return {"message": f"User {user.email} created"}
        finally:
            db.close()

    @app.post("/login")
    def login_user(user: UserLogin) -> dict:
        db = SessionLocal()

        try:
            existing_user = db.query(User).filter(User.email == user.email).first()

            if not existing_user:
                logger.warning(f"Failed login attempt for email: {user.email}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid email or password",
                )

            if not verify_password(user.password, existing_user.hashed_password):
                logger.warning(f"Failed login attempt for email: {user.email}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid email or password",
                )
            access_token = create_access_token(data={"sub": existing_user.email})
            logger.info(f"User logged in successfully: {user.email}")
            return {"access_token": access_token, "token_type": "bearer"}
        finally: 
                db.close()

    @app.get("/me")
    def get_me(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
        token = credentials.credentials

        try:
            payload = decode_access_token(token)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user_email = payload.get("sub")

        if not user_email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid token payload",
                headers={"WWW-Authenticate": "Bearer"},
    )

        return {"email": user_email}