# ml/train_ckd_model.py
# Chronic Kidney Disease (CKD) Prediction Model
# Trains a Random Forest classifier, evaluates, visualizes, and saves artifacts.

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import joblib
import warnings

warnings.filterwarnings("ignore")

# Configuration
DATA_PATH = "Chronic_Kidney_Disease_data.csv"
MODEL_DIR = "ml/models"
os.makedirs(MODEL_DIR, exist_ok=True)

# Load Dataset
print("Loading dataset...")
df = pd.read_csv(DATA_PATH)
df.columns = df.columns.str.strip()
print(f"Dataset loaded. Rows: {df.shape[0]} | Columns: {df.shape[1]}")

# Set target column
target_column = 'Diagnosis'
print(f"Using '{target_column}' as target column.")

# Handle Missing Values
df.replace('?', np.nan, inplace=True)
df.fillna(df.mode().iloc[0], inplace=True)
print("Missing values handled.")

# Drop unnecessary columns
if 'PatientID' in df.columns:
    df.drop('PatientID', axis=1, inplace=True)

# Encode Categorical Features
le = LabelEncoder()
for col in df.select_dtypes(include='object').columns:
    if col != target_column:
        df[col] = le.fit_transform(df[col])
if df[target_column].dtype == 'object':
    df[target_column] = le.fit_transform(df[target_column])
print("Categorical columns encoded.")

# Split Features and Target
X = df.drop(columns=[target_column])
y = df[target_column]
feature_names = X.columns.tolist()  # Save feature names for prediction
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
print(f"Data split complete. Training: {X_train.shape[0]} | Testing: {X_test.shape[0]}")

# Feature Scaling
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
print("Feature scaling complete.")

# Train Random Forest Model
model = RandomForestClassifier(n_estimators=100, max_depth=10, min_samples_split=5, random_state=42)
model.fit(X_train, y_train)
print("Model training complete.")

# Evaluate Model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy*100:.2f}%")
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(6, 4))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Not CKD','CKD'], yticklabels=['Not CKD','CKD'])
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix - CKD Prediction')
plt.tight_layout()
plt.savefig(os.path.join(MODEL_DIR, "confusion_matrix.png"))
plt.close()
print("Confusion matrix saved.")

# Feature Importance
feature_importance = pd.DataFrame({'Feature': X.columns, 'Importance': model.feature_importances_}).sort_values('Importance', ascending=False)
plt.figure(figsize=(10, 6))
sns.barplot(x='Importance', y='Feature', data=feature_importance.head(10), palette='viridis')
plt.title('Top 10 Important Features - CKD Model')
plt.tight_layout()
plt.savefig(os.path.join(MODEL_DIR, "feature_importance.png"))
plt.close()
print("Feature importance chart saved.")

# Save Model, Scaler, and Feature Names
joblib.dump(model, os.path.join(MODEL_DIR, "ckd_model.pkl"))
joblib.dump(scaler, os.path.join(MODEL_DIR, "scaler.pkl"))
joblib.dump(feature_names, os.path.join(MODEL_DIR, "feature_names.pkl"))
print("Model, scaler, and feature names saved.")

# Sample Prediction
sample = X_test[0].reshape(1, -1)
prediction = model.predict(sample)
print(f"Sample prediction (0 = No CKD, 1 = CKD): {prediction[0]}")
print("Training completed successfully.")
