# Telco Customer Churn Prediction

A production-ready ML project that predicts customer churn using Logistic Regression,
served via a FastAPI REST API and containerised with Docker.

---

## Project Structure

```
churn-prediction/
├── notebooks/
│   └── churn_prediction.ipynb   ← Full EDA + training notebook
├── app/
│   └── main.py                  ← FastAPI service
├── models/                      ← Trained model is saved here by the notebook
├── data/
│   └── Telco-Customer-Churn-data.csv   ← Put the dataset here
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## Quick Start

### Step 1 — Place the dataset

```
churn-prediction/data/Telco-Customer-Churn-data.csv
```

### Step 2 — Train the model (run the notebook)

```bash
cd churn-prediction
pip install -r requirements.txt
jupyter notebook notebooks/churn_prediction.ipynb
```

Run all cells. This saves `models/churn_pipeline.pkl`.

### Step 3 — Run the API locally (without Docker)

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open: http://localhost:8000/docs

---

## Docker

### Build & run

```bash
docker compose up --build
```

### Or with plain Docker

```bash
docker build -t churn-api .
docker run -p 8000:8000 churn-api
```

---

## API Endpoints

| Method | Path       | Description                   |
|--------|------------|-------------------------------|
| GET    | `/`        | Health check                  |
| GET    | `/health`  | Health check                  |
| POST   | `/predict` | Predict churn for a customer  |

### Example request

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "gender": "Female",
    "seniorcitizen": 0,
    "partner": "No",
    "dependents": "No",
    "phoneservice": "Yes",
    "multiplelines": "No",
    "internetservice": "Fiber optic",
    "onlinesecurity": "No",
    "onlinebackup": "No",
    "deviceprotection": "No",
    "techsupport": "No",
    "streamingtv": "Yes",
    "streamingmovies": "Yes",
    "contract": "Month-to-month",
    "paperlessbilling": "Yes",
    "paymentmethod": "Electronic check",
    "tenure": 5,
    "monthlycharges": 90.0,
    "totalcharges": 450.0
  }'
```

### Example response

```json
{
  "churn_probability": 0.7821,
  "churn_prediction": 1,
  "churn_label": "CHURN"
}
```

---

## Model Performance (Test Set)

| Metric    | Score  |
|-----------|--------|
| Accuracy  | ~79%   |
| Precision | ~61%   |
| Recall    | ~55%   |
| F1-Score  | ~58%   |
| ROC-AUC   | ~84%   |

---

## Tech Stack

- **Python 3.10**
- **scikit-learn** — preprocessing pipeline + Logistic Regression
- **pandas / numpy** — data handling
- **FastAPI + Uvicorn** — REST API
- **Docker / Docker Compose** — containerisation
