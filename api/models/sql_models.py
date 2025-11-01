from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, Text, Date, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:yourpassword@localhost/ckd_database")
engine = create_engine(DATABASE_URL)
Base = declarative_base()

class Patient(Base):
    __tablename__ = 'patients'

    patient_id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String(10), nullable=False)
    contact_number = Column(String(20))
    email = Column(String(100))
    address = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    medical_history = relationship("MedicalHistory", back_populates="patient", uselist=False)
    vital_signs = relationship("VitalSigns", back_populates="patient")
    lab_results = relationship("LabResults", back_populates="patient")
    diagnoses = relationship("Diagnosis", back_populates="patient")

class MedicalHistory(Base):
    __tablename__ = 'medical_history'

    history_id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.patient_id', ondelete='CASCADE'))
    diabetes = Column(Boolean, default=False)
    hypertension = Column(Boolean, default=False)
    cardiovascular_disease = Column(Boolean, default=False)
    family_history_ckd = Column(Boolean, default=False)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient", back_populates="medical_history")

class VitalSigns(Base):
    __tablename__ = 'vital_signs'

    vital_id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.patient_id', ondelete='CASCADE'))
    measurement_date = Column(DateTime, default=datetime.utcnow)
    blood_pressure_systolic = Column(Integer)
    blood_pressure_diastolic = Column(Integer)
    heart_rate = Column(Integer)
    weight_kg = Column(Float)
    height_cm = Column(Float)
    bmi = Column(Float)
    temperature_c = Column(Float)

    patient = relationship("Patient", back_populates="vital_signs")

class LabResults(Base):
    __tablename__ = 'lab_results'

    lab_id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.patient_id', ondelete='CASCADE'))
    test_date = Column(DateTime, default=datetime.utcnow)
    serum_creatinine = Column(Float)
    blood_urea_nitrogen = Column(Integer)
    sodium_level = Column(Integer)
    potassium_level = Column(Float)
    hemoglobin = Column(Float)
    white_blood_cells = Column(Float)
    red_blood_cells = Column(Float)
    egfr = Column(Float)

    patient = relationship("Patient", back_populates="lab_results")

class Diagnosis(Base):
    __tablename__ = 'diagnoses'

    diagnosis_id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.patient_id', ondelete='CASCADE'))
    diagnosis_date = Column(DateTime, default=datetime.utcnow)
    ckd_stage = Column(Integer)
    gfr_value = Column(Float)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient", back_populates="diagnoses")

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("Database tables created successfully!")