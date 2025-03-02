from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date, Time, Float, Boolean, Text, Enum
from sqlalchemy.orm import relationship
from datetime import datetime, date, time
import enum
from database import Base
import uuid

# Enum definitions
class Gender(enum.Enum):
    MALE = "M"
    FEMALE = "F"
    OTHER = "O"

class StudentStatus(enum.Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    GRADUATED = "Graduated"
    SUSPENDED = "Suspended"

class Status(enum.Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    EX_MEMBER = "ExMember"
    SUSPENDED = "Suspended"

class AttendanceStatus(enum.Enum):
    ABSENT = "Absent"
    PRESENT = "Present"
    LATE = "Late"
    EXCUSED = "Excused"

class DayOfWeek(enum.Enum):
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"

class AssignmentType(enum.Enum):
    HOMEWORK = "HW"
    GRADED = "Graded"

class NotificationType(enum.Enum):
    BROADCAST = "Broadcast"
    NEWS = "News"
    REMINDER = "Reminder"
    ALERT = "Alert"
    
class RecipientType(enum.Enum):
    ALL = "All"
    STUDENTS = "Students"
    TEACHERS = "Teachers"
    SPECIFIC_CLASS = "Specific Class"
    
class CreatorType(enum.Enum):
    ADMIN = "Admin"
    TEACHER = "Teacher"
    
class LeaveType(enum.Enum):
    SICK = "Sick"
    CASUAL = "Casual"
    ANNUAL = "Annual"
    EMERGENCY = "Emergency"
    
class LeaveStatus(enum.Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    
class FeedbackType(enum.Enum):
    ACADEMIC = "Academic"
    BEHAVIORAL = "Behavioral"
    GENERAL = "General"
    
class ItemStatus(enum.Enum):
    LOST = "Lost"
    FOUND = "Found"

def generate_uuid():
    return str(uuid.uuid4())

class Teacher(Base):
    __tablename__ = "teachers"
    
    teacher_id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    phone = Column(Integer, nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    status = Column(Enum(Status), nullable=False)
    profile_pic = Column(String(255), nullable=True)
    address = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    password_hash = Column(String(255), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    
    # Relationships
    classes = relationship("Class", back_populates="teacher")
    class_subjects = relationship("Class_Subject", back_populates="teacher")
    feedbacks = relationship("Feedback", back_populates="teacher")
    notifications = relationship("Notification", back_populates="teacher")
    
    def __repr__(self):
        return f"<Teacher {self.name}>"

class Class(Base):
    __tablename__ = "classes"
    
    class_id = Column(String(36), primary_key=True, default=generate_uuid)
    class_number = Column(Integer, nullable=False)
    section = Column(String(1), nullable=False)
    class_teacher_id = Column(String(36), ForeignKey("teachers.teacher_id"), nullable=False)
    
    # Relationships
    teacher = relationship("Teacher", back_populates="classes")
    students = relationship("Student", back_populates="class_")
    class_subjects = relationship("Class_Subject", back_populates="class_")
    attendances = relationship("Attendance", back_populates="class_")
    exams = relationship("Exams", back_populates="class_")
    notifications = relationship("Notification", back_populates="class_")
    
    def __repr__(self):
        return f"<Class {self.class_number}-{self.section}>"

class Student(Base):
    __tablename__ = "students"
    
    student_id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    class_id = Column(String(36), ForeignKey("classes.class_id"), nullable=False)
    roll_no = Column(Integer, nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    phone = Column(Integer, nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    status = Column(Enum(StudentStatus), nullable=False)
    profile_pic = Column(String(255), nullable=True)
    address = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    password_hash = Column(String(255), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    
    # Relationships
    class_ = relationship("Class", back_populates="students")
    attendances = relationship("Attendance", back_populates="student")
    grades = relationship("Grade", back_populates="student")
    assignment_gradings = relationship("Assignment_grading", back_populates="student")
    leave_applications = relationship("Leave_Application", back_populates="student")
    feedbacks = relationship("Feedback", back_populates="student")
    extra_credits = relationship("Extra_Credit", back_populates="student")
    
    def __repr__(self):
        return f"<Student {self.name}>"

class Admin(Base):
    __tablename__ = "admins"
    
    admin_id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    phone = Column(Integer, nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    status = Column(Enum(Status), nullable=False)
    profile_pic = Column(String(255), nullable=True)
    address = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    password_hash = Column(String(255), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    
    # Relationships
    notifications = relationship("Notification", back_populates="admin")
    extra_credits = relationship("Extra_Credit", back_populates="admin")
    lost_found_items = relationship("Lost_and_Found", back_populates="admin")
    
    def __repr__(self):
        return f"<Admin {self.name}>"

class Subject(Base):
    __tablename__ = "subjects"
    
    subject_id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    code = Column(String(50), nullable=False, unique=True)
    
    # Relationships
    class_subjects = relationship("Class_Subject", back_populates="subject")
    exams = relationship("Exams", back_populates="subject")
    
    def __repr__(self):
        return f"<Subject {self.name}>"

class Class_Subject(Base):
    __tablename__ = "class_subjects"
    
    class_sub_id = Column(String(36), primary_key=True, default=generate_uuid)
    class_id = Column(String(36), ForeignKey("classes.class_id"), nullable=False)
    subject_id = Column(String(36), ForeignKey("subjects.subject_id"), nullable=False)
    subject_teacher_id = Column(String(36), ForeignKey("teachers.teacher_id"), nullable=False)
    
    # Relationships
    class_ = relationship("Class", back_populates="class_subjects")
    subject = relationship("Subject", back_populates="class_subjects")
    teacher = relationship("Teacher", back_populates="class_subjects")
    timetables = relationship("Timetable", back_populates="class_subject")
    assignments = relationship("Assignment", back_populates="class_subject")
    
    def __repr__(self):
        return f"<Class_Subject {self.class_sub_id}>"

class Attendance(Base):
    __tablename__ = "attendances"
    
    attendance_id = Column(String(36), primary_key=True, default=generate_uuid)
    class_id = Column(String(36), ForeignKey("classes.class_id"), nullable=False)
    student_id = Column(String(36), ForeignKey("students.student_id"), nullable=False)
    date = Column(Date, nullable=False)
    status = Column(Enum(AttendanceStatus), nullable=False)
    
    # Relationships
    class_ = relationship("Class", back_populates="attendances")
    student = relationship("Student", back_populates="attendances")
    
    def __repr__(self):
        return f"<Attendance {self.student_id} on {self.date}: {self.status}>"

class Timetable(Base):
    __tablename__ = "timetables"
    
    timetable_id = Column(String(36), primary_key=True, default=generate_uuid)
    class_sub_id = Column(String(36), ForeignKey("class_subjects.class_sub_id"), nullable=False)
    day = Column(Enum(DayOfWeek), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    
    # Relationships
    class_subject = relationship("Class_Subject", back_populates="timetables")
    
    def __repr__(self):
        return f"<Timetable {self.day} {self.start_time}-{self.end_time}>"

class Exams(Base):
    __tablename__ = "exams"
    
    exam_id = Column(String(36), primary_key=True, default=generate_uuid)
    class_id = Column(String(36), ForeignKey("classes.class_id"), nullable=False)
    subject_id = Column(String(36), ForeignKey("subjects.subject_id"), nullable=False)
    date = Column(Date, nullable=False)
    name = Column(String(255), nullable=False)
    total_marks = Column(Integer, nullable=False)
    
    # Relationships
    class_ = relationship("Class", back_populates="exams")
    subject = relationship("Subject", back_populates="exams")
    grades = relationship("Grade", back_populates="exam")
    
    def __repr__(self):
        return f"<Exam {self.name} on {self.date}>"

class Grade(Base):
    __tablename__ = "grades"
    
    grades_id = Column(String(36), primary_key=True, default=generate_uuid)
    student_id = Column(String(36), ForeignKey("students.student_id"), nullable=False)
    exam_id = Column(String(36), ForeignKey("exams.exam_id"), nullable=False)
    marks = Column(Float, nullable=False)
    grade = Column(String(2), nullable=False)
    
    # Relationships
    student = relationship("Student", back_populates="grades")
    exam = relationship("Exams", back_populates="grades")
    
    def __repr__(self):
        return f"<Grade {self.student_id} in {self.exam_id}: {self.grade}>"

class Assignment(Base):
    __tablename__ = "assignments"
    
    assignment_id = Column(String(36), primary_key=True, default=generate_uuid)
    class_sub_id = Column(String(36), ForeignKey("class_subjects.class_sub_id"), nullable=False)
    created_time = Column(DateTime, default=datetime.now)
    title = Column(String(255), nullable=False)
    dueDate = Column(DateTime, nullable=False)
    description = Column(Text, nullable=True)
    type = Column(Enum(AssignmentType), nullable=False)
    
    # Relationships
    class_subject = relationship("Class_Subject", back_populates="assignments")
    gradings = relationship("Assignment_grading", back_populates="assignment")
    
    def __repr__(self):
        return f"<Assignment {self.title} due {self.dueDate}>"

class Assignment_grading(Base):
    __tablename__ = "assignment_gradings"
    
    grading_id = Column(String(36), primary_key=True, default=generate_uuid)
    assignment_id = Column(String(36), ForeignKey("assignments.assignment_id"), nullable=False)
    student_id = Column(String(36), ForeignKey("students.student_id"), nullable=False)
    feedback = Column(Text, nullable=True)
    grade = Column(String(2), nullable=True)
    marks = Column(Integer, nullable=True)
    graded_at = Column(DateTime, nullable=True)
    
    # Relationships
    assignment = relationship("Assignment", back_populates="gradings")
    student = relationship("Student", back_populates="assignment_gradings")
    
    def __repr__(self):
        return f"<Assignment_grading {self.student_id} for {self.assignment_id}>"

class Notification(Base):
    __tablename__ = "notifications"
    
    notification_id = Column(String(36), primary_key=True, default=generate_uuid)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    type = Column(Enum(NotificationType), nullable=False)
    recipient = Column(Enum(RecipientType), nullable=False)
    class_id = Column(String(36), ForeignKey("classes.class_id"), nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    creator_type = Column(Enum(CreatorType), nullable=False)
    admin_id = Column(String(36), ForeignKey("admins.admin_id"), nullable=True)
    teacher_id = Column(String(36), ForeignKey("teachers.teacher_id"), nullable=True)
    
    # Relationships
    class_ = relationship("Class", back_populates="notifications")
    admin = relationship("Admin", back_populates="notifications")
    teacher = relationship("Teacher", back_populates="notifications")
    
    def __repr__(self):
        return f"<Notification {self.title}>"

class Leave_Application(Base):
    __tablename__ = "leave_applications"
    
    leave_id = Column(String(36), primary_key=True, default=generate_uuid)
    student_id = Column(String(36), ForeignKey("students.student_id"), nullable=False)
    title = Column(String(255), nullable=False)
    type = Column(Enum(LeaveType), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(Enum(LeaveStatus), nullable=False, default=LeaveStatus.PENDING)
    reason = Column(Text, nullable=True)
    applied_at = Column(DateTime, default=datetime.now)
    
    # Relationships
    student = relationship("Student", back_populates="leave_applications")
    
    def __repr__(self):
        return f"<Leave_Application {self.title} for {self.student_id}>"

class Feedback(Base):
    __tablename__ = "feedbacks"
    
    feedback_id = Column(String(36), primary_key=True, default=generate_uuid)
    student_id = Column(String(36), ForeignKey("students.student_id"), nullable=False)
    teacher_id = Column(String(36), ForeignKey("teachers.teacher_id"), nullable=False)
    title = Column(String(255), nullable=False)
    feedback_type = Column(Enum(FeedbackType), nullable=False)
    feedback_text = Column(Text, nullable=False)
    given_at = Column(DateTime, default=datetime.now)
    
    # Relationships
    student = relationship("Student", back_populates="feedbacks")
    teacher = relationship("Teacher", back_populates="feedbacks")
    
    def __repr__(self):
        return f"<Feedback {self.title} for {self.student_id}>"

class Extra_Credit(Base):
    __tablename__ = "extra_credits"
    
    credit_id = Column(String(36), primary_key=True, default=generate_uuid)
    student_id = Column(String(36), ForeignKey("students.student_id"), nullable=False)
    admin_id = Column(String(36), ForeignKey("admins.admin_id"), nullable=False)
    grade = Column(String(2), nullable=False)
    
    # Relationships
    student = relationship("Student", back_populates="extra_credits")
    admin = relationship("Admin", back_populates="extra_credits")
    
    def __repr__(self):
        return f"<Extra_Credit {self.student_id}: {self.grade}>"

class Lost_and_Found(Base):
    __tablename__ = "lost_and_found"
    
    unique_id = Column(String(36), primary_key=True, default=generate_uuid)
    admin_id = Column(String(36), ForeignKey("admins.admin_id"), nullable=False)
    item_name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    location = Column(String(255), nullable=False)
    date_reported = Column(Date, default=date.today)
    status = Column(Enum(ItemStatus), nullable=False)
    
    # Relationships
    admin = relationship("Admin", back_populates="lost_found_items")
    
    def __repr__(self):
        return f"<Lost_and_Found {self.item_name}: {self.status}>"
