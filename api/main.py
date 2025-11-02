from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ====== CRITICAL: This must run BEFORE any schema imports ======
# Monkey-patch Pydantic's model construction to allow _id fields
import pydantic
from pydantic._internal._model_construction import ModelMetaclass

# Store the original __new__ method
_original_new = ModelMetaclass.__new__

def patched_new(mcs, cls_name, bases, namespace, **kwargs):
    """Patched ModelMetaclass.__new__ that allows fields starting with underscore"""
    # Check if any field starts with underscore
    annotations = namespace.get('__annotations__', {})
    has_underscore_fields = any(key.startswith('_') for key in annotations.keys())
    
    if has_underscore_fields:
        # Force populate_by_name to True for models with underscore fields
        if 'model_config' not in namespace:
            from pydantic import ConfigDict
            namespace['model_config'] = ConfigDict(
                populate_by_name=True,
                arbitrary_types_allowed=True
            )
        elif hasattr(namespace['model_config'], 'update'):
            namespace['model_config'].update({
                'populate_by_name': True,
                'arbitrary_types_allowed': True
            })
    
    return _original_new(mcs, cls_name, bases, namespace, **kwargs)

# Apply the patch
ModelMetaclass.__new__ = staticmethod(patched_new)
print("Applied Pydantic underscore field compatibility patch")
# ====== END PATCH ======

# Now import everything else - schemas will use the patched version
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
