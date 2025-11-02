from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ConfigDict

# ====== MONKEYPATCH: Fix Pydantic MongoDB _id compatibility ======
# This allows Pydantic models to use fields with leading underscores (like _id)
# TODO: Remove this when MongoDB schemas are updated with proper model_config
print("Applying MongoDB Pydantic compatibility patches...")

try:
    # Patch patient_history_mongo schemas
    from api.schemas import patient_history_mongo
    
    patient_history_models = [
        'PatientHistoryBase',
        'PatientHistoryCreate', 
        'PatientHistoryUpdate', 
        'PatientHistoryResponse'
    ]
    
    patched_count = 0
    for model_name in patient_history_models:
        if hasattr(patient_history_mongo, model_name):
            model = getattr(patient_history_mongo, model_name)
            model.model_config = ConfigDict(
                populate_by_name=True,
                arbitrary_types_allowed=True
            )
            print(f"  Patched {model_name} (patient_history_mongo)")
            patched_count += 1
            
except ImportError as e:
    print(f"Could not import patient_history_mongo schemas: {e}")
except Exception as e:
    print(f"Warning: Could not patch patient_history_mongo schemas: {e}")

try:
    # Patch prediction_mongo schemas
    from api.schemas import prediction_mongo
    
    prediction_models = [
        'PredictionBase',
        'PredictionCreate',
        'PredictionUpdate',
        'PredictionResponse'
    ]
    
    for model_name in prediction_models:
        if hasattr(prediction_mongo, model_name):
            model = getattr(prediction_mongo, model_name)
            model.model_config = ConfigDict(
                populate_by_name=True,
                arbitrary_types_allowed=True
            )
            print(f"  Patched {model_name} (prediction_mongo)")
            patched_count += 1
            
except ImportError as e:
    print(f"Could not import prediction_mongo schemas: {e}")
except Exception as e:
    print(f"Warning: Could not patch prediction_mongo schemas: {e}")

if patched_count > 0:
    print(f"Successfully patched {patched_count} model(s) for MongoDB compatibility")
else:
    print("No models found to patch")
# ====== END MONKEYPATCH ======

# Your existing router imports
from api.routers import (
    diagnoses,
    lab_results,
    medical_history,
    patient_history_mongo,
    patients,
    predictions_mongo,
    vital_signs
)

# Create FastAPI app
app = FastAPI(
    title="CKD Prediction API",
    description="API for Chronic Kidney Disease prediction and patient management",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(patients.router, prefix="/api/v1/patients", tags=["patients"])
app.include_router(diagnoses.router, prefix="/api/v1/diagnoses", tags=["diagnoses"])
app.include_router(vital_signs.router, prefix="/api/v1/vital-signs", tags=["vital-signs"])
app.include_router(lab_results.router, prefix="/api/v1/lab-results", tags=["lab-results"])
app.include_router(medical_history.router, prefix="/api/v1/medical-history", tags=["medical-history"])
app.include_router(patient_history_mongo.router, prefix="/api/v1/patient-history", tags=["patient-history"])
app.include_router(predictions_mongo.router, prefix="/api/v1/predictions", tags=["predictions"])

@app.get("/")
async def root():
    return {
        "message": "CKD Prediction API is running",
        "version": "1.0.0",
        "status": "healthy"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "CKD Prediction API"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
