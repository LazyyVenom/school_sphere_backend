from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# MySQL connection string for XAMPP
# Default XAMPP MySQL credentials: username="root", password="" (empty)
# You can adjust these values as needed
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:@localhost:3306/school_sphere"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
