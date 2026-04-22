from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost/car_rental"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

