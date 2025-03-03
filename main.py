from fastapi import FastAPI, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from database import get_db, engine
import sql_models
from typing import List, Optional
from models import (
    # Existing models
    Student as StudentModel, StudentCreate, StudentFilter,
    Teacher as TeacherModel, TeacherFilter, TeacherCreate,
    Class as ClassModel, ClassFilter, ClassCreate,
    Subject as SubjectModel, SubjectFilter, SubjectCreate,
    Attendance as AttendanceModel, AttendanceFilter, AttendanceCreate,
    Exams as ExamsModel, ExamFilter, ExamsCreate,
    Grade as GradeModel, GradeFilter, GradeCreate,
    Assignment as AssignmentModel, AssignmentFilter, AssignmentCreate,
    Feedback as FeedbackModel, FeedbackFilter, FeedbackCreate,
    Leave_Application as LeaveApplicationModel, LeaveApplicationFilter, LeaveApplicationCreate,
    Admin as AdminModel, AdminCreate,
    Class_Subject as Class_SubjectModel, Class_SubjectCreate,
    Timetable as TimetableModel, TimetableCreate,
    Assignment_grading as Assignment_gradingModel, Assignment_gradingCreate,
    Notification as NotificationModel, NotificationCreate,
    Extra_Credit as Extra_CreditModel, ExtraCreditCreate,
    Lost_and_Found as Lost_and_FoundModel, LostAndFoundCreate,
    StudentUpdate, TeacherUpdate, ClassUpdate, SubjectUpdate, AdminUpdate,
    AttendanceUpdate, TimetableUpdate, ExamUpdate, GradeUpdate, AssignmentUpdate,
    AssignmentGradingUpdate, NotificationUpdate, LeaveApplicationUpdate,
    FeedbackUpdate, ExtraCreditUpdate, LostAndFoundUpdate,
    # Import enum classes
    ItemStatus, LeaveStatus, Gender, StudentStatus, Status, AttendanceStatus,
    DayOfWeek, AssignmentType, NotificationType, RecipientType, CreatorType,
    LeaveType, FeedbackType
)
from passlib.context import CryptContext 
import uuid
from datetime import datetime, date, timedelta

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

# Get students with filters
@app.post("/students/filter", response_model=List[StudentModel])
def filter_students(
    filters: Optional[StudentFilter] = None,
    db: Session = Depends(get_db)
):
    """
    Get students with optional filters.
    If no filters are provided, returns all students.
    """
    query = db.query(sql_models.Student)
    
    # Apply filters if provided
    if filters:
        if filters.student_id:
            query = query.filter(sql_models.Student.student_id == filters.student_id)
        if filters.name:
            query = query.filter(sql_models.Student.name.ilike(f'%{filters.name}%'))
        if filters.class_id:
            query = query.filter(sql_models.Student.class_id == filters.class_id)
        if filters.roll_no:
            query = query.filter(sql_models.Student.roll_no == filters.roll_no)
        if filters.gender:
            query = query.filter(sql_models.Student.gender == filters.gender)
        if filters.email:
            query = query.filter(sql_models.Student.email.ilike(f'%{filters.email}%'))
        if filters.status:
            query = query.filter(sql_models.Student.status == filters.status)
    
    students = query.all()
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

# Filter teachers
@app.post("/teachers/filter", response_model=List[TeacherModel])
def filter_teachers(
    filters: Optional[TeacherFilter] = None,
    db: Session = Depends(get_db)
):
    """
    Get teachers with optional filters.
    If no filters are provided, returns all teachers.
    """
    query = db.query(sql_models.Teacher)
    
    # Apply filters if provided
    if filters:
        if filters.teacher_id:
            query = query.filter(sql_models.Teacher.teacher_id == filters.teacher_id)
        if filters.name:
            query = query.filter(sql_models.Teacher.name.ilike(f'%{filters.name}%'))
        if filters.gender:
            query = query.filter(sql_models.Teacher.gender == filters.gender)
        if filters.email:
            query = query.filter(sql_models.Teacher.email.ilike(f'%{filters.email}%'))
        if filters.status:
            query = query.filter(sql_models.Teacher.status == filters.status)
    
    teachers = query.all()
    return teachers

# Create teacher
@app.post("/teachers", response_model=TeacherModel, status_code=201)
def create_teacher(teacher: TeacherCreate, db: Session = Depends(get_db)):
    """
    Create a new teacher in the database
    """
    # Check if email already exists
    db_teacher = db.query(sql_models.Teacher).filter(sql_models.Teacher.email == teacher.email).first()
    if db_teacher:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new teacher object
    new_teacher = sql_models.Teacher(
        teacher_id=str(uuid.uuid4()),
        name=teacher.name,
        gender=teacher.gender,
        phone=teacher.phone,
        email=teacher.email,
        status=teacher.status,
        profile_pic=teacher.profile_pic,
        address=teacher.address,
        password_hash=pwd_context.hash(teacher.password),
        date_of_birth=teacher.date_of_birth
    )
    
    # Add to database
    try:
        db.add(new_teacher)
        db.commit()
        db.refresh(new_teacher)
        return new_teacher
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create teacher: {str(e)}")

# Filter classes
@app.post("/classes/filter", response_model=List[ClassModel])
def filter_classes(
    filters: Optional[ClassFilter] = None,
    db: Session = Depends(get_db)
):
    """
    Get classes with optional filters.
    If no filters are provided, returns all classes.
    """
    query = db.query(sql_models.Class)
    
    # Apply filters if provided
    if filters:
        if filters.class_id:
            query = query.filter(sql_models.Class.class_id == filters.class_id)
        if filters.class_number:
            query = query.filter(sql_models.Class.class_number == filters.class_number)
        if filters.section:
            query = query.filter(sql_models.Class.section == filters.section)
        if filters.class_teacher_id:
            query = query.filter(sql_models.Class.class_teacher_id == filters.class_teacher_id)
    
    classes = query.all()
    return classes

# Create class
@app.post("/classes", response_model=ClassModel, status_code=201)
def create_class(class_data: ClassCreate, db: Session = Depends(get_db)):
    """
    Create a new class in the database
    """
    # Check if teacher exists
    teacher = db.query(sql_models.Teacher).filter(sql_models.Teacher.teacher_id == class_data.class_teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    # Check if class with same number and section already exists
    existing_class = db.query(sql_models.Class).filter(
        sql_models.Class.class_number == class_data.class_number,
        sql_models.Class.section == class_data.section
    ).first()
    
    if existing_class:
        raise HTTPException(status_code=400, detail=f"Class {class_data.class_number}-{class_data.section} already exists")
    
    # Create new class
    new_class = sql_models.Class(
        class_id=str(uuid.uuid4()),
        class_number=class_data.class_number,
        section=class_data.section,
        class_teacher_id=class_data.class_teacher_id
    )
    
    try:
        db.add(new_class)
        db.commit()
        db.refresh(new_class)
        return new_class
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create class: {str(e)}")

# Filter subjects
@app.post("/subjects/filter", response_model=List[SubjectModel])
def filter_subjects(
    filters: Optional[SubjectFilter] = None,
    db: Session = Depends(get_db)
):
    """
    Get subjects with optional filters.
    If no filters are provided, returns all subjects.
    """
    query = db.query(sql_models.Subject)
    
    # Apply filters if provided
    if filters:
        if filters.subject_id:
            query = query.filter(sql_models.Subject.subject_id == filters.subject_id)
        if filters.name:
            query = query.filter(sql_models.Subject.name.ilike(f'%{filters.name}%'))
        if filters.code:
            query = query.filter(sql_models.Subject.code == filters.code)
    
    subjects = query.all()
    return subjects

# Create subject
@app.post("/subjects", response_model=SubjectModel, status_code=201)
def create_subject(subject: SubjectCreate, db: Session = Depends(get_db)):
    """
    Create a new subject in the database
    """
    # Check if subject with same code already exists
    existing_subject = db.query(sql_models.Subject).filter(sql_models.Subject.code == subject.code).first()
    if existing_subject:
        raise HTTPException(status_code=400, detail=f"Subject with code {subject.code} already exists")
    
    # Create new subject
    new_subject = sql_models.Subject(
        subject_id=str(uuid.uuid4()),
        name=subject.name,
        code=subject.code
    )
    
    try:
        db.add(new_subject)
        db.commit()
        db.refresh(new_subject)
        return new_subject
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create subject: {str(e)}")

# Filter attendance
@app.post("/attendance/filter", response_model=List[AttendanceModel])
def filter_attendance(
    filters: Optional[AttendanceFilter] = None,
    db: Session = Depends(get_db)
):
    """
    Get attendance records with optional filters.
    If no filters are provided, returns all attendance records.
    """
    query = db.query(sql_models.Attendance)
    
    # Apply filters if provided
    if filters:
        if filters.attendance_id:
            query = query.filter(sql_models.Attendance.attendance_id == filters.attendance_id)
        if filters.class_id:
            query = query.filter(sql_models.Attendance.class_id == filters.class_id)
        if filters.student_id:
            query = query.filter(sql_models.Attendance.student_id == filters.student_id)
        if filters.date:
            query = query.filter(sql_models.Attendance.date == filters.date)
        if filters.date_from:
            query = query.filter(sql_models.Attendance.date >= filters.date_from)
        if filters.date_to:
            query = query.filter(sql_models.Attendance.date <= filters.date_to)
        if filters.status:
            query = query.filter(sql_models.Attendance.status == filters.status)
    
    attendance_records = query.all()
    return attendance_records

# Create attendance record
@app.post("/attendance", response_model=AttendanceModel, status_code=201)
def create_attendance(attendance: AttendanceCreate, db: Session = Depends(get_db)):
    """
    Create a new attendance record in the database
    """
    # Check if class exists
    class_check = db.query(sql_models.Class).filter(sql_models.Class.class_id == attendance.class_id).first()
    if not class_check:
        raise HTTPException(status_code=404, detail="Class not found")
    
    # Check if student exists and belongs to the class
    student_check = db.query(sql_models.Student).filter(
        sql_models.Student.student_id == attendance.student_id,
        sql_models.Student.class_id == attendance.class_id
    ).first()
    if not student_check:
        raise HTTPException(status_code=404, detail="Student not found in this class")
    
    # Check if attendance record for this student on this date already exists
    existing_attendance = db.query(sql_models.Attendance).filter(
        sql_models.Attendance.student_id == attendance.student_id,
        sql_models.Attendance.date == attendance.date
    ).first()
    if existing_attendance:
        raise HTTPException(status_code=400, detail="Attendance record for this student on this date already exists")
    
    # Create new attendance record
    new_attendance = sql_models.Attendance(
        attendance_id=str(uuid.uuid4()),
        class_id=attendance.class_id,
        student_id=attendance.student_id,
        date=attendance.date,
        status=attendance.status
    )
    
    try:
        db.add(new_attendance)
        db.commit()
        db.refresh(new_attendance)
        return new_attendance
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create attendance record: {str(e)}")

# Filter exams
@app.post("/exams/filter", response_model=List[ExamsModel])
def filter_exams(
    filters: Optional[ExamFilter] = None,
    db: Session = Depends(get_db)
):
    """
    Get exams with optional filters.
    If no filters are provided, returns all exams.
    """
    query = db.query(sql_models.Exams)
    
    # Apply filters if provided
    if filters:
        if filters.exam_id:
            query = query.filter(sql_models.Exams.exam_id == filters.exam_id)
        if filters.class_id:
            query = query.filter(sql_models.Exams.class_id == filters.class_id)
        if filters.subject_id:
            query = query.filter(sql_models.Exams.subject_id == filters.subject_id)
        if filters.name:
            query = query.filter(sql_models.Exams.name.ilike(f'%{filters.name}%'))
        if filters.date:
            query = query.filter(sql_models.Exams.date == filters.date)
        if filters.date_from:
            query = query.filter(sql_models.Exams.date >= filters.date_from)
        if filters.date_to:
            query = query.filter(sql_models.Exams.date <= filters.date_to)
    
    exams = query.all()
    return exams

# Create exam
@app.post("/exams", response_model=ExamsModel, status_code=201)
def create_exam(exam: ExamsCreate, db: Session = Depends(get_db)):
    """
    Create a new exam in the database
    """
    # Validate class exists
    class_check = db.query(sql_models.Class).filter(sql_models.Class.class_id == exam.class_id).first()
    if not class_check:
        raise HTTPException(status_code=404, detail="Class not found")
    
    # Validate subject exists
    subject_check = db.query(sql_models.Subject).filter(sql_models.Subject.subject_id == exam.subject_id).first()
    if not subject_check:
        raise HTTPException(status_code=404, detail="Subject not found")
    
    # Create new exam
    new_exam = sql_models.Exams(
        exam_id=str(uuid.uuid4()),
        class_id=exam.class_id,
        subject_id=exam.subject_id,
        date=exam.date,
        name=exam.name,
        total_marks=exam.total_marks
    )
    
    try:
        db.add(new_exam)
        db.commit()
        db.refresh(new_exam)
        return new_exam
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create exam: {str(e)}")

# Create grade
@app.post("/grades", response_model=GradeModel, status_code=201)
def create_grade(grade: GradeCreate, db: Session = Depends(get_db)):
    """
    Create a new grade in the database
    """
    # Validate student exists
    student_check = db.query(sql_models.Student).filter(sql_models.Student.student_id == grade.student_id).first()
    if not student_check:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Validate exam exists
    exam_check = db.query(sql_models.Exams).filter(sql_models.Exams.exam_id == grade.exam_id).first()
    if not exam_check:
        raise HTTPException(status_code=404, detail="Exam not found")
    
    # Check if marks exceed total marks
    if grade.marks > exam_check.total_marks:
        raise HTTPException(status_code=400, detail=f"Marks cannot exceed total marks for the exam ({exam_check.total_marks})")
    
    # Check if grade already exists for this student and exam
    existing_grade = db.query(sql_models.Grade).filter(
        sql_models.Grade.student_id == grade.student_id,
        sql_models.Grade.exam_id == grade.exam_id
    ).first()
    if existing_grade:
        raise HTTPException(status_code=400, detail="Grade already exists for this student and exam")
    
    # Create new grade
    new_grade = sql_models.Grade(
        grades_id=str(uuid.uuid4()),
        student_id=grade.student_id,
        exam_id=grade.exam_id,
        marks=grade.marks,
        grade=grade.grade
    )
    
    try:
        db.add(new_grade)
        db.commit()
        db.refresh(new_grade)
        return new_grade
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create grade: {str(e)}")

# Create assignment
@app.post("/assignments", response_model=AssignmentModel, status_code=201)
def create_assignment(assignment: AssignmentCreate, db: Session = Depends(get_db)):
    """
    Create a new assignment in the database
    """
    # Validate class_subject exists
    class_sub_check = db.query(sql_models.Class_Subject).filter(sql_models.Class_Subject.class_sub_id == assignment.class_sub_id).first()
    if not class_sub_check:
        raise HTTPException(status_code=404, detail="Class subject relation not found")
    
    # Create new assignment
    new_assignment = sql_models.Assignment(
        assignment_id=str(uuid.uuid4()),
        class_sub_id=assignment.class_sub_id,
        title=assignment.title,
        dueDate=assignment.dueDate,
        description=assignment.description,
        type=assignment.type
    )
    
    try:
        db.add(new_assignment)
        db.commit()
        db.refresh(new_assignment)
        return new_assignment
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create assignment: {str(e)}")

# Create assignment grading
@app.post("/assignments/grading", response_model=Assignment_gradingModel, status_code=201)
def create_assignment_grading(grading: Assignment_gradingCreate, db: Session = Depends(get_db)):
    """
    Create a new assignment grading in the database
    """
    # Validate assignment exists
    assignment_check = db.query(sql_models.Assignment).filter(sql_models.Assignment.assignment_id == grading.assignment_id).first()
    if not assignment_check:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    # Validate student exists
    student_check = db.query(sql_models.Student).filter(sql_models.Student.student_id == grading.student_id).first()
    if not student_check:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Check if grading already exists for this student and assignment
    existing_grading = db.query(sql_models.Assignment_grading).filter(
        sql_models.Assignment_grading.student_id == grading.student_id,
        sql_models.Assignment_grading.assignment_id == grading.assignment_id
    ).first()
    if existing_grading:
        raise HTTPException(status_code=400, detail="Grading already exists for this student and assignment")
    
    # Create new assignment grading
    new_grading = sql_models.Assignment_grading(
        grading_id=str(uuid.uuid4()),
        assignment_id=grading.assignment_id,
        student_id=grading.student_id,
        feedback=grading.feedback,
        grade=grading.grade,
        marks=grading.marks,
        graded_at=datetime.now()
    )
    
    try:
        db.add(new_grading)
        db.commit()
        db.refresh(new_grading)
        return new_grading
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create assignment grading: {str(e)}")

# Create admin
@app.post("/admins", response_model=AdminModel, status_code=201)
def create_admin(admin: AdminCreate, db: Session = Depends(get_db)):
    """
    Create a new admin in the database
    """
    # Check if email already exists
    db_admin = db.query(sql_models.Admin).filter(sql_models.Admin.email == admin.email).first()
    if db_admin:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new admin
    new_admin = sql_models.Admin(
        admin_id=str(uuid.uuid4()),
        name=admin.name,
        gender=admin.gender,
        phone=admin.phone,
        email=admin.email,
        status=admin.status,
        profile_pic=admin.profile_pic,
        address=admin.address,
        password_hash=pwd_context.hash(admin.password),
        date_of_birth=admin.date_of_birth
    )
    
    try:
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)
        return new_admin
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create admin: {str(e)}")

# Create class subject relation
@app.post("/class-subjects", response_model=Class_SubjectModel, status_code=201)
def create_class_subject(class_subject: Class_SubjectCreate, db: Session = Depends(get_db)):
    """
    Create a new class subject relation in the database
    """
    # Validate class exists
    class_check = db.query(sql_models.Class).filter(sql_models.Class.class_id == class_subject.class_id).first()
    if not class_check:
        raise HTTPException(status_code=404, detail="Class not found")
    
    # Validate subject exists
    subject_check = db.query(sql_models.Subject).filter(sql_models.Subject.subject_id == class_subject.subject_id).first()
    if not subject_check:
        raise HTTPException(status_code=404, detail="Subject not found")
    
    # Validate teacher exists
    teacher_check = db.query(sql_models.Teacher).filter(sql_models.Teacher.teacher_id == class_subject.subject_teacher_id).first()
    if not teacher_check:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    # Check if class subject relation already exists
    existing_relation = db.query(sql_models.Class_Subject).filter(
        sql_models.Class_Subject.class_id == class_subject.class_id,
        sql_models.Class_Subject.subject_id == class_subject.subject_id
    ).first()
    if existing_relation:
        raise HTTPException(status_code=400, detail="Class subject relation already exists")
    
    # Create new class subject relation
    new_class_subject = sql_models.Class_Subject(
        class_sub_id=str(uuid.uuid4()),
        class_id=class_subject.class_id,
        subject_id=class_subject.subject_id,
        subject_teacher_id=class_subject.subject_teacher_id
    )
    
    try:
        db.add(new_class_subject)
        db.commit()
        db.refresh(new_class_subject)
        return new_class_subject
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create class subject relation: {str(e)}")

# Create timetable entry
@app.post("/timetable", response_model=TimetableModel, status_code=201)
def create_timetable_entry(timetable: TimetableCreate, db: Session = Depends(get_db)):
    """
    Create a new timetable entry in the database
    """
    # Validate class subject relation exists
    class_sub_check = db.query(sql_models.Class_Subject).filter(sql_models.Class_Subject.class_sub_id == timetable.class_sub_id).first()
    if not class_sub_check:
        raise HTTPException(status_code=404, detail="Class subject relation not found")
    
    # Check for time slot conflicts for the same class on the same day
    class_id = class_sub_check.class_id
    
    # Get all timetable entries for this class on the same day
    conflicting_slots = db.query(sql_models.Timetable).join(
        sql_models.Class_Subject, sql_models.Class_Subject.class_sub_id == sql_models.Timetable.class_sub_id
    ).filter(
        sql_models.Class_Subject.class_id == class_id,
        sql_models.Timetable.day == timetable.day
    ).all()
    
    # Check for time conflicts
    for slot in conflicting_slots:
        # Overlap check: if the new entry starts during an existing slot or ends during an existing slot
        if ((timetable.start_time >= slot.start_time and timetable.start_time < slot.end_time) or
            (timetable.end_time > slot.start_time and timetable.end_time <= slot.end_time) or
            (timetable.start_time <= slot.start_time and timetable.end_time >= slot.end_time)):
            raise HTTPException(status_code=400, detail="Time slot conflicts with an existing entry")
    
    # Create new timetable entry
    new_timetable = sql_models.Timetable(
        timetable_id=str(uuid.uuid4()),
        class_sub_id=timetable.class_sub_id,
        day=timetable.day,
        start_time=timetable.start_time,
        end_time=timetable.end_time
    )
    
    try:
        db.add(new_timetable)
        db.commit()
        db.refresh(new_timetable)
        return new_timetable
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create timetable entry: {str(e)}")

# Create notification
@app.post("/notifications", response_model=NotificationModel, status_code=201)
def create_notification(notification: NotificationCreate, db: Session = Depends(get_db)):
    """
    Create a new notification in the database
    """
    # Validate class ID if recipient is specific class
    if notification.recipient == 'Specific Class':
        class_check = db.query(sql_models.Class).filter(sql_models.Class.class_id == notification.class_id).first()
        if not class_check:
            raise HTTPException(status_code=404, detail="Class not found")
    
    # Validate admin/teacher based on creator type
    if notification.creator_type == 'Admin' and notification.admin_id:
        admin_check = db.query(sql_models.Admin).filter(sql_models.Admin.admin_id == notification.admin_id).first()
        if not admin_check:
            raise HTTPException(status_code=404, detail="Admin not found")
    elif notification.creator_type == 'Teacher' and notification.teacher_id:
        teacher_check = db.query(sql_models.Teacher).filter(sql_models.Teacher.teacher_id == notification.teacher_id).first()
        if not teacher_check:
            raise HTTPException(status_code=404, detail="Teacher not found")
    
    # Create new notification
    new_notification = sql_models.Notification(
        notification_id=str(uuid.uuid4()),
        title=notification.title,
        content=notification.content,
        type=notification.type,
        recipient=notification.recipient,
        class_id=notification.class_id,
        creator_type=notification.creator_type,
        admin_id=notification.admin_id,
        teacher_id=notification.teacher_id
    )
    
    try:
        db.add(new_notification)
        db.commit()
        db.refresh(new_notification)
        return new_notification
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create notification: {str(e)}")

# Create leave application
@app.post("/leave-applications", response_model=LeaveApplicationModel, status_code=201)
def create_leave_application(leave: LeaveApplicationCreate, db: Session = Depends(get_db)):
    """
    Create a new leave application in the database
    """
    # Validate student exists
    student_check = db.query(sql_models.Student).filter(sql_models.Student.student_id == leave.student_id).first()
    if not student_check:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Create new leave application
    new_leave = sql_models.Leave_Application(
        leave_id=str(uuid.uuid4()),
        student_id=leave.student_id,
        title=leave.title,
        type=leave.type,
        start_date=leave.start_date,
        end_date=leave.end_date,
        reason=leave.reason,
        applied_at=datetime.now()
    )
    
    try:
        db.add(new_leave)
        db.commit()
        db.refresh(new_leave)
        return new_leave
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create leave application: {str(e)}")

# Create feedback
@app.post("/feedback", response_model=FeedbackModel, status_code=201)
def create_feedback(feedback: FeedbackCreate, db: Session = Depends(get_db)):
    """
    Create a new feedback in the database
    """
    # Validate student exists
    student_check = db.query(sql_models.Student).filter(sql_models.Student.student_id == feedback.student_id).first()
    if not student_check:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Validate teacher exists
    teacher_check = db.query(sql_models.Teacher).filter(sql_models.Teacher.teacher_id == feedback.teacher_id).first()
    if not teacher_check:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    # Create new feedback
    new_feedback = sql_models.Feedback(
        feedback_id=str(uuid.uuid4()),
        student_id=feedback.student_id,
        teacher_id=feedback.teacher_id,
        title=feedback.title,
        feedback_type=feedback.feedback_type,
        feedback_text=feedback.feedback_text,
        given_at=datetime.now()
    )
    
    try:
        db.add(new_feedback)
        db.commit()
        db.refresh(new_feedback)
        return new_feedback
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create feedback: {str(e)}")

# Create extra credit
@app.post("/extra-credits", response_model=Extra_CreditModel, status_code=201)
def create_extra_credit(extra_credit: ExtraCreditCreate, db: Session = Depends(get_db)):
    """
    Create a new extra credit in the database
    """
    # Validate student exists
    student_check = db.query(sql_models.Student).filter(sql_models.Student.student_id == extra_credit.student_id).first()
    if not student_check:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Validate admin exists
    admin_check = db.query(sql_models.Admin).filter(sql_models.Admin.admin_id == extra_credit.admin_id).first()
    if not admin_check:
        raise HTTPException(status_code=404, detail="Admin not found")
    
    # Create new extra credit
    new_extra_credit = sql_models.Extra_Credit(
        credit_id=str(uuid.uuid4()),
        student_id=extra_credit.student_id,
        admin_id=extra_credit.admin_id,
        grade=extra_credit.grade
    )
    
    try:
        db.add(new_extra_credit)
        db.commit()
        db.refresh(new_extra_credit)
        return new_extra_credit
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create extra credit: {str(e)}")

# Create lost and found item
@app.post("/lost-found", response_model=Lost_and_FoundModel, status_code=201)
def create_lost_found(item: LostAndFoundCreate, db: Session = Depends(get_db)):
    """
    Create a new lost and found item in the database
    """
    # Validate admin exists
    admin_check = db.query(sql_models.Admin).filter(sql_models.Admin.admin_id == item.admin_id).first()
    if not admin_check:
        raise HTTPException(status_code=404, detail="Admin not found")
    
    # Create new lost and found item
    new_item = sql_models.Lost_and_Found(
        unique_id=str(uuid.uuid4()),
        admin_id=item.admin_id,
        item_name=item.item_name,
        description=item.description,
        location=item.location,
        date_reported=date.today(),
        status=item.status
    )
    
    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create lost and found item: {str(e)}")

# Update routes for entities

# Update student
@app.put("/students/{student_id}", response_model=StudentModel)
def update_student(
    student_id: str,
    student_update: StudentUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a student by ID
    """
    # Check if student exists
    db_student = db.query(sql_models.Student).filter(sql_models.Student.student_id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Email validation
    if student_update.email is not None:
        existing_email = db.query(sql_models.Student).filter(
            sql_models.Student.email == student_update.email,
            sql_models.Student.student_id != student_id
        ).first()
        if existing_email:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    # Class validation
    if student_update.class_id is not None:
        class_check = db.query(sql_models.Class).filter(sql_models.Class.class_id == student_update.class_id).first()
        if not class_check:
            raise HTTPException(status_code=404, detail="Class not found")
    
    # Roll number validation
    if student_update.roll_no is not None and student_update.class_id is not None:
        roll_check = db.query(sql_models.Student).filter(
            sql_models.Student.class_id == student_update.class_id,
            sql_models.Student.roll_no == student_update.roll_no,
            sql_models.Student.student_id != student_id
        ).first()
        if roll_check:
            raise HTTPException(status_code=400, detail="Roll number already exists in this class")
    elif student_update.roll_no is not None and db_student.class_id is not None:
        roll_check = db.query(sql_models.Student).filter(
            sql_models.Student.class_id == db_student.class_id,
            sql_models.Student.roll_no == student_update.roll_no,
            sql_models.Student.student_id != student_id
        ).first()
        if roll_check:
            raise HTTPException(status_code=400, detail="Roll number already exists in this class")
    
    # Update student attributes
    update_data = student_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_student, key, value)
    
    try:
        db.commit()
        db.refresh(db_student)
        return db_student
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update student: {str(e)}")

# Update teacher
@app.put("/teachers/{teacher_id}", response_model=TeacherModel)
def update_teacher(
    teacher_id: str,
    teacher_update: TeacherUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a teacher by ID
    """
    # Check if teacher exists
    db_teacher = db.query(sql_models.Teacher).filter(sql_models.Teacher.teacher_id == teacher_id).first()
    if not db_teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    # Email validation
    if teacher_update.email is not None:
        existing_email = db.query(sql_models.Teacher).filter(
            sql_models.Teacher.email == teacher_update.email,
            sql_models.Teacher.teacher_id != teacher_id
        ).first()
        if existing_email:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    # Update teacher attributes
    update_data = teacher_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_teacher, key, value)
    
    try:
        db.commit()
        db.refresh(db_teacher)
        return db_teacher
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update teacher: {str(e)}")

# Update class
@app.put("/classes/{class_id}", response_model=ClassModel)
def update_class(
    class_id: str,
    class_update: ClassUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a class by ID
    """
    # Check if class exists
    db_class = db.query(sql_models.Class).filter(sql_models.Class.class_id == class_id).first()
    if not db_class:
        raise HTTPException(status_code=404, detail="Class not found")
    
    # Teacher validation
    if class_update.class_teacher_id is not None:
        teacher_check = db.query(sql_models.Teacher).filter(
            sql_models.Teacher.teacher_id == class_update.class_teacher_id
        ).first()
        if not teacher_check:
            raise HTTPException(status_code=404, detail="Teacher not found")
    
    # Class number and section validation
    if (class_update.class_number is not None or class_update.section is not None):
        new_class_number = class_update.class_number if class_update.class_number is not None else db_class.class_number
        new_section = class_update.section if class_update.section is not None else db_class.section
        
        existing_class = db.query(sql_models.Class).filter(
            sql_models.Class.class_number == new_class_number,
            sql_models.Class.section == new_section,
            sql_models.Class.class_id != class_id
        ).first()
        
        if existing_class:
            raise HTTPException(
                status_code=400,
                detail=f"Class {new_class_number}-{new_section} already exists"
            )
    
    # Update class attributes
    update_data = class_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        # Handle the special case of 'class_teacher_id'
        # It's class_teacher in the model but class_teacher_id in update schema
        if key == 'class_teacher_id':
            setattr(db_class, key, value)
        else:
            setattr(db_class, key, value)
    
    try:
        db.commit()
        db.refresh(db_class)
        return db_class
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update class: {str(e)}")

# Update subject
@app.put("/subjects/{subject_id}", response_model=SubjectModel)
def update_subject(
    subject_id: str,
    subject_update: SubjectUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a subject by ID
    """
    # Check if subject exists
    db_subject = db.query(sql_models.Subject).filter(sql_models.Subject.subject_id == subject_id).first()
    if not db_subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    
    # Code validation
    if subject_update.code is not None:
        existing_code = db.query(sql_models.Subject).filter(
            sql_models.Subject.code == subject_update.code,
            sql_models.Subject.subject_id != subject_id
        ).first()
        if existing_code:
            raise HTTPException(status_code=400, detail=f"Subject with code {subject_update.code} already exists")
    
    # Update subject attributes
    update_data = subject_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_subject, key, value)
    
    try:
        db.commit()
        db.refresh(db_subject)
        return db_subject
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update subject: {str(e)}")

# Update attendance record
@app.put("/attendance/{attendance_id}", response_model=AttendanceModel)
def update_attendance(
    attendance_id: str,
    attendance_update: AttendanceUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an attendance record by ID
    """
    # Check if attendance record exists
    db_attendance = db.query(sql_models.Attendance).filter(sql_models.Attendance.attendance_id == attendance_id).first()
    if not db_attendance:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    
    # Update attendance attributes
    update_data = attendance_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_attendance, key, value)
    
    try:
        db.commit()
        db.refresh(db_attendance)
        return db_attendance
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update attendance: {str(e)}")

# Update timetable entry
@app.put("/timetable/{timetable_id}", response_model=TimetableModel)
def update_timetable(
    timetable_id: str,
    timetable_update: TimetableUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a timetable entry by ID
    """
    # Check if timetable entry exists
    db_timetable = db.query(sql_models.Timetable).filter(sql_models.Timetable.timetable_id == timetable_id).first()
    if not db_timetable:
        raise HTTPException(status_code=404, detail="Timetable entry not found")
    
    # Get the class_id for conflict checking
    class_sub = db.query(sql_models.Class_Subject).filter(
        sql_models.Class_Subject.class_sub_id == db_timetable.class_sub_id
    ).first()
    class_id = class_sub.class_id if class_sub else None
    
    if class_id:
        # Check for time conflicts if day, start_time, or end_time is updated
        if timetable_update.day is not None or timetable_update.start_time is not None or timetable_update.end_time is not None:
            new_day = timetable_update.day if timetable_update.day is not None else db_timetable.day
            new_start_time = timetable_update.start_time if timetable_update.start_time is not None else db_timetable.start_time
            new_end_time = timetable_update.end_time if timetable_update.end_time is not None else db_timetable.end_time
            
            # Find potentially conflicting slots for the same class on the same day
            conflicting_slots = db.query(sql_models.Timetable).join(
                sql_models.Class_Subject, 
                sql_models.Class_Subject.class_sub_id == sql_models.Timetable.class_sub_id
            ).filter(
                sql_models.Class_Subject.class_id == class_id,
                sql_models.Timetable.day == new_day,
                sql_models.Timetable.timetable_id != timetable_id
            ).all()
            
            # Check for overlapping time slots
            for slot in conflicting_slots:
                if ((new_start_time >= slot.start_time and new_start_time < slot.end_time) or
                    (new_end_time > slot.start_time and new_end_time <= slot.end_time) or
                    (new_start_time <= slot.start_time and new_end_time >= slot.end_time)):
                    raise HTTPException(status_code=400, detail="Time slot conflicts with an existing entry")
    
    # Update timetable attributes
    update_data = timetable_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_timetable, key, value)
    
    try:
        db.commit()
        db.refresh(db_timetable)
        return db_timetable
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update timetable: {str(e)}")

# Update exam
@app.put("/exams/{exam_id}", response_model=ExamsModel)
def update_exam(
    exam_id: str,
    exam_update: ExamUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an exam by ID
    """
    # Check if exam exists
    db_exam = db.query(sql_models.Exams).filter(sql_models.Exams.exam_id == exam_id).first()
    if not db_exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    
    # Update exam attributes
    update_data = exam_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_exam, key, value)
    
    try:
        db.commit()
        db.refresh(db_exam)
        return db_exam
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update exam: {str(e)}")

# Update grade
@app.put("/grades/{grade_id}", response_model=GradeModel)
def update_grade(
    grade_id: str,
    grade_update: GradeUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a grade by ID
    """
    # Check if grade exists
    db_grade = db.query(sql_models.Grade).filter(sql_models.Grade.grades_id == grade_id).first()
    if not db_grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    
    # Validate marks against total marks
    if grade_update.marks is not None:
        exam = db.query(sql_models.Exams).filter(sql_models.Exams.exam_id == db_grade.exam_id).first()
        if exam and grade_update.marks > exam.total_marks:
            raise HTTPException(status_code=400, detail=f"Marks cannot exceed total marks for the exam ({exam.total_marks})")
    
    # Update grade attributes
    update_data = grade_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_grade, key, value)
    
    try:
        db.commit()
        db.refresh(db_grade)
        return db_grade
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update grade: {str(e)}")

# Update assignment
@app.put("/assignments/{assignment_id}", response_model=AssignmentModel)
def update_assignment(
    assignment_id: str,
    assignment_update: AssignmentUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an assignment by ID
    """
    # Check if assignment exists
    db_assignment = db.query(sql_models.Assignment).filter(sql_models.Assignment.assignment_id == assignment_id).first()
    if not db_assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    # Update assignment attributes
    update_data = assignment_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_assignment, key, value)
    
    try:
        db.commit()
        db.refresh(db_assignment)
        return db_assignment
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update assignment: {str(e)}")

# Update assignment grading
@app.put("/assignments/grading/{grading_id}", response_model=Assignment_gradingModel)
def update_assignment_grading(
    grading_id: str,
    grading_update: AssignmentGradingUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an assignment grading by ID
    """
    # Check if grading exists
    db_grading = db.query(sql_models.Assignment_grading).filter(sql_models.Assignment_grading.grading_id == grading_id).first()
    if not db_grading:
        raise HTTPException(status_code=404, detail="Assignment grading not found")
    
    # Update grading attributes and set graded_at to current time
    update_data = grading_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_grading, key, value)
    
    # Update the graded_at timestamp
    db_grading.graded_at = datetime.now()
    
    try:
        db.commit()
        db.refresh(db_grading)
        return db_grading
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update assignment grading: {str(e)}")

# Update notification
@app.put("/notifications/{notification_id}", response_model=NotificationModel)
def update_notification(
    notification_id: str,
    notification_update: NotificationUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a notification by ID
    """
    # Check if notification exists
    db_notification = db.query(sql_models.Notification).filter(sql_models.Notification.notification_id == notification_id).first()
    if not db_notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    # Update notification attributes
    update_data = notification_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_notification, key, value)
    
    try:
        db.commit()
        db.refresh(db_notification)
        return db_notification
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update notification: {str(e)}")

# Update leave application
@app.put("/leave-applications/{leave_id}", response_model=LeaveApplicationModel)
def update_leave_application(
    leave_id: str,
    leave_update: LeaveApplicationUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a leave application by ID
    """
    # Check if leave application exists
    db_leave = db.query(sql_models.Leave_Application).filter(sql_models.Leave_Application.leave_id == leave_id).first()
    if not db_leave:
        raise HTTPException(status_code=404, detail="Leave application not found")
    
    # Update leave application attributes
    update_data = leave_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_leave, key, value)
    
    try:
        db.commit()
        db.refresh(db_leave)
        return db_leave
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update leave application: {str(e)}")

# Update feedback
@app.put("/feedback/{feedback_id}", response_model=FeedbackModel)
def update_feedback(
    feedback_id: str,
    feedback_update: FeedbackUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a feedback by ID
    """
    # Check if feedback exists
    db_feedback = db.query(sql_models.Feedback).filter(sql_models.Feedback.feedback_id == feedback_id).first()
    if not db_feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    # Update feedback attributes
    update_data = feedback_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_feedback, key, value)
    
    try:
        db.commit()
        db.refresh(db_feedback)
        return db_feedback
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update feedback: {str(e)}")

# Update extra credit
@app.put("/extra-credits/{credit_id}", response_model=Extra_CreditModel)
def update_extra_credit(
    credit_id: str,
    extra_credit_update: ExtraCreditUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an extra credit by ID
    """
    # Check if extra credit exists
    db_extra_credit = db.query(sql_models.Extra_Credit).filter(sql_models.Extra_Credit.credit_id == credit_id).first()
    if not db_extra_credit:
        raise HTTPException(status_code=404, detail="Extra credit not found")
    
    # Update extra credit attributes
    update_data = extra_credit_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_extra_credit, key, value)
    
    try:
        db.commit()
        db.refresh(db_extra_credit)
        return db_extra_credit
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update extra credit: {str(e)}")

# Update lost and found item
@app.put("/lost-found/{item_id}", response_model=Lost_and_FoundModel)
def update_lost_found(
    item_id: str,
    item_update: LostAndFoundUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a lost and found item by ID
    """
    # Check if item exists
    db_item = db.query(sql_models.Lost_and_Found).filter(sql_models.Lost_and_Found.unique_id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Lost and found item not found")
    
    # Update item attributes
    update_data = item_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)
    
    try:
        db.commit()
        db.refresh(db_item)
        return db_item
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update lost and found item: {str(e)}")

# Update admin
@app.put("/admins/{admin_id}", response_model=AdminModel)
def update_admin(
    admin_id: str,
    admin_update: AdminUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an admin by ID
    """
    # Check if admin exists
    db_admin = db.query(sql_models.Admin).filter(sql_models.Admin.admin_id == admin_id).first()
    if not db_admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    
    # Email validation
    if admin_update.email is not None:
        existing_email = db.query(sql_models.Admin).filter(
            sql_models.Admin.email == admin_update.email,
            sql_models.Admin.admin_id != admin_id
        ).first()
        if existing_email:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    # Update admin attributes
    update_data = admin_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_admin, key, value)
    
    try:
        db.commit()
        db.refresh(db_admin)
        return db_admin
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update admin: {str(e)}")

# Delete routes for entities

# Delete student
@app.delete("/students/{student_id}", status_code=204)
def delete_student(
    student_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete a student by ID
    """
    # Check if student exists
    db_student = db.query(sql_models.Student).filter(sql_models.Student.student_id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    try:
        db.delete(db_student)
        db.commit()
        return None
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete student: {str(e)}")

# Delete teacher
@app.delete("/teachers/{teacher_id}", status_code=204)
def delete_teacher(
    teacher_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete a teacher by ID
    """
    # Check if teacher exists
    db_teacher = db.query(sql_models.Teacher).filter(sql_models.Teacher.teacher_id == teacher_id).first()
    if not db_teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    # Check if teacher is assigned as a class teacher
    class_teacher_check = db.query(sql_models.Class).filter(sql_models.Class.class_teacher_id == teacher_id).first()
    if class_teacher_check:
        raise HTTPException(status_code=400, detail="Cannot delete teacher who is assigned as a class teacher")
    
    # Check if teacher is assigned as a subject teacher
    subject_teacher_check = db.query(sql_models.Class_Subject).filter(sql_models.Class_Subject.subject_teacher_id == teacher_id).first()
    if subject_teacher_check:
        raise HTTPException(status_code=400, detail="Cannot delete teacher who is assigned as a subject teacher")
    
    try:
        db.delete(db_teacher)
        db.commit()
        return None
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete teacher: {str(e)}")

# Delete class
@app.delete("/classes/{class_id}", status_code=204)
def delete_class(
    class_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete a class by ID
    """
    # Check if class exists
    db_class = db.query(sql_models.Class).filter(sql_models.Class.class_id == class_id).first()
    if not db_class:
        raise HTTPException(status_code=404, detail="Class not found")
    
    # Check if class has students
    student_check = db.query(sql_models.Student).filter(sql_models.Student.class_id == class_id).first()
    if student_check:
        raise HTTPException(status_code=400, detail="Cannot delete class that has students")
    
    try:
        db.delete(db_class)
        db.commit()
        return None
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete class: {str(e)}")

# Delete subject
@app.delete("/subjects/{subject_id}", status_code=204)
def delete_subject(
    subject_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete a subject by ID
    """
    # Check if subject exists
    db_subject = db.query(sql_models.Subject).filter(sql_models.Subject.subject_id == subject_id).first()
    if not db_subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    
    # Check if subject is assigned to any class
    class_subject_check = db.query(sql_models.Class_Subject).filter(sql_models.Class_Subject.subject_id == subject_id).first()
    if class_subject_check:
        raise HTTPException(status_code=400, detail="Cannot delete subject that is assigned to a class")
    
    try:
        db.delete(db_subject)
        db.commit()
        return None
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete subject: {str(e)}")

# Delete attendance record
@app.delete("/attendance/{attendance_id}", status_code=204)
def delete_attendance(
    attendance_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete an attendance record by ID
    """
    # Check if attendance record exists
    db_attendance = db.query(sql_models.Attendance).filter(sql_models.Attendance.attendance_id == attendance_id).first()
    if not db_attendance:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    
    try:
        db.delete(db_attendance)
        db.commit()
        return None
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete attendance record: {str(e)}")

# Delete timetable entry
@app.delete("/timetable/{timetable_id}", status_code=204)
def delete_timetable(
    timetable_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete a timetable entry by ID
    """
    # Check if timetable entry exists
    db_timetable = db.query(sql_models.Timetable).filter(sql_models.Timetable.timetable_id == timetable_id).first()
    if not db_timetable:
        raise HTTPException(status_code=404, detail="Timetable entry not found")
    
    try:
        db.delete(db_timetable)
        db.commit()
        return None
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete timetable entry: {str(e)}")

# Delete exam
@app.delete("/exams/{exam_id}", status_code=204)
def delete_exam(
    exam_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete an exam by ID
    """
    # Check if exam exists
    db_exam = db.query(sql_models.Exams).filter(sql_models.Exams.exam_id == exam_id).first()
    if not db_exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    
    # Check if exam has grades
    grade_check = db.query(sql_models.Grade).filter(sql_models.Grade.exam_id == exam_id).first()
    if grade_check:
        raise HTTPException(status_code=400, detail="Cannot delete exam that has grades assigned")
    
    try:
        db.delete(db_exam)
        db.commit()
        return None
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete exam: {str(e)}")

# Delete grade
@app.delete("/grades/{grade_id}", status_code=204)
def delete_grade(
    grade_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete a grade by ID
    """
    # Check if grade exists
    db_grade = db.query(sql_models.Grade).filter(sql_models.Grade.grades_id == grade_id).first()
    if not db_grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    
    try:
        db.delete(db_grade)
        db.commit()
        return None
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete grade: {str(e)}")

# Delete assignment
@app.delete("/assignments/{assignment_id}", status_code=204)
def delete_assignment(
    assignment_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete an assignment by ID
    """
    # Check if assignment exists
    db_assignment = db.query(sql_models.Assignment).filter(sql_models.Assignment.assignment_id == assignment_id).first()
    if not db_assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    # Delete related gradings first
    try:
        db.query(sql_models.Assignment_grading).filter(
            sql_models.Assignment_grading.assignment_id == assignment_id
        ).delete(synchronize_session=False)
        
        db.delete(db_assignment)
        db.commit()
        return None
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete assignment: {str(e)}")

# Delete assignment grading
@app.delete("/assignments/grading/{grading_id}", status_code=204)
def delete_assignment_grading(
    grading_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete an assignment grading by ID
    """
    # Check if grading exists
    db_grading = db.query(sql_models.Assignment_grading).filter(sql_models.Assignment_grading.grading_id == grading_id).first()
    if not db_grading:
        raise HTTPException(status_code=404, detail="Assignment grading not found")
    
    try:
        db.delete(db_grading)
        db.commit()
        return None
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete assignment grading: {str(e)}")

# Delete admin
@app.delete("/admins/{admin_id}", status_code=204)
def delete_admin(
    admin_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete an admin by ID
    """
    # Check if admin exists
    db_admin = db.query(sql_models.Admin).filter(sql_models.Admin.admin_id == admin_id).first()
    if not db_admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    
    # Check if there are any dependencies
    notifications = db.query(sql_models.Notification).filter(sql_models.Notification.admin_id == admin_id).count()
    lost_found = db.query(sql_models.Lost_and_Found).filter(sql_models.Lost_and_Found.admin_id == admin_id).count()
    extra_credits = db.query(sql_models.Extra_Credit).filter(sql_models.Extra_Credit.admin_id == admin_id).count()
    
    if notifications > 0 or lost_found > 0 or extra_credits > 0:
        raise HTTPException(
            status_code=400, 
            detail="Cannot delete admin with existing notifications, lost and found items, or extra credits"
        )
    
    try:
        db.delete(db_admin)
        db.commit()
        return None
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete admin: {str(e)}")

# Delete class subject relation
@app.delete("/class-subjects/{class_sub_id}", status_code=204)
def delete_class_subject(
    class_sub_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete a class subject relation by ID
    """
    # Check if class subject relation exists
    db_class_subject = db.query(sql_models.Class_Subject).filter(sql_models.Class_Subject.class_sub_id == class_sub_id).first()
    if not db_class_subject:
        raise HTTPException(status_code=404, detail="Class subject relation not found")
    
    # Check for dependencies: timetable entries, assignments
    timetable_check = db.query(sql_models.Timetable).filter(sql_models.Timetable.class_sub_id == class_sub_id).first()
    if timetable_check:
        raise HTTPException(status_code=400, detail="Cannot delete class subject relation with timetable entries")
    
    assignment_check = db.query(sql_models.Assignment).filter(sql_models.Assignment.class_sub_id == class_sub_id).first()
    if assignment_check:
        raise HTTPException(status_code=400, detail="Cannot delete class subject relation with assignments")
    
    try:
        db.delete(db_class_subject)
        db.commit()
        return None
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete class subject relation: {str(e)}")

# Delete notification
@app.delete("/notifications/{notification_id}", status_code=204)
def delete_notification(
    notification_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete a notification by ID
    """
    # Check if notification exists
    db_notification = db.query(sql_models.Notification).filter(sql_models.Notification.notification_id == notification_id).first()
    if not db_notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    try:
        db.delete(db_notification)
        db.commit()
        return None
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete notification: {str(e)}")

# Delete leave application
@app.delete("/leave-applications/{leave_id}", status_code=204)
def delete_leave_application(
    leave_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete a leave application by ID
    """
    # Check if leave application exists
    db_leave = db.query(sql_models.Leave_Application).filter(sql_models.Leave_Application.leave_id == leave_id).first()
    if not db_leave:
        raise HTTPException(status_code=404, detail="Leave application not found")
    
    try:
        db.delete(db_leave)
        db.commit()
        return None
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete leave application: {str(e)}")

# Delete feedback
@app.delete("/feedback/{feedback_id}", status_code=204)
def delete_feedback(
    feedback_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete a feedback by ID
    """
    # Check if feedback exists
    db_feedback = db.query(sql_models.Feedback).filter(sql_models.Feedback.feedback_id == feedback_id).first()
    if not db_feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    try:
        db.delete(db_feedback)
        db.commit()
        return None
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete feedback: {str(e)}")

# Delete extra credit
@app.delete("/extra-credits/{credit_id}", status_code=204)
def delete_extra_credit(
    credit_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete an extra credit by ID
    """
    # Check if extra credit exists
    db_extra_credit = db.query(sql_models.Extra_Credit).filter(sql_models.Extra_Credit.credit_id == credit_id).first()
    if not db_extra_credit:
        raise HTTPException(status_code=404, detail="Extra credit not found")
    
    try:
        db.delete(db_extra_credit)
        db.commit()
        return None
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete extra credit: {str(e)}")

# Delete lost and found item
@app.delete("/lost-found/{item_id}", status_code=204)
def delete_lost_found(
    item_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete a lost and found item by ID
    """
    # Check if item exists
    db_item = db.query(sql_models.Lost_and_Found).filter(sql_models.Lost_and_Found.unique_id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Lost and found item not found")
    
    try:
        db.delete(db_item)
        db.commit()
        return None
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete lost and found item: {str(e)}")

# Additional useful routes

# Get student by ID
@app.get("/students/{student_id}", response_model=StudentModel)
def get_student(
    student_id: str,
    db: Session = Depends(get_db)
):
    """
    Get a student by ID
    """
    db_student = db.query(sql_models.Student).filter(sql_models.Student.student_id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student

# Get teacher by ID
@app.get("/teachers/{teacher_id}", response_model=TeacherModel)
def get_teacher(
    teacher_id: str,
    db: Session = Depends(get_db)
):
    """
    Get a teacher by ID
    """
    db_teacher = db.query(sql_models.Teacher).filter(sql_models.Teacher.teacher_id == teacher_id).first()
    if not db_teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return db_teacher

# Get class by ID
@app.get("/classes/{class_id}", response_model=ClassModel)
def get_class(
    class_id: str,
    db: Session = Depends(get_db)
):
    """
    Get a class by ID
    """
    db_class = db.query(sql_models.Class).filter(sql_models.Class.class_id == class_id).first()
    if not db_class:
        raise HTTPException(status_code=404, detail="Class not found")
    return db_class

# Get students by class ID
@app.get("/classes/{class_id}/students", response_model=List[StudentModel])
def get_students_by_class(
    class_id: str,
    db: Session = Depends(get_db)
):
    """
    Get all students in a specific class
    """
    # Check if class exists
    db_class = db.query(sql_models.Class).filter(sql_models.Class.class_id == class_id).first()
    if not db_class:
        raise HTTPException(status_code=404, detail="Class not found")
    
    students = db.query(sql_models.Student).filter(sql_models.Student.class_id == class_id).all()
    return students

# Get subject by ID
@app.get("/subjects/{subject_id}", response_model=SubjectModel)
def get_subject(
    subject_id: str,
    db: Session = Depends(get_db)
):
    """
    Get a subject by ID
    """
    db_subject = db.query(sql_models.Subject).filter(sql_models.Subject.subject_id == subject_id).first()
    if not db_subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return db_subject

# Get attendance for a specific student on a specific date
@app.get("/attendance/student/{student_id}/date/{date_value}", response_model=List[AttendanceModel])
def get_student_attendance_by_date(
    student_id: str,
    date_value: date,
    db: Session = Depends(get_db)
):
    """
    Get attendance record for a specific student on a specific date
    """
    # Check if student exists
    db_student = db.query(sql_models.Student).filter(sql_models.Student.student_id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    attendance = db.query(sql_models.Attendance).filter(
        sql_models.Attendance.student_id == student_id,
        sql_models.Attendance.date == date_value
    ).all()
    
    return attendance

# Get attendance for a class on a specific date
@app.get("/attendance/class/{class_id}/date/{date_value}", response_model=List[AttendanceModel])
def get_class_attendance_by_date(
    class_id: str,
    date_value: date,
    db: Session = Depends(get_db)
):
    """
    Get attendance records for all students in a class on a specific date
    """
    # Check if class exists
    db_class = db.query(sql_models.Class).filter(sql_models.Class.class_id == class_id).first()
    if not db_class:
        raise HTTPException(status_code=404, detail="Class not found")
    
    attendance = db.query(sql_models.Attendance).filter(
        sql_models.Attendance.class_id == class_id,
        sql_models.Attendance.date == date_value
    ).all()
    
    return attendance

# Get timetable for a specific class
@app.get("/timetable/class/{class_id}", response_model=List[TimetableModel])
def get_class_timetable(
    class_id: str,
    db: Session = Depends(get_db)
):
    """
    Get all timetable entries for a specific class
    """
    # Check if class exists
    db_class = db.query(sql_models.Class).filter(sql_models.Class.class_id == class_id).first()
    if not db_class:
        raise HTTPException(status_code=404, detail="Class not found")
    
    timetable = db.query(sql_models.Timetable).join(
        sql_models.Class_Subject, 
        sql_models.Class_Subject.class_sub_id == sql_models.Timetable.class_sub_id
    ).filter(
        sql_models.Class_Subject.class_id == class_id
    ).all()
    
    return timetable

# Get all assignments for a specific class
@app.get("/assignments/class/{class_id}", response_model=List[AssignmentModel])
def get_class_assignments(
    class_id: str,
    db: Session = Depends(get_db)
):
    """
    Get all assignments for a specific class
    """
    # Check if class exists
    db_class = db.query(sql_models.Class).filter(sql_models.Class.class_id == class_id).first()
    if not db_class:
        raise HTTPException(status_code=404, detail="Class not found")
    
    assignments = db.query(sql_models.Assignment).join(
        sql_models.Class_Subject,
        sql_models.Class_Subject.class_sub_id == sql_models.Assignment.class_sub_id
    ).filter(
        sql_models.Class_Subject.class_id == class_id
    ).all()
    
    return assignments

# Get all pending leave applications
@app.get("/leave-applications/pending", response_model=List[LeaveApplicationModel])
def get_pending_leave_applications(
    db: Session = Depends(get_db)
):
    """
    Get all pending leave applications
    """
    leaves = db.query(sql_models.Leave_Application).filter(
        sql_models.Leave_Application.status == LeaveStatus.PENDING
    ).all()
    
    return leaves

# Change password route for students
@app.put("/students/{student_id}/change-password", status_code=204)
def change_student_password(
    student_id: str,
    old_password: str = Body(...),
    new_password: str = Body(...),
    db: Session = Depends(get_db)
):
    """
    Change a student's password
    """
    # Check if student exists
    db_student = db.query(sql_models.Student).filter(sql_models.Student.student_id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Verify old password
    if not pwd_context.verify(old_password, db_student.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect old password")
    
    # Update password
    db_student.password_hash = pwd_context.hash(new_password)
    
    try:
        db.commit()
        return None
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to change password: {str(e)}")

# Change password route for teachers
@app.put("/teachers/{teacher_id}/change-password", status_code=204)
def change_teacher_password(
    teacher_id: str,
    old_password: str = Body(...),
    new_password: str = Body(...),
    db: Session = Depends(get_db)
):
    """
    Change a teacher's password
    """
    # Check if teacher exists
    db_teacher = db.query(sql_models.Teacher).filter(sql_models.Teacher.teacher_id == teacher_id).first()
    if not db_teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    # Verify old password
    if not pwd_context.verify(old_password, db_teacher.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect old password")
    
    # Update password
    db_teacher.password_hash = pwd_context.hash(new_password)
    
    try:
        db.commit()
        return None
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to change password: {str(e)}")

# Dashboard summary stats
@app.get("/dashboard/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    """
    Get summary statistics for dashboard
    """
    today = date.today()
    try:
        stats = {
            "total_students": db.query(sql_models.Student).count(),
            "total_teachers": db.query(sql_models.Teacher).count(),
            "total_classes": db.query(sql_models.Class).count(),
            "total_subjects": db.query(sql_models.Subject).count(),
            "pending_leaves": db.query(sql_models.Leave_Application).filter(
                sql_models.Leave_Application.status == LeaveStatus.PENDING
            ).count(),
            "assignments_due_today": db.query(sql_models.Assignment).filter(
                sql_models.Assignment.dueDate >= datetime.combine(today, datetime.min.time()),
                sql_models.Assignment.dueDate < datetime.combine(today + timedelta(days=1), datetime.min.time())
            ).count(),
            "lost_items": db.query(sql_models.Lost_and_Found).filter(
                sql_models.Lost_and_Found.status == ItemStatus.LOST
            ).count(),
        }
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve dashboard stats: {str(e)}")
