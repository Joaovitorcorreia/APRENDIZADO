from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123456@localhost:5432/postgres"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"options": "-c client_min_messages=notice -c lc_messages=C"})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()