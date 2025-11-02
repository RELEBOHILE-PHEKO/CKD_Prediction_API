from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from api.database import get_db
from api.models.sql_models import Patient, Diagnosis
from api.schemas.diagnosis import DiagnosisCreate, DiagnosisUpdate, DiagnosisResponse

router = APIRouter(
    prefix="/diagnoses",
    tags=["Diagnoses"]
)


@router.post("/", response_model=DiagnosisResponse, status_code=status.HTTP_201_CREATED)
def create_diagnosis(diagnosis: DiagnosisCreate, db: Session = Depends(get_db)):
    """
    Create a diagnosis record for a patient.
    """
    patient = db.query(Patient).filter(Patient.patient_id == diagnosis.patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with ID {diagnosis.patient_id} not found"
        )
    
    try:
        diagnosis_data = diagnosis.model_dump()
        if not diagnosis_data.get("diagnosis_date"):
            diagnosis_data["diagnosis_date"] = datetime.utcnow()
        
        db_diagnosis = Diagnosis(**diagnosis_data)
        db.add(db_diagnosis)
        db.commit()
        db.refresh(db_diagnosis)
        return db_diagnosis
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating diagnosis: {str(e)}"
        )


@router.get("/", response_model=List[DiagnosisResponse])
def get_diagnoses(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    patient_id: int = Query(None, description="Filter by patient ID"),
    db: Session = Depends(get_db)
):
    """
    Get all diagnoses with pagination. Optionally filter by patient_id.
    """
    query = db.query(Diagnosis)
    if patient_id:
        query = query.filter(Diagnosis.patient_id == patient_id)
    
    diagnoses = query.offset(skip).limit(limit).all()
    return diagnoses


@router.get("/patient/{patient_id}", response_model=List[DiagnosisResponse])
def get_patient_diagnoses(patient_id: int, db: Session = Depends(get_db)):
    """
    Get all diagnoses for a specific patient.
    """
    patient = db.query(Patient).filter(Patient.patient_id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with ID {patient_id} not found"
        )
    
    diagnoses = db.query(Diagnosis).filter(
        Diagnosis.patient_id == patient_id
    ).all()
    return diagnoses


@router.get("/{diagnosis_id}", response_model=DiagnosisResponse)
def get_diagnosis_by_id(diagnosis_id: int, db: Session = Depends(get_db)):
    """
    Get diagnosis by ID.
    """
    diagnosis = db.query(Diagnosis).filter(Diagnosis.diagnosis_id == diagnosis_id).first()
    if not diagnosis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Diagnosis with ID {diagnosis_id} not found"
        )
    return diagnosis


@router.put("/{diagnosis_id}", response_model=DiagnosisResponse)
def update_diagnosis(
    diagnosis_id: int,
    diagnosis_update: DiagnosisUpdate,
    db: Session = Depends(get_db)
):
    """
    Update diagnosis by ID.
    """
    diagnosis = db.query(Diagnosis).filter(Diagnosis.diagnosis_id == diagnosis_id).first()
    if not diagnosis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Diagnosis with ID {diagnosis_id} not found"
        )
    
    try:
        update_data = diagnosis_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(diagnosis, field, value)
        
        db.commit()
        db.refresh(diagnosis)
        return diagnosis
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating diagnosis: {str(e)}"
        )


@router.delete("/{diagnosis_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_diagnosis(diagnosis_id: int, db: Session = Depends(get_db)):
    """
    Delete diagnosis by ID.
    """
    diagnosis = db.query(Diagnosis).filter(Diagnosis.diagnosis_id == diagnosis_id).first()
    if not diagnosis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Diagnosis with ID {diagnosis_id} not found"
        )
    
    try:
        db.delete(diagnosis)
        db.commit()
        return None
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error deleting diagnosis: {str(e)}"
        )

