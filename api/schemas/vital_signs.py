from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class VitalSignsBase(BaseModel):
    patient_id: int
    measurement_date: Optional[datetime] = None
    blood_pressure_systolic: Optional[int] = Field(None, ge=0, le=300)
    blood_pressure_diastolic: Optional[int] = Field(None, ge=0, le=200)
    heart_rate: Optional[int] = Field(None, ge=0, le=300)
    weight_kg: Optional[float] = Field(None, ge=0)
    height_cm: Optional[float] = Field(None, ge=0)
    bmi: Optional[float] = Field(None, ge=0, le=100)
    temperature_c: Optional[float] = Field(None, ge=30, le=45)


class VitalSignsCreate(VitalSignsBase):
    pass


class VitalSignsUpdate(BaseModel):
    measurement_date: Optional[datetime] = None
    blood_pressure_systolic: Optional[int] = Field(None, ge=0, le=300)
    blood_pressure_diastolic: Optional[int] = Field(None, ge=0, le=200)
    heart_rate: Optional[int] = Field(None, ge=0, le=300)
    weight_kg: Optional[float] = Field(None, ge=0)
    height_cm: Optional[float] = Field(None, ge=0)
    bmi: Optional[float] = Field(None, ge=0, le=100)
    temperature_c: Optional[float] = Field(None, ge=30, le=45)


class VitalSignsResponse(VitalSignsBase):
    vital_id: int

    class Config:
        from_attributes = True

