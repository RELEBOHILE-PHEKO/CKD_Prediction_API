# CKD_Prediction_API

# Chronic Kidney Disease Database (Task 1)

This repository contains the database setup for the Chronic Kidney Disease prediction pipeline.

## Database Setup

1. **Prerequisites**:
   - PostgreSQL 13+
   - Python 3.8+
   - Required Python packages: `psycopg2-binary sqlalchemy python-dotenv pymongo`

2. **Setup**:
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