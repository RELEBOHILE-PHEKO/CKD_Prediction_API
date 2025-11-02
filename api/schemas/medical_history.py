from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class MedicalHistoryBase(BaseModel):
    patient_id: int
    diabetes: bool = False
    hypertension: bool = False
    cardiovascular_disease: bool = False
    family_history_ckd: bool = False
    notes: Optional[str] = None


class MedicalHistoryCreate(MedicalHistoryBase):
    pass


class MedicalHistoryUpdate(BaseModel):
    diabetes: Optional[bool] = None
    hypertension: Optional[bool] = None
    cardiovascular_disease: Optional[bool] = None
    family_history_ckd: Optional[bool] = None
    notes: Optional[str] = None


class MedicalHistoryResponse(MedicalHistoryBase):
    history_id: int
    created_at: datetime

    class Config:
        from_attributes = True

