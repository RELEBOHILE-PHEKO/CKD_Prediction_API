from pydantic import BaseModel, EmailStr, Field
from datetime import date, datetime
from typing import Optional


class PatientBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    date_of_birth: date
    gender: str = Field(..., min_length=1, max_length=10)
    contact_number: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    address: Optional[str] = None


class PatientCreate(PatientBase):
    pass


class PatientUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    date_of_birth: Optional[date] = None
    gender: Optional[str] = Field(None, min_length=1, max_length=10)
    contact_number: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    address: Optional[str] = None


class PatientResponse(PatientBase):
    patient_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

