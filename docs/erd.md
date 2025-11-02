# Entity Relationship Diagram

## Relational Database (PostgreSQL)


erDiagram
    PATIENTS ||--o{ PATIENT_NOTES : has
    PATIENTS ||--o{ MEDICAL_IMAGES : has
    PATIENTS ||--o{ TREATMENT_PLANS : has
    
    PATIENT_NOTES {
        ObjectId _id PK
        int patient_id FK
        date note_date
        string note_type
        string content
        string doctor
        array tags
        timestamp created_at
    }
    
    MEDICAL_IMAGES {
        ObjectId _id PK
        int patient_id FK
        string image_type
        date date
        string findings
        string file_path
        string uploaded_by
        timestamp created_at
    }
    
    TREATMENT_PLANS {
        ObjectId _id PK
        int patient_id FK
        date start_date
        boolean active
        array medications {
            string name
            string dosage
            string frequency
        }
        array dietary_restrictions
        date next_appointment
        timestamp updated_at
    }