from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from typing import Dict, Any, List, Optional
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class MongoDB:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDB, cls).__new__(cls)
            mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
            cls._instance.client = MongoClient(mongo_uri)
            cls._instance.db = cls._instance.client.get_database("ckd_database")
        return cls._instance

    @property
    def patient_history(self) -> Collection:
        return self.db.patient_history
    
    @property
    def predictions(self) -> Collection:
        return self.db.predictions

class PatientHistory:
    def __init__(self):
        self.db = MongoDB().patient_history

    def add_history_entry(
        self,
        patient_id: int,
        entry_type: str,
        entry_data: Dict[str, Any],
        timestamp: datetime = None
    ) -> str:
        if not timestamp:
            timestamp = datetime.utcnow()
        
        history_entry = {
            "patient_id": patient_id,
            "entry_type": entry_type,
            "data": entry_data,
            "timestamp": timestamp,
            "metadata": {
                "source": "system",
                "created_at": datetime.utcnow()
            }
        }
        
        result = self.db.insert_one(history_entry)
        return str(result.inserted_id)

class PredictionModel:
    def __init__(self):
        self.db = MongoDB().predictions

    def save_prediction(
        self,
        patient_id: int,
        model_name: str,
        features: Dict[str, Any],
        prediction: Dict[str, Any],
        model_version: str = "1.0",
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        prediction_doc = {
            "patient_id": patient_id,
            "model_name": model_name,
            "model_version": model_version,
            "features": features,
            "prediction": prediction,
            "timestamp": datetime.utcnow(),
            "metadata": metadata or {}
        }
        
        result = self.db.insert_one(prediction_doc)
        return str(result.inserted_id)

    def get_patient_predictions(
        self,
        patient_id: int,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        return list(self.db.find(
            {"patient_id": patient_id}
        ).sort("timestamp", -1).limit(limit))