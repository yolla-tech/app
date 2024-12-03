from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

DATABASE_URL = "postgresql://postgres:postgres@localhost/yolla"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Initialize tables
try:
    from models.user import User
    
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")
except Exception as e:
    print(f"Error creating tables: {e}")
