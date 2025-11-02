from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from api.database import get_db
from api.models.sql_models import Patient, LabResults
from api.schemas.lab_results import LabResultsCreate, LabResultsUpdate, LabResultsResponse

router = APIRouter(
    prefix="/lab-results",
    tags=["Lab Results"]
)


@router.post("/", response_model=LabResultsResponse, status_code=status.HTTP_201_CREATED)
def create_lab_results(lab_results: LabResultsCreate, db: Session = Depends(get_db)):
    """
    Create lab results record for a patient.
    """
    patient = db.query(Patient).filter(Patient.patient_id == lab_results.patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with ID {lab_results.patient_id} not found"
        )
    
    try:
        lab_data = lab_results.model_dump()
        if not lab_data.get("test_date"):
            lab_data["test_date"] = datetime.utcnow()
        
        db_lab_results = LabResults(**lab_data)
        db.add(db_lab_results)
        db.commit()
        db.refresh(db_lab_results)
        return db_lab_results
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating lab results: {str(e)}"
        )


@router.get("/", response_model=List[LabResultsResponse])
def get_lab_results(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    patient_id: int = Query(None, description="Filter by patient ID"),
    db: Session = Depends(get_db)
):
    """
    Get all lab results with pagination. Optionally filter by patient_id.
    """
    query = db.query(LabResults)
    if patient_id:
        query = query.filter(LabResults.patient_id == patient_id)
    
    lab_results = query.offset(skip).limit(limit).all()
    return lab_results


@router.get("/patient/{patient_id}", response_model=List[LabResultsResponse])
def get_patient_lab_results(patient_id: int, db: Session = Depends(get_db)):
    """
    Get all lab results for a specific patient.
    """
    patient = db.query(Patient).filter(Patient.patient_id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with ID {patient_id} not found"
        )
    
    lab_results = db.query(LabResults).filter(
        LabResults.patient_id == patient_id
    ).all()
    return lab_results


@router.get("/{lab_id}", response_model=LabResultsResponse)
def get_lab_results_by_id(lab_id: int, db: Session = Depends(get_db)):
    """
    Get lab results by ID.
    """
    lab_results = db.query(LabResults).filter(LabResults.lab_id == lab_id).first()
    if not lab_results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lab results with ID {lab_id} not found"
        )
    return lab_results


@router.put("/{lab_id}", response_model=LabResultsResponse)
def update_lab_results(
    lab_id: int,
    lab_results_update: LabResultsUpdate,
    db: Session = Depends(get_db)
):
    """
    Update lab results by ID.
    """
    lab_results = db.query(LabResults).filter(LabResults.lab_id == lab_id).first()
    if not lab_results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lab results with ID {lab_id} not found"
        )
    
    try:
        update_data = lab_results_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(lab_results, field, value)
        
        db.commit()
        db.refresh(lab_results)
        return lab_results
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating lab results: {str(e)}"
        )


@router.delete("/{lab_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_lab_results(lab_id: int, db: Session = Depends(get_db)):
    """
    Delete lab results by ID.
    """
    lab_results = db.query(LabResults).filter(LabResults.lab_id == lab_id).first()
    if not lab_results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lab results with ID {lab_id} not found"
        )
    
    try:
        db.delete(lab_results)
        db.commit()
        return None
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error deleting lab results: {str(e)}"
        )

