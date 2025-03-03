from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, engine
import sql_models
from typing import List
from models import Student as StudentModel, StudentCreate
from passlib.context import CryptContext 
import uuid

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

sql_models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="SchoolSphere API")

@app.get("/")
def read_root():
    return {"message": "Welcome to SchoolSphere API"}

# About page route
@app.get("/about")
def about() -> dict[str, str]:
    return {"message": "This is the about page."}

# Get all students route
@app.get("/students", response_model=List[StudentModel])
def get_all_students(db: Session = Depends(get_db)):
    """
    Get all students in the database
    """
    students = db.query(sql_models.Student).all()
    if not students:
        raise HTTPException(status_code=404, detail="No students found")
    return students

# Add a student route
@app.post("/students", response_model=StudentModel, status_code=201)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    """
    Create a new student in the database
    """
    db_student = db.query(sql_models.Student).filter(sql_models.Student.email == student.email).first()
    if db_student:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    class_check = db.query(sql_models.Class).filter(sql_models.Class.class_id == student.class_id).first()
    if not class_check:
        raise HTTPException(status_code=404, detail="Class not found")
    
    roll_check = db.query(sql_models.Student).filter(
        sql_models.Student.class_id == student.class_id,
        sql_models.Student.roll_no == student.roll_no
    ).first()
    if roll_check:
        raise HTTPException(status_code=400, detail="Roll number already exists in this class")
    
    new_student = sql_models.Student(
        student_id=str(uuid.uuid4()),
        name=student.name,
        class_id=student.class_id,
        roll_no=student.roll_no,
        gender=student.gender,
        phone=student.phone,
        email=student.email,
        status=student.status,
        profile_pic=student.profile_pic,
        address=student.address,
        password_hash=pwd_context.hash(student.password),
        date_of_birth=student.date_of_birth
    )
    
    try:
        db.add(new_student)
        db.commit()
        db.refresh(new_student)
        return new_student
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create student: {str(e)}")

