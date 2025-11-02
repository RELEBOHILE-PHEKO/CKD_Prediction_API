// MongoDB Schema for Unstructured Data
db = db.getSiblingDB('ckd_database');

// Create collections
db.createCollection('patient_notes');
db.createCollection('medical_images');
db.createCollection('treatment_plans');

// Create indexes
db.patient_notes.createIndex({ patient_id: 1 });
db.medical_images.createIndex({ patient_id: 1, date: -1 });
db.treatment_plans.createIndex({ patient_id: 1, active: 1 });

// Sample data
db.patient_notes.insertOne({
    patient_id: 1,
    note_date: new Date(),
    note_type: "initial_assessment",
    content: "Patient presents with elevated blood pressure and proteinuria. Family history of CKD.",
    doctor: "Dr. Smith",
    tags: ["hypertension", "family_history"]
});

db.medical_images.insertOne({
    patient_id: 1,
    image_type: "kidney_ultrasound",
    date: new Date(),
    findings: "Mild hydronephrosis observed in right kidney",
    file_path: "/images/pat123_ultra_20231101.jpg"
});

db.treatment_plans.insertOne({
    patient_id: 1,
    start_date: new Date(),
    active: true,
    medications: [
        { name: "Lisinopril", dosage: "10mg", frequency: "daily" },
        { name: "Furosemide", dosage: "20mg", frequency: "twice daily" }
    ],
    dietary_restrictions: ["low_sodium", "reduced_protein"],
    next_appointment: new Date("2023-12-01")
});