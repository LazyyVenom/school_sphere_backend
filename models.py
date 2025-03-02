from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, field_validator
from enum import Enum
from datetime import datetime, date, time

# Enum definitions
class Gender(str, Enum):
    MALE = "M"
    FEMALE = "F"
    OTHER = "O"

class StudentStatus(str, Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    GRADUATED = "Graduated"
    SUSPENDED = "Suspended"

class Status(str, Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    EX_MEMBER = "ExMember"
    SUSPENDED = "Suspended"

class AttendanceStatus(str, Enum):
    ABSENT = "Absent"
    PRESENT = "Present"
    LATE = "Late"
    EXCUSED = "Excused"

class DayOfWeek(str, Enum):
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"

class AssignmentType(str, Enum):
    HOMEWORK = "HW"
    GRADED = "Graded"

# New Enums
class NotificationType(str, Enum):
    BROADCAST = "Broadcast"
    NEWS = "News"
    REMINDER = "Reminder"
    ALERT = "Alert"
    
class RecipientType(str, Enum):
    ALL = "All"
    STUDENTS = "Students"
    TEACHERS = "Teachers"
    SPECIFIC_CLASS = "Specific Class"
    
class CreatorType(str, Enum):
    ADMIN = "Admin"
    TEACHER = "Teacher"
    
class LeaveType(str, Enum):
    SICK = "Sick"
    CASUAL = "Casual"
    ANNUAL = "Annual"
    EMERGENCY = "Emergency"
    
class LeaveStatus(str, Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    
class FeedbackType(str, Enum):
    ACADEMIC = "Academic"
    BEHAVIORAL = "Behavioral"
    GENERAL = "General"
    
class ItemStatus(str, Enum):
    LOST = "Lost"
    FOUND = "Found"

# Teacher model
class Teacher(BaseModel):
    teacher_id: str = Field(..., description="Unique identifier for the teacher")
    name: str
    gender: Gender
    phone: int = Field(..., description="10-digit phone number")
    email: str
    status: Status
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

# Admin model
class Admin(BaseModel):
    admin_id: str = Field(..., description="Unique identifier for the admin")
    name: str
    gender: Gender
    phone: int = Field(..., description="10-digit phone number")
    email: str
    status: Status
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

# Subject model
class Subject(BaseModel):
    subject_id: str = Field(..., description="Unique identifier for the subject")
    name: str
    code: str

# Class_Subject model
class Class_Subject(BaseModel):
    class_sub_id: str = Field(..., description="Unique identifier for class-subject relation")
    class_id: str = Field(..., description="Foreign key to classes")
    subject_id: str = Field(..., description="Foreign key to subjects")
    subject_teacher: str = Field(..., description="Foreign key to teachers")

# Attendance model
class Attendance(BaseModel):
    attendance_id: str = Field(..., description="Unique identifier for attendance record")
    class_id: str = Field(..., description="Foreign key to classes")
    student_id: str = Field(..., description="Foreign key to students")
    date: date
    status: AttendanceStatus

# Timetable model
class Timetable(BaseModel):
    timetable_id: str = Field(..., description="Unique identifier for timetable entry")
    class_sub_id: str = Field(..., description="Foreign key to class_subjects")
    day: DayOfWeek
    start_time: time
    end_time: time
    
    @field_validator('end_time')
    @classmethod
    def validate_end_time(cls, v, values):
        if 'start_time' in values.data and v <= values.data['start_time']:
            raise ValueError('End time must be after start time')
        return v

# Exams model
class Exams(BaseModel):
    exam_id: str = Field(..., description="Unique identifier for exam")
    class_id: str = Field(..., description="Foreign key to classes")
    subject_id: str = Field(..., description="Foreign key to subjects")
    date: date
    name: str
    total_marks: int = Field(..., gt=0)

# Grade model
class Grade(BaseModel):
    grades_id: str = Field(..., description="Unique identifier for grade")
    student_id: str = Field(..., description="Foreign key to students")
    exam_id: str = Field(..., description="Foreign key to exams")
    marks: float = Field(..., ge=0)
    grade: str = Field(..., max_length=2)
    
    @field_validator('marks')
    @classmethod
    def validate_marks(cls, v, values):
        # Additional validation could be added here to check against total_marks
        # from the related exam, but would require database access
        if v < 0:
            raise ValueError('Marks cannot be negative')
        return v

# Assignment model
class Assignment(BaseModel):
    assignment_id: str = Field(..., description="Unique identifier for assignment")
    class_sub_id: str = Field(..., description="Foreign key to class_subjects")
    created_time: datetime = Field(default_factory=datetime.now)
    title: str = Field(..., max_length=255)
    dueDate: datetime
    description: Optional[str] = None
    type: AssignmentType
    
    @field_validator('dueDate')
    @classmethod
    def validate_due_date(cls, v, values):
        if 'created_time' in values.data and v <= values.data['created_time']:
            raise ValueError('Due date must be after created time')
        return v

# Assignment_grading model
class Assignment_grading(BaseModel):
    grading_id: str = Field(..., description="Unique identifier for grading")
    assignment_id: str = Field(..., description="Foreign key to assignments")
    student_id: str = Field(..., description="Foreign key to students")
    feedback: Optional[str] = None
    grade: Optional[str] = Field(None, max_length=2)
    marks: Optional[int] = Field(None, ge=0)
    graded_at: Optional[datetime] = None

# Notification model
class Notification(BaseModel):
    notification_id: str = Field(..., description="Unique identifier for notification")
    title: str = Field(..., max_length=255)
    type: NotificationType
    recipient: RecipientType
    class_id: Optional[str] = Field(None, description="Foreign key to classes, nullable")
    created_at: datetime = Field(default_factory=datetime.now)
    creator_type: CreatorType
    admin_id: Optional[str] = Field(None, description="Foreign key to admins")
    teacher_id: Optional[str] = Field(None, description="Foreign key to teachers")
    
    @field_validator('class_id')
    @classmethod
    def validate_class_id(cls, v, values):
        if 'recipient' in values.data and values.data['recipient'] == RecipientType.SPECIFIC_CLASS and v is None:
            raise ValueError('Class ID is required when recipient is Specific Class')
        return v
    
    @field_validator('admin_id', 'teacher_id')
    @classmethod
    def validate_creator_ids(cls, v, values, field):
        if 'creator_type' in values.data:
            if values.data['creator_type'] == CreatorType.ADMIN and field.name == 'admin_id' and v is None:
                raise ValueError('Admin ID is required when creator is Admin')
            elif values.data['creator_type'] == CreatorType.TEACHER and field.name == 'teacher_id' and v is None:
                raise ValueError('Teacher ID is required when creator is Teacher')
        return v

# Leave_Application model
class Leave_Application(BaseModel):
    leave_id: str = Field(..., description="Unique identifier for leave application")
    student_id: str = Field(..., description="Foreign key to students")
    title: str = Field(..., max_length=255)
    type: LeaveType
    start_date: date
    end_date: date
    status: LeaveStatus = Field(default=LeaveStatus.PENDING)
    reason: Optional[str] = None
    applied_at: datetime = Field(default_factory=datetime.now)
    
    @field_validator('end_date')
    @classmethod
    def validate_end_date(cls, v, values):
        if 'start_date' in values.data and v < values.data['start_date']:
            raise ValueError('End date must be on or after start date')
        return v

# Feedback model
class Feedback(BaseModel):
    feedback_id: str = Field(..., description="Unique identifier for feedback")
    student_id: str = Field(..., description="Foreign key to students")
    teacher_id: str = Field(..., description="Foreign key to teachers")
    title: str = Field(..., max_length=255)
    feedback_type: FeedbackType
    feedback_text: str
    given_at: datetime = Field(default_factory=datetime.now)

# Extra_Credit model
class Extra_Credit(BaseModel):
    credit_id: str = Field(..., description="Unique identifier for extra credit")
    student_id: str = Field(..., description="Foreign key to students")
    admin_id: str = Field(..., description="Foreign key to admins")
    grade: str = Field(..., max_length=2)

# Lost_and_Found model
class Lost_and_Found(BaseModel):
    unique_id: str = Field(..., description="Unique identifier for lost and found item")
    admin_id: str = Field(..., description="Foreign key to admins")
    item_name: str = Field(..., max_length=255)
    description: Optional[str] = None
    location: str = Field(..., max_length=255)
    date_reported: date = Field(default_factory=date.today)
    status: ItemStatus

