from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

# Use the sync driver (psycopg)
DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5431/ai_factory"

# Create synchronous engine
engine = create_engine(
    DATABASE_URL,
    echo=False  # Set to True to log SQL queries
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency for e.g. FastAPI or any app
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()