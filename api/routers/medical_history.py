from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from api.database import get_db
from api.models.sql_models import Patient, MedicalHistory
from api.schemas.medical_history import (
    MedicalHistoryCreate,
    MedicalHistoryUpdate,
    MedicalHistoryResponse
)

router = APIRouter(
    prefix="/medical-history",
    tags=["Medical History"]
)


@router.post("/", response_model=MedicalHistoryResponse, status_code=status.HTTP_201_CREATED)
def create_medical_history(history: MedicalHistoryCreate, db: Session = Depends(get_db)):
    """
    Create medical history for a patient.
    """
    patient = db.query(Patient).filter(Patient.patient_id == history.patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with ID {history.patient_id} not found"
        )
    
    existing = db.query(MedicalHistory).filter(
        MedicalHistory.patient_id == history.patient_id
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Medical history already exists for patient {history.patient_id}"
        )
    
    try:
        db_history = MedicalHistory(**history.model_dump())
        db.add(db_history)
        db.commit()
        db.refresh(db_history)
        return db_history
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating medical history: {str(e)}"
        )


@router.get("/", response_model=List[MedicalHistoryResponse])
def get_medical_histories(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Get all medical histories with pagination.
    """
    histories = db.query(MedicalHistory).offset(skip).limit(limit).all()
    return histories


@router.get("/patient/{patient_id}", response_model=MedicalHistoryResponse)
def get_patient_medical_history(patient_id: int, db: Session = Depends(get_db)):
    """
    Get medical history for a specific patient.
    """
    history = db.query(MedicalHistory).filter(
        MedicalHistory.patient_id == patient_id
    ).first()
    if not history:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Medical history not found for patient {patient_id}"
        )
    return history


@router.get("/{history_id}", response_model=MedicalHistoryResponse)
def get_medical_history(history_id: int, db: Session = Depends(get_db)):
    """
    Get medical history by ID.
    """
    history = db.query(MedicalHistory).filter(
        MedicalHistory.history_id == history_id
    ).first()
    if not history:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Medical history with ID {history_id} not found"
        )
    return history


@router.put("/{history_id}", response_model=MedicalHistoryResponse)
def update_medical_history(
    history_id: int,
    history_update: MedicalHistoryUpdate,
    db: Session = Depends(get_db)
):
    """
    Update medical history by ID.
    """
    history = db.query(MedicalHistory).filter(
        MedicalHistory.history_id == history_id
    ).first()
    if not history:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Medical history with ID {history_id} not found"
        )
    
    try:
        update_data = history_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(history, field, value)
        
        db.commit()
        db.refresh(history)
        return history
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating medical history: {str(e)}"
        )


@router.delete("/{history_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_medical_history(history_id: int, db: Session = Depends(get_db)):
    """
    Delete medical history by ID.
    """
    history = db.query(MedicalHistory).filter(
        MedicalHistory.history_id == history_id
    ).first()
    if not history:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Medical history with ID {history_id} not found"
        )
    
    try:
        db.delete(history)
        db.commit()
        return None
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error deleting medical history: {str(e)}"
        )

