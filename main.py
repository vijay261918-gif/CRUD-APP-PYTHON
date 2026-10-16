from fastapi import FastAPI, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from database import Base, engine, get_db
from models import Student
from schemas import StudentCreate, StudentUpdate, StudentResponse
from crud import (
    create_student,
    get_students,
    get_student,
    update_student,
    delete_student,
)
from ai_service import query_ollama
from pydantic import BaseModel


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Student Database CRUD API",
    description="A REST API for managing student records with optional AI query support",
    version="1.0.0",
)


class AIQueryRequest(BaseModel):
    query: str


class AIQueryResponse(BaseModel):
    answer: str


@app.post("/students", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student_endpoint(student: StudentCreate, db: Session = Depends(get_db)):
    existing = db.query(Student).filter(Student.email == student.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    return create_student(db, student)


@app.get("/students", response_model=List[StudentResponse])
def list_students(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    course: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return get_students(db, skip=skip, limit=limit, course=course)


@app.get("/students/{student_id}", response_model=StudentResponse)
def get_student_endpoint(student_id: int, db: Session = Depends(get_db)):
    student = get_student(db, student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    return student


@app.put("/students/{student_id}", response_model=StudentResponse)
@app.patch("/students/{student_id}", response_model=StudentResponse)
def update_student_endpoint(student_id: int, student: StudentUpdate, db: Session = Depends(get_db)):
    if student.email is not None:
        existing = db.query(Student).filter(Student.email == student.email, Student.id != student_id).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    updated = update_student(db, student_id, student)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    return updated


@app.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student_endpoint(student_id: int, db: Session = Depends(get_db)):
    deleted = delete_student(db, student_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    return None


@app.post("/ai/query", response_model=AIQueryResponse)
async def ai_query(request: AIQueryRequest, db: Session = Depends(get_db)):
    answer = await query_ollama(db, request.query)
    return AIQueryResponse(answer=answer)