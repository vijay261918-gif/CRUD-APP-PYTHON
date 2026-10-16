from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Student
from schemas import StudentCreate, StudentUpdate
from datetime import date
from typing import Optional, List


def create_student(db: Session, student: StudentCreate) -> Student:
    db_student = Student(
        name=student.name,
        date_of_birth=student.date_of_birth,
        email=student.email,
        phone=student.phone,
        course=student.course,
        address=student.address,
        enrollment_date=student.enrollment_date,
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def get_students(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    course: Optional[str] = None,
) -> List[Student]:
    query = db.query(Student)
    if course:
        query = query.filter(Student.course == course)
    return query.offset(skip).limit(limit).all()


def get_student(db: Session, student_id: int) -> Optional[Student]:
    return db.query(Student).filter(Student.id == student_id).first()


def update_student(db: Session, student_id: int, student: StudentUpdate) -> Optional[Student]:
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if not db_student:
        return None

    update_data = student.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_student, field, value)

    db.commit()
    db.refresh(db_student)
    return db_student


def delete_student(db: Session, student_id: int) -> bool:
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if not db_student:
        return False

    db.delete(db_student)
    db.commit()
    return True


def get_student_stats(db: Session) -> dict:
    total = db.query(func.count(Student.id)).scalar()
    courses = db.query(Student.course, func.count(Student.id)).group_by(Student.course).all()
    course_counts = {course: count for course, count in courses if course}
    return {"total_students": total, "by_course": course_counts}