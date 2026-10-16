from datetime import date
from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class StudentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    date_of_birth: date
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    course: Optional[str] = Field(None, max_length=100)
    address: Optional[str] = Field(None, max_length=200)
    enrollment_date: Optional[date] = None


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    date_of_birth: Optional[date] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    course: Optional[str] = Field(None, max_length=100)
    address: Optional[str] = Field(None, max_length=200)
    enrollment_date: Optional[date] = None


class StudentResponse(StudentBase):
    id: int

    class Config:
        from_attributes = True