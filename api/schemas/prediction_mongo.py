from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, Any, Optional


class PredictionCreate(BaseModel):
    patient_id: int
    model_name: str = Field(..., min_length=1, max_length=100)
    features: Dict[str, Any] = Field(..., description="Input features for the model")
    prediction: Dict[str, Any] = Field(..., description="Model prediction results")
    model_version: str = Field("1.0", max_length=50)
    metadata: Optional[Dict[str, Any]] = None


class PredictionUpdate(BaseModel):
    model_name: Optional[str] = Field(None, min_length=1, max_length=100)
    features: Optional[Dict[str, Any]] = None
    prediction: Optional[Dict[str, Any]] = None
    model_version: Optional[str] = Field(None, max_length=50)
    metadata: Optional[Dict[str, Any]] = None


class PredictionResponse(BaseModel):
    id: str = Field(..., alias="_id")
    patient_id: int
    model_name: str
    model_version: str
    features: Dict[str, Any]
    prediction: Dict[str, Any]
    timestamp: datetime
    metadata: Dict[str, Any]

    class Config:
        populate_by_name = True
        from_attributes = True

