from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from api.routers import (
    patients,
    medical_history,
    vital_signs,
    lab_results,
    diagnoses
)
from api.routers import patient_history_mongo, predictions_mongo

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    yield
    # Shutdown (if needed)


# Create FastAPI application
app = FastAPI(
    title="CKD Prediction API",
    description="API for Chronic Kidney Disease prediction and patient management",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers (PostgreSQL/SQL)
app.include_router(patients.router, prefix="/api/v1")
app.include_router(medical_history.router, prefix="/api/v1")
app.include_router(vital_signs.router, prefix="/api/v1")
app.include_router(lab_results.router, prefix="/api/v1")
app.include_router(diagnoses.router, prefix="/api/v1")

# Include routers (MongoDB)
app.include_router(patient_history_mongo.router, prefix="/api/v1/mongo")
app.include_router(predictions_mongo.router, prefix="/api/v1/mongo")


# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to CKD Prediction API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"}
    )

