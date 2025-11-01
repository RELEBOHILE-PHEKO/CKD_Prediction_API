# CKD_Prediction_API

# Chronic Kidney Disease Database and API

This repository contains the database setup and FastAPI implementation for the Chronic Kidney Disease prediction pipeline.

## Task 1 - Database Setup

1. **Prerequisites**:
   - PostgreSQL 13+
   - MongoDB (optional, for predictions storage)
   - Python 3.8+
   - Required Python packages (see requirements.txt)

2. **Database Setup**:
   ```bash
   # Install dependencies
   pip install -r requirements.txt
   
   # Create database and user (run in psql)
   CREATE DATABASE ckd_database;
   
   # Import schema and data (run in psql or pgAdmin)
   \i sql/01_schema.sql
   \i sql/02_procedures.sql
   \i sql/03_triggers.sql
   \i sql/04_sample_data.sql
   ```

## Task 2 - FastAPI CRUD Endpoints

### API Setup

1. **Environment Variables**:
   Create a `.env` file in the root directory:
   ```env
   DATABASE_URL=postgresql://postgres:yourpassword@localhost/ckd_database
   MONGODB_URI=mongodb://localhost:27017/
   ```

2. **Run the API**:
   ```bash
   # Install dependencies
   pip install -r requirements.txt
   
   # Run the FastAPI server
   uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **API Documentation**:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Available Endpoints

#### Patients (`/api/v1/patients`)
- `POST /api/v1/patients/` - Create a new patient
- `GET /api/v1/patients/` - Get all patients (with pagination)
- `GET /api/v1/patients/{patient_id}` - Get patient by ID
- `PUT /api/v1/patients/{patient_id}` - Update patient
- `DELETE /api/v1/patients/{patient_id}` - Delete patient

#### Medical History (`/api/v1/medical-history`)
- `POST /api/v1/medical-history/` - Create medical history
- `GET /api/v1/medical-history/` - Get all medical histories
- `GET /api/v1/medical-history/patient/{patient_id}` - Get patient's medical history
- `GET /api/v1/medical-history/{history_id}` - Get medical history by ID
- `PUT /api/v1/medical-history/{history_id}` - Update medical history
- `DELETE /api/v1/medical-history/{history_id}` - Delete medical history

#### Vital Signs (`/api/v1/vital-signs`)
- `POST /api/v1/vital-signs/` - Create vital signs record
- `GET /api/v1/vital-signs/` - Get all vital signs (filterable by patient_id)
- `GET /api/v1/vital-signs/patient/{patient_id}` - Get patient's vital signs
- `GET /api/v1/vital-signs/{vital_id}` - Get vital signs by ID
- `PUT /api/v1/vital-signs/{vital_id}` - Update vital signs
- `DELETE /api/v1/vital-signs/{vital_id}` - Delete vital signs

#### Lab Results (`/api/v1/lab-results`)
- `POST /api/v1/lab-results/` - Create lab results record
- `GET /api/v1/lab-results/` - Get all lab results (filterable by patient_id)
- `GET /api/v1/lab-results/patient/{patient_id}` - Get patient's lab results
- `GET /api/v1/lab-results/{lab_id}` - Get lab results by ID
- `PUT /api/v1/lab-results/{lab_id}` - Update lab results
- `DELETE /api/v1/lab-results/{lab_id}` - Delete lab results

#### Diagnoses (`/api/v1/diagnoses`)
- `POST /api/v1/diagnoses/` - Create diagnosis record
- `GET /api/v1/diagnoses/` - Get all diagnoses (filterable by patient_id)
- `GET /api/v1/diagnoses/patient/{patient_id}` - Get patient's diagnoses
- `GET /api/v1/diagnoses/{diagnosis_id}` - Get diagnosis by ID
- `PUT /api/v1/diagnoses/{diagnosis_id}` - Update diagnosis
- `DELETE /api/v1/diagnoses/{diagnosis_id}` - Delete diagnosis

### MongoDB Endpoints

#### Patient History (`/api/v1/mongo/patient-history`)
- `POST /api/v1/mongo/patient-history/` - Create patient history entry
- `GET /api/v1/mongo/patient-history/` - Get all patient histories (filterable by patient_id, entry_type)
- `GET /api/v1/mongo/patient-history/patient/{patient_id}` - Get patient's history entries
- `GET /api/v1/mongo/patient-history/{history_id}` - Get history entry by ID
- `PUT /api/v1/mongo/patient-history/{history_id}` - Update history entry
- `DELETE /api/v1/mongo/patient-history/{history_id}` - Delete history entry

#### Predictions (`/api/v1/mongo/predictions`)
- `POST /api/v1/mongo/predictions/` - Create prediction record
- `GET /api/v1/mongo/predictions/` - Get all predictions (filterable by patient_id, model_name)
- `GET /api/v1/mongo/predictions/patient/{patient_id}` - Get patient's predictions
- `GET /api/v1/mongo/predictions/{prediction_id}` - Get prediction by ID
- `PUT /api/v1/mongo/predictions/{prediction_id}` - Update prediction
- `DELETE /api/v1/mongo/predictions/{prediction_id}` - Delete prediction
