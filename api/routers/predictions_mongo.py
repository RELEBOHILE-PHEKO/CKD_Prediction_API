from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
from bson import ObjectId
from bson.errors import InvalidId

from api.database import get_mongo_db
from api.models.mongo_models import MongoDB
from api.schemas.prediction_mongo import (
    PredictionCreate,
    PredictionUpdate,
    PredictionResponse
)

router = APIRouter(
    prefix="/predictions",
    tags=["Predictions (MongoDB)"]
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


@router.post("/", response_model=PredictionResponse, status_code=status.HTTP_201_CREATED)
def create_prediction(
    prediction: PredictionCreate,
    mongo_db: MongoDB = Depends(get_mongo_db)
):
    """
    Create a new prediction record.
    """
    try:
        from datetime import datetime
        
        prediction_data = prediction.model_dump()
        prediction_data["timestamp"] = datetime.utcnow()
        if not prediction_data.get("metadata"):
            prediction_data["metadata"] = {}
        
        collection = mongo_db.predictions
        result = collection.insert_one(prediction_data)
        
        created_doc = collection.find_one({"_id": result.inserted_id})
        created_doc["_id"] = str(created_doc["_id"])
        
        return created_doc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating prediction: {str(e)}"
        )


@router.get("/", response_model=List[PredictionResponse])
def get_predictions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    patient_id: int = Query(None, description="Filter by patient ID"),
    model_name: str = Query(None, description="Filter by model name"),
    mongo_db: MongoDB = Depends(get_mongo_db)
):
    """
    Get all predictions with pagination and optional filters.
    """
    try:
        collection = mongo_db.predictions
        
        query = {}
        if patient_id is not None:
            query["patient_id"] = patient_id
        if model_name:
            query["model_name"] = model_name
        
        cursor = collection.find(query).skip(skip).limit(limit).sort("timestamp", -1)
        predictions = list(cursor)
        
        for prediction in predictions:
            prediction["_id"] = str(prediction["_id"])
        
        return predictions
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error fetching predictions: {str(e)}"
        )


@router.get("/patient/{patient_id}", response_model=List[PredictionResponse])
def get_predictions_by_patient_id(
    patient_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    mongo_db: MongoDB = Depends(get_mongo_db)
):
    """
    Get all predictions for a specific patient.
    """
    try:
        collection = mongo_db.predictions
        cursor = collection.find({"patient_id": patient_id}).skip(skip).limit(limit).sort("timestamp", -1)
        predictions = list(cursor)
        
        for prediction in predictions:
            prediction["_id"] = str(prediction["_id"])
        
        return predictions
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error fetching predictions: {str(e)}"
        )


@router.get("/{prediction_id}", response_model=PredictionResponse)
def get_prediction(prediction_id: str, mongo_db: MongoDB = Depends(get_mongo_db)):
    """
    Get a prediction by ID.
    """
    try:
        obj_id = validate_object_id(prediction_id)
        collection = mongo_db.predictions
        prediction = collection.find_one({"_id": obj_id})
        
        if not prediction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Prediction with ID {prediction_id} not found"
            )
        
        prediction["_id"] = str(prediction["_id"])
        return prediction
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error fetching prediction: {str(e)}"
        )


@router.put("/{prediction_id}", response_model=PredictionResponse)
def update_prediction(
    prediction_id: str,
    prediction_update: PredictionUpdate,
    mongo_db: MongoDB = Depends(get_mongo_db)
):
    """
    Update a prediction by ID.
    """
    try:
        obj_id = validate_object_id(prediction_id)
        collection = mongo_db.predictions
        
        existing = collection.find_one({"_id": obj_id})
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Prediction with ID {prediction_id} not found"
            )
        
        update_data = prediction_update.model_dump(exclude_unset=True)
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
            detail=f"Error updating prediction: {str(e)}"
        )


@router.delete("/{prediction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_prediction(prediction_id: str, mongo_db: MongoDB = Depends(get_mongo_db)):
    """
    Delete a prediction by ID.
    """
    try:
        obj_id = validate_object_id(prediction_id)
        collection = mongo_db.predictions
        
        result = collection.delete_one({"_id": obj_id})
        
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Prediction with ID {prediction_id} not found"
            )
        
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error deleting prediction: {str(e)}"
        )

