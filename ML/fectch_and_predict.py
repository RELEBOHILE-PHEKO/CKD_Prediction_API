import pandas as pd
import numpy as np
import joblib
import os

MODEL_DIR = "ml/models"

# Load model, scaler, and feature names
model = joblib.load(os.path.join(MODEL_DIR, "ckd_model.pkl"))
scaler = joblib.load(os.path.join(MODEL_DIR, "scaler.pkl"))
feature_names = joblib.load(os.path.join(MODEL_DIR, "feature_names.pkl"))
print("Model, scaler, and feature names loaded successfully.")

def predict_ckd(patient_dict):
    # Convert input dict to DataFrame
    df = pd.DataFrame([patient_dict])

    # Keep only columns used during training
    df = df[feature_names]

    # Transform features
    df_scaled = scaler.transform(df)

    # Predict
    prediction = model.predict(df_scaled)[0]
    return prediction

# Example patient (replace values with actual data)
sample_patient = {
    'Age': 45,
    'Gender': 1,
    'Ethnicity': 0,
    'SocioeconomicStatus': 2,
    'EducationLevel': 1,
    'BMI': 27.5,
    'Smoking': 0,
    'AlcoholConsumption': 1,
    'PhysicalActivity': 2,
    'DietQuality': 3,
    'SleepQuality': 2,
    'FamilyHistoryKidneyDisease': 0,
    'FamilyHistoryHypertension': 1,
    'FamilyHistoryDiabetes': 0,
    'PreviousAcuteKidneyInjury': 0,
    'UrinaryTractInfections': 0,
    'SystolicBP': 130,
    'DiastolicBP': 85,
    'FastingBloodSugar': 100,
    'HbA1c': 5.6,
    'SerumCreatinine': 1.0,
    'BUNLevels': 15,
    'GFR': 90,
    'ProteinInUrine': 0,
    'ACR': 10,
    'SerumElectrolytesSodium': 140,
    'SerumElectrolytesPotassium': 4.0,
    'SerumElectrolytesCalcium': 9.0,
    'SerumElectrolytesPhosphorus': 3.5,
    'HemoglobinLevels': 14,
    'CholesterolTotal': 180,
    'CholesterolLDL': 100,
    'CholesterolHDL': 50,
    'CholesterolTriglycerides': 120,
    'ACEInhibitors': 0,
    'Diuretics': 0,
    'NSAIDsUse': 0,
    'Statins': 0,
    'AntidiabeticMedications': 0,
    'Edema': 0,
    'FatigueLevels': 1,
    'NauseaVomiting': 0,
    'MuscleCramps': 0,
    'Itching': 0,
    'QualityOfLifeScore': 80,
    'HeavyMetalsExposure': 0,
    'OccupationalExposureChemicals': 0,
    'WaterQuality': 1,
    'MedicalCheckupsFrequency': 2,
    'MedicationAdherence': 1,
    'HealthLiteracy': 2,
    'DoctorInCharge': 1
}

result = predict_ckd(sample_patient)
print(f"Predicted CKD (0 = No, 1 = Yes): {result}")
