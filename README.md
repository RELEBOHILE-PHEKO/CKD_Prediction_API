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
   
   # Run the SQL files in this order:
   ```bash
   psql -U your_username -d ckd_database -f sql/schema.sql
   psql -U your_username -d ckd_database -f sql/procedures.sql
   psql -U your_username -d ckd_database -f sql/triggers.sql
   psql -U your_username -d ckd_database -f sql/sample_data.sql