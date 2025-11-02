from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
from datetime import datetime
from bson import ObjectId
from bson.errors import InvalidId

from api.database import get_mongo_db
from api.models.mongo_models import MongoDB
from api.schemas.patient_history_mongo import (
    PatientHistoryCreate,
    PatientHistoryUpdate,
    PatientHistoryResponse
)

router = APIRouter(
    prefix="/patient-history",
    tags=["Patient History (MongoDB)"]
)


def validate_object_id(id_str: str) -> ObjectId:
    """Validate and convert string to ObjectId."""
    try:
        return ObjectId(id_str)
    except InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid ID format: {id_str}"
        )


@router.post("/", response_model=PatientHistoryResponse, status_code=status.HTTP_201_CREATED)
def create_patient_history(
    history: PatientHistoryCreate,
    mongo_db: MongoDB = Depends(get_mongo_db)
):
    """
    Create a new patient history entry.
    """
    try:
        history_data = history.model_dump()
        if not history_data.get("timestamp"):
            history_data["timestamp"] = datetime.utcnow()
        
        history_data["metadata"] = {
            "source": "system",
            "created_at": datetime.utcnow()
        }
        
        collection = mongo_db.patient_history
        result = collection.insert_one(history_data)
        
        created_doc = collection.find_one({"_id": result.inserted_id})
        created_doc["_id"] = str(created_doc["_id"])
        
        return created_doc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating patient history: {str(e)}"
        )


@router.get("/", response_model=List[PatientHistoryResponse])
def get_patient_histories(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    patient_id: int = Query(None, description="Filter by patient ID"),
    entry_type: str = Query(None, description="Filter by entry type"),
    mongo_db: MongoDB = Depends(get_mongo_db)
):
    """
    Get all patient history entries with pagination and optional filters.
    """
    try:
        collection = mongo_db.patient_history
        
        query = {}
        if patient_id is not None:
            query["patient_id"] = patient_id
        if entry_type:
            query["entry_type"] = entry_type
        
        cursor = collection.find(query).skip(skip).limit(limit).sort("timestamp", -1)
        histories = list(cursor)
        
        for history in histories:
            history["_id"] = str(history["_id"])
        
        return histories
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error fetching patient histories: {str(e)}"
        )


@router.get("/patient/{patient_id}", response_model=List[PatientHistoryResponse])
def get_patient_history_by_patient_id(
    patient_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    mongo_db: MongoDB = Depends(get_mongo_db)
):
    """
    Get all history entries for a specific patient.
    """
    try:
        collection = mongo_db.patient_history
        cursor = collection.find({"patient_id": patient_id}).skip(skip).limit(limit).sort("timestamp", -1)
        histories = list(cursor)
        
        for history in histories:
            history["_id"] = str(history["_id"])
        
        return histories
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error fetching patient history: {str(e)}"
        )


@router.get("/{history_id}", response_model=PatientHistoryResponse)
def get_patient_history(history_id: str, mongo_db: MongoDB = Depends(get_mongo_db)):
    """
    Get a patient history entry by ID.
    """
    try:
        obj_id = validate_object_id(history_id)
        collection = mongo_db.patient_history
        history = collection.find_one({"_id": obj_id})
        
        if not history:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Patient history with ID {history_id} not found"
            )
        
        history["_id"] = str(history["_id"])
        return history
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error fetching patient history: {str(e)}"
        )


@router.put("/{history_id}", response_model=PatientHistoryResponse)
def update_patient_history(
    history_id: str,
    history_update: PatientHistoryUpdate,
    mongo_db: MongoDB = Depends(get_mongo_db)
):
    """
    Update a patient history entry by ID.
    """
    try:
        obj_id = validate_object_id(history_id)
        collection = mongo_db.patient_history
        
        existing = collection.find_one({"_id": obj_id})
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Patient history with ID {history_id} not found"
            )
        
        update_data = history_update.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields to update"
            )
        
        collection.update_one(
            {"_id": obj_id},
            {"$set": update_data}
        )
        
        updated_doc = collection.find_one({"_id": obj_id})
        updated_doc["_id"] = str(updated_doc["_id"])
        
        return updated_doc
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating patient history: {str(e)}"
        )


@router.delete("/{history_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient_history(history_id: str, mongo_db: MongoDB = Depends(get_mongo_db)):
    """
    Delete a patient history entry by ID.
    """
    try:
        obj_id = validate_object_id(history_id)
        collection = mongo_db.patient_history
        
        result = collection.delete_one({"_id": obj_id})
        
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Patient history with ID {history_id} not found"
            )
        
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error deleting patient history: {str(e)}"
        )

