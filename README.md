

---

# Chronic Kidney Disease (CKD) Prediction API

This project builds a scalable backend for predicting and managing **Chronic Kidney Disease (CKD)** cases. It integrates **FastAPI**, **PostgreSQL**, and **MongoDB** with machine learning support to store patient data, handle predictions, and provide clinical insights.

---

## Objective

To design and implement a dual-database architecture that efficiently manages both structured and unstructured medical data while providing real-time disease prediction capabilities.

---

## ⚙️ Technologies

* **FastAPI** — RESTful API framework
* **PostgreSQL** — Relational data (patients, labs, diagnoses)
* **MongoDB** — Non-relational data (predictions, model outputs)
* **SQLAlchemy** — ORM for PostgreSQL models
* **Pydantic** — Data validation & serialization
* **scikit-learn** — ML model training
* **Uvicorn** — ASGI server

---

##  Key Features

✅ CRUD endpoints for patients, medical history, lab results, and diagnoses
✅ Machine learning model integration for CKD prediction
✅ Hybrid data storage (SQL + NoSQL)
✅ Clear modular code organization (models, routes, schemas, ML)
✅ Ready for deployment on Render / Railway

---

## 🧪 How to Run

1. **Clone the repo**

   ```bash
   git clone https://github.com/RELEBOHILE-PHEKO/CKD_Prediction_API.git
   cd CKD_Prediction_API
   ```

2. **Set up the environment**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the API**

   ```bash
   uvicorn api.main:app --reload
   ```

4. **Access API Docs**

   * Swagger UI → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   * ReDoc → [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

##  Team Roles & Contributions

| Name                 | Role                                       | Responsibilities                                                                                                    |
| -------------------- | ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------- |
| **Relebohile Pheko** | *Task 3 – Model Integration & MongoDB API* | Integrated CKD prediction endpoints using MongoDB, implemented ML model logic, and tested deployed API on Render.   |
| **Teammate 1**       | *Task 1 – Database Design & Setup*         | Designed PostgreSQL schema, created SQL scripts (tables, triggers, sample data), and ensured referential integrity. |
| **Teammate 2**       | *Task 2 – FastAPI CRUD Operations*         | Built patient and diagnosis CRUD routes, handled request validation, and tested API consistency.                    |

> Each member contributed to testing, debugging, and integration across both database layers.


---

