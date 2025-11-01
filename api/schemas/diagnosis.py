from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class DiagnosisBase(BaseModel):
    patient_id: int
    diagnosis_date: Optional[datetime] = None
    ckd_stage: Optional[int] = Field(None, ge=0, le=5)
    gfr_value: Optional[float] = Field(None, ge=0)
    notes: Optional[str] = None


class DiagnosisCreate(DiagnosisBase):
    pass


class DiagnosisUpdate(BaseModel):
    diagnosis_date: Optional[datetime] = None
    ckd_stage: Optional[int] = Field(None, ge=0, le=5)
    gfr_value: Optional[float] = Field(None, ge=0)
    notes: Optional[str] = None


class DiagnosisResponse(DiagnosisBase):
    diagnosis_id: int
    created_at: datetime

    class Config:
        from_attributes = True

