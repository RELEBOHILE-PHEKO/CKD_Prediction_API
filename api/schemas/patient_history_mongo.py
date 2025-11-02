from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, Any, Optional


class PatientHistoryCreate(BaseModel):
    patient_id: int
    entry_type: str = Field(..., min_length=1, max_length=100, description="Type of history entry")
    data: Dict[str, Any] = Field(..., description="History entry data")
    timestamp: Optional[datetime] = None


class PatientHistoryUpdate(BaseModel):
    entry_type: Optional[str] = Field(None, min_length=1, max_length=100)
    data: Optional[Dict[str, Any]] = None
    timestamp: Optional[datetime] = None


class PatientHistoryResponse(BaseModel):
    id: str = Field(..., alias="_id")
    patient_id: int
    entry_type: str
    data: Dict[str, Any]
    timestamp: datetime
    metadata: Dict[str, Any]

    class Config:
        populate_by_name = True
        from_attributes = True

