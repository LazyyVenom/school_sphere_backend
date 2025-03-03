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

# StudentCreate model for creating new students without auto-generated fields
class StudentCreate(BaseModel):
    name: str
    class_id: str
    roll_no: int
    gender: Gender
    phone: int
    email: str
    status: StudentStatus = StudentStatus.ACTIVE
    profile_pic: Optional[str] = None
    address: str
    password: str
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
    def validate_class_id(cls, v, info):
        values = info.data
        if 'recipient' in values and values['recipient'] == RecipientType.SPECIFIC_CLASS and v is None:
            raise ValueError('Class ID is required when recipient is Specific Class')
        return v
    
    @field_validator('admin_id')
    @classmethod
    def validate_admin_id(cls, v, info):
        values = info.data
        if 'creator_type' in values and values['creator_type'] == CreatorType.ADMIN and v is None:
            raise ValueError('Admin ID is required when creator is Admin')
        return v
    
    @field_validator('teacher_id')
    @classmethod
    def validate_teacher_id(cls, v, info):
        values = info.data
        if 'creator_type' in values and values['creator_type'] == CreatorType.TEACHER and v is None:
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

# Filter models for POST requests
class StudentFilter(BaseModel):
    student_id: Optional[str] = None
    name: Optional[str] = None
    class_id: Optional[str] = None
    roll_no: Optional[int] = None
    gender: Optional[Gender] = None
    email: Optional[str] = None
    status: Optional[StudentStatus] = None
    
class TeacherFilter(BaseModel):
    teacher_id: Optional[str] = None
    name: Optional[str] = None
    gender: Optional[Gender] = None
    email: Optional[str] = None
    status: Optional[Status] = None

class ClassFilter(BaseModel):
    class_id: Optional[str] = None
    class_number: Optional[int] = None
    section: Optional[str] = None
    class_teacher_id: Optional[str] = None

class SubjectFilter(BaseModel):
    subject_id: Optional[str] = None
    name: Optional[str] = None
    code: Optional[str] = None

class AttendanceFilter(BaseModel):
    attendance_id: Optional[str] = None
    class_id: Optional[str] = None
    student_id: Optional[str] = None
    date: Optional[date] = None
    date_from: Optional[date] = None
    date_to: Optional[date] = None
    status: Optional[AttendanceStatus] = None

class ExamFilter(BaseModel):
    exam_id: Optional[str] = None
    class_id: Optional[str] = None
    subject_id: Optional[str] = None
    date: Optional[date] = None
    date_from: Optional[date] = None
    date_to: Optional[date] = None
    name: Optional[str] = None

class GradeFilter(BaseModel):
    grades_id: Optional[str] = None
    student_id: Optional[str] = None
    exam_id: Optional[str] = None
    grade: Optional[str] = None
    
class AssignmentFilter(BaseModel):
    assignment_id: Optional[str] = None
    class_sub_id: Optional[str] = None
    title: Optional[str] = None
    type: Optional[AssignmentType] = None
    due_before: Optional[datetime] = None
    due_after: Optional[datetime] = None

class FeedbackFilter(BaseModel):
    feedback_id: Optional[str] = None
    student_id: Optional[str] = None
    teacher_id: Optional[str] = None
    feedback_type: Optional[FeedbackType] = None
    given_from: Optional[datetime] = None
    given_to: Optional[datetime] = None

class LeaveApplicationFilter(BaseModel):
    leave_id: Optional[str] = None
    student_id: Optional[str] = None
    type: Optional[LeaveType] = None
    status: Optional[LeaveStatus] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    applied_from: Optional[datetime] = None
    applied_to: Optional[datetime] = None

# Create models for entities

class TeacherCreate(BaseModel):
    name: str
    gender: Gender
    phone: int
    email: str
    status: Status = Status.ACTIVE
    profile_pic: Optional[str] = None
    address: str
    password: str
    date_of_birth: date
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        if not (1000000000 <= v <= 9999999999):
            raise ValueError('Phone number must be 10 digits')
        return v

class ClassCreate(BaseModel):
    class_number: int
    section: str
    class_teacher_id: str
    
    @field_validator('section')
    @classmethod
    def validate_section(cls, v):
        if len(v) != 1:
            raise ValueError('Section must be a single character')
        return v

class SubjectCreate(BaseModel):
    name: str
    code: str

class AdminCreate(BaseModel):
    name: str
    gender: Gender
    phone: int
    email: str
    status: Status = Status.ACTIVE
    profile_pic: Optional[str] = None
    address: str
    password: str
    date_of_birth: date
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        if not (1000000000 <= v <= 9999999999):
            raise ValueError('Phone number must be 10 digits')
        return v

class Class_SubjectCreate(BaseModel):
    class_id: str
    subject_id: str
    subject_teacher_id: str

class AttendanceCreate(BaseModel):
    class_id: str
    student_id: str
    date: date
    status: AttendanceStatus

class TimetableCreate(BaseModel):
    class_sub_id: str
    day: DayOfWeek
    start_time: time
    end_time: time
    
    @field_validator('end_time')
    @classmethod
    def validate_end_time(cls, v, values):
        if 'start_time' in values.data and v <= values.data['start_time']:
            raise ValueError('End time must be after start time')
        return v

class ExamsCreate(BaseModel):
    class_id: str
    subject_id: str
    date: date
    name: str
    total_marks: int = Field(..., gt=0)

class GradeCreate(BaseModel):
    student_id: str
    exam_id: str
    marks: float = Field(..., ge=0)
    grade: str = Field(..., max_length=2)

class AssignmentCreate(BaseModel):
    class_sub_id: str
    title: str = Field(..., max_length=255)
    dueDate: datetime
    description: Optional[str] = None
    type: AssignmentType

class Assignment_gradingCreate(BaseModel):
    assignment_id: str
    student_id: str
    feedback: Optional[str] = None
    grade: Optional[str] = Field(None, max_length=2)
    marks: Optional[int] = Field(None, ge=0)

class NotificationCreate(BaseModel):
    title: str = Field(..., max_length=255)
    content: str
    type: NotificationType
    recipient: RecipientType
    class_id: Optional[str] = None
    creator_type: CreatorType
    admin_id: Optional[str] = None
    teacher_id: Optional[str] = None
    
    @field_validator('class_id')
    @classmethod
    def validate_class_id(cls, v, info):
        values = info.data
        if 'recipient' in values and values['recipient'] == RecipientType.SPECIFIC_CLASS and v is None:
            raise ValueError('Class ID is required when recipient is Specific Class')
        return v
    
    @field_validator('admin_id')
    @classmethod
    def validate_admin_id(cls, v, info):
        values = info.data
        if 'creator_type' in values and values['creator_type'] == CreatorType.ADMIN and v is None:
            raise ValueError('Admin ID is required when creator is Admin')
        return v
    
    @field_validator('teacher_id')
    @classmethod
    def validate_teacher_id(cls, v, info):
        values = info.data
        if 'creator_type' in values and values['creator_type'] == CreatorType.TEACHER and v is None:
            raise ValueError('Teacher ID is required when creator is Teacher')
        return v

class LeaveApplicationCreate(BaseModel):
    student_id: str
    title: str = Field(..., max_length=255)
    type: LeaveType
    start_date: date
    end_date: date
    reason: Optional[str] = None
    
    @field_validator('end_date')
    @classmethod
    def validate_end_date(cls, v, values):
        if 'start_date' in values.data and v < values.data['start_date']:
            raise ValueError('End date must be on or after start date')
        return v

class FeedbackCreate(BaseModel):
    student_id: str
    teacher_id: str
    title: str = Field(..., max_length=255)
    feedback_type: FeedbackType
    feedback_text: str

class ExtraCreditCreate(BaseModel):
    student_id: str
    admin_id: str
    grade: str = Field(..., max_length=2)

class LostAndFoundCreate(BaseModel):
    admin_id: str
    item_name: str = Field(..., max_length=255)
    description: Optional[str] = None
    location: str = Field(..., max_length=255)
    status: ItemStatus

# Update models for entities
class StudentUpdate(BaseModel):
    name: Optional[str] = None
    class_id: Optional[str] = None
    roll_no: Optional[int] = None
    gender: Optional[Gender] = None
    phone: Optional[int] = None
    email: Optional[str] = None
    status: Optional[StudentStatus] = None
    profile_pic: Optional[str] = None
    address: Optional[str] = None
    date_of_birth: Optional[date] = None
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        if v is not None and not (1000000000 <= v <= 9999999999):
            raise ValueError('Phone number must be 10 digits')
        return v

class TeacherUpdate(BaseModel):
    name: Optional[str] = None
    gender: Optional[Gender] = None
    phone: Optional[int] = None
    email: Optional[str] = None
    status: Optional[Status] = None
    profile_pic: Optional[str] = None
    address: Optional[str] = None
    date_of_birth: Optional[date] = None
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        if v is not None and not (1000000000 <= v <= 9999999999):
            raise ValueError('Phone number must be 10 digits')
        return v

class ClassUpdate(BaseModel):
    class_number: Optional[int] = None
    section: Optional[str] = None
    class_teacher_id: Optional[str] = None
    
    @field_validator('section')
    @classmethod
    def validate_section(cls, v):
        if v is not None and len(v) != 1:
            raise ValueError('Section must be a single character')
        return v

class SubjectUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None

class AdminUpdate(BaseModel):
    name: Optional[str] = None
    gender: Optional[Gender] = None
    phone: Optional[int] = None
    email: Optional[str] = None
    status: Optional[Status] = None
    profile_pic: Optional[str] = None
    address: Optional[str] = None
    date_of_birth: Optional[date] = None
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        if v is not None and not (1000000000 <= v <= 9999999999):
            raise ValueError('Phone number must be 10 digits')
        return v

class AttendanceUpdate(BaseModel):
    status: Optional[AttendanceStatus] = None

class TimetableUpdate(BaseModel):
    day: Optional[DayOfWeek] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    
    @field_validator('end_time')
    @classmethod
    def validate_end_time(cls, v, values):
        if v is not None and 'start_time' in values.data and values.data['start_time'] is not None and v <= values.data['start_time']:
            raise ValueError('End time must be after start time')
        return v

class ExamUpdate(BaseModel):
    date: Optional[date] = None
    name: Optional[str] = None
    total_marks: Optional[int] = None

class GradeUpdate(BaseModel):
    marks: Optional[float] = None
    grade: Optional[str] = None

class AssignmentUpdate(BaseModel):
    title: Optional[str] = None
    dueDate: Optional[datetime] = None
    description: Optional[str] = None
    type: Optional[AssignmentType] = None

class AssignmentGradingUpdate(BaseModel):
    feedback: Optional[str] = None
    grade: Optional[str] = None
    marks: Optional[int] = None

class NotificationUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    type: Optional[NotificationType] = None

class LeaveApplicationUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[LeaveStatus] = None
    reason: Optional[str] = None

class FeedbackUpdate(BaseModel):
    title: Optional[str] = None
    feedback_type: Optional[FeedbackType] = None
    feedback_text: Optional[str] = None

class ExtraCreditUpdate(BaseModel):
    grade: Optional[str] = None

class LostAndFoundUpdate(BaseModel):
    item_name: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    status: Optional[ItemStatus] = None

