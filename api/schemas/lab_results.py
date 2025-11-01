from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class LabResultsBase(BaseModel):
    patient_id: int
    test_date: Optional[datetime] = None
    serum_creatinine: Optional[float] = Field(None, ge=0)
    blood_urea_nitrogen: Optional[int] = Field(None, ge=0)
    sodium_level: Optional[int] = Field(None, ge=0)
    potassium_level: Optional[float] = Field(None, ge=0)
    hemoglobin: Optional[float] = Field(None, ge=0)
    white_blood_cells: Optional[float] = Field(None, ge=0)
    red_blood_cells: Optional[float] = Field(None, ge=0)
    egfr: Optional[float] = Field(None, ge=0)


class LabResultsCreate(LabResultsBase):
    pass


class LabResultsUpdate(BaseModel):
    test_date: Optional[datetime] = None
    serum_creatinine: Optional[float] = Field(None, ge=0)
    blood_urea_nitrogen: Optional[int] = Field(None, ge=0)
    sodium_level: Optional[int] = Field(None, ge=0)
    potassium_level: Optional[float] = Field(None, ge=0)
    hemoglobin: Optional[float] = Field(None, ge=0)
    white_blood_cells: Optional[float] = Field(None, ge=0)
    red_blood_cells: Optional[float] = Field(None, ge=0)
    egfr: Optional[float] = Field(None, ge=0)


class LabResultsResponse(LabResultsBase):
    lab_id: int

    class Config:
        from_attributes = True

