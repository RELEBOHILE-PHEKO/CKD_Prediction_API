from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from api.database import get_db
from api.models.sql_models import Patient, VitalSigns
from api.schemas.vital_signs import VitalSignsCreate, VitalSignsUpdate, VitalSignsResponse

router = APIRouter(
    prefix="/vital-signs",
    tags=["Vital Signs"]
)


@router.post("/", response_model=VitalSignsResponse, status_code=status.HTTP_201_CREATED)
def create_vital_signs(vital_signs: VitalSignsCreate, db: Session = Depends(get_db)):
    """
    Create vital signs record for a patient.
    """
    patient = db.query(Patient).filter(Patient.patient_id == vital_signs.patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with ID {vital_signs.patient_id} not found"
        )
    
    try:
        vital_data = vital_signs.model_dump()
        if not vital_data.get("measurement_date"):
            vital_data["measurement_date"] = datetime.utcnow()
        
        db_vital_signs = VitalSigns(**vital_data)
        db.add(db_vital_signs)
        db.commit()
        db.refresh(db_vital_signs)
        return db_vital_signs
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating vital signs: {str(e)}"
        )


@router.get("/", response_model=List[VitalSignsResponse])
def get_vital_signs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    patient_id: int = Query(None, description="Filter by patient ID"),
    db: Session = Depends(get_db)
):
    """
    Get all vital signs with pagination. Optionally filter by patient_id.
    """
    query = db.query(VitalSigns)
    if patient_id:
        query = query.filter(VitalSigns.patient_id == patient_id)
    
    vital_signs = query.offset(skip).limit(limit).all()
    return vital_signs


@router.get("/patient/{patient_id}", response_model=List[VitalSignsResponse])
def get_patient_vital_signs(patient_id: int, db: Session = Depends(get_db)):
    """
    Get all vital signs for a specific patient.
    """
    patient = db.query(Patient).filter(Patient.patient_id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with ID {patient_id} not found"
        )
    
    vital_signs = db.query(VitalSigns).filter(
        VitalSigns.patient_id == patient_id
    ).all()
    return vital_signs


@router.get("/{vital_id}", response_model=VitalSignsResponse)
def get_vital_signs_by_id(vital_id: int, db: Session = Depends(get_db)):
    """
    Get vital signs by ID.
    """
    vital_signs = db.query(VitalSigns).filter(VitalSigns.vital_id == vital_id).first()
    if not vital_signs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vital signs with ID {vital_id} not found"
        )
    return vital_signs


@router.put("/{vital_id}", response_model=VitalSignsResponse)
def update_vital_signs(
    vital_id: int,
    vital_signs_update: VitalSignsUpdate,
    db: Session = Depends(get_db)
):
    """
    Update vital signs by ID.
    """
    vital_signs = db.query(VitalSigns).filter(VitalSigns.vital_id == vital_id).first()
    if not vital_signs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vital signs with ID {vital_id} not found"
        )
    
    try:
        update_data = vital_signs_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(vital_signs, field, value)
        
        db.commit()
        db.refresh(vital_signs)
        return vital_signs
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating vital signs: {str(e)}"
        )


@router.delete("/{vital_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vital_signs(vital_id: int, db: Session = Depends(get_db)):
    """
    Delete vital signs by ID.
    """
    vital_signs = db.query(VitalSigns).filter(VitalSigns.vital_id == vital_id).first()
    if not vital_signs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vital signs with ID {vital_id} not found"
        )
    
    try:
        db.delete(vital_signs)
        db.commit()
        return None
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error deleting vital signs: {str(e)}"
        )

