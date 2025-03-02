from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, field_validator
from enum import Enum
from datetime import datetime, date

# Enum definitions
class Gender(str, Enum):
    MALE = "M"
    FEMALE = "F"
    OTHER = "O"

class TeacherStatus(str, Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    EX_MEMBER = "ExMember"
    SUSPENDED = "Suspended"

class StudentStatus(str, Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    GRADUATED = "Graduated"
    SUSPENDED = "Suspended"

# Teacher model
class Teacher(BaseModel):
    teacher_id: str = Field(..., description="Unique identifier for the teacher")
    name: str
    gender: Gender
    phone: int = Field(..., description="10-digit phone number")
    email: str
    status: TeacherStatus
    profile_pic: Optional[str] = None
    address: str
    created_at: datetime = Field(default_factory=datetime.now)
    password_hash: str
    date_of_birth: date
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        if not (1000000000 <= v <= 9999999999):
            raise ValueError('Phone number must be 10 digits')
        return v

# Class model
class Class(BaseModel):
    class_id: str = Field(..., description="Unique identifier for the class")
    class_number: int = Field(..., alias="class")
    section: str = Field(..., max_length=1)
    class_teacher: str = Field(..., description="Foreign key to teachers")

# Student model
class Student(BaseModel):
    student_id: str = Field(..., description="Unique identifier for the student")
    name: str
    class_id: str = Field(..., description="Foreign key to classes")
    roll_no: int
    gender: Gender
    phone: int = Field(..., description="10-digit phone number")
    email: str
    status: StudentStatus
    profile_pic: Optional[str] = None
    address: str
    created_at: datetime = Field(default_factory=datetime.now)
    password_hash: str
    date_of_birth: date
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        if not (1000000000 <= v <= 9999999999):
            raise ValueError('Phone number must be 10 digits')
        return v

