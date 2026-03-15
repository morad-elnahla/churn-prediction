<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Syne&weight=800&size=32&pause=1000&color=E8FF47&center=true&vCenter=true&width=600&lines=ChurnGuard+%E2%9A%A1;Customer+Churn+Intelligence;ML-Powered+%C2%B7+Production+Ready" alt="ChurnGuard" />

<br/>

![Python](https://img.shields.io/badge/Python-3.10-E8FF47?style=for-the-badge&logo=python&logoColor=black&labelColor=0a0c10)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.7.1-E8FF47?style=for-the-badge&logo=scikitlearn&logoColor=black&labelColor=0a0c10)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-E8FF47?style=for-the-badge&logo=fastapi&logoColor=black&labelColor=0a0c10)
![Docker](https://img.shields.io/badge/Docker-Ready-E8FF47?style=for-the-badge&logo=docker&logoColor=black&labelColor=0a0c10)

<br/>

> **Predict who's about to leave — before they do.**  
> A production-ready ML system that scores customer churn risk in real-time using Gradient Boosting.

<br/>

| 🎯 ROC-AUC | ⚡ F1-Score | 🔍 Recall | 📦 Training Rows |
|:---:|:---:|:---:|:---:|
| **0.836** | **0.609** | **66.8%** | **7,043** |

</div>

---

## ✦ What is this?

**ChurnGuard** is an end-to-end machine learning project built on the [Telco Customer Churn dataset](https://www.kaggle.com/blastchar/telco-customer-churn).  
It identifies customers likely to cancel their subscription, allowing businesses to take action before churn happens.

The project covers the full ML lifecycle:
- Exploratory Data Analysis
- Feature Engineering & Preprocessing Pipeline
- Multi-model comparison (LR, Random Forest, Gradient Boosting)
- Threshold tuning for imbalanced classes
- REST API deployment with a full web interface
- Containerisation with Docker

---

## ✦ Project Structure

```
churn-prediction/
│
├── 📓 notebooks/
│   └── churn_prediction.ipynb     ← Full EDA + training pipeline
│
├── 🚀 app/
│   ├── main.py                    ← FastAPI service
│   ├── templates/
│   │   └── index.html             ← Web UI
│   └── static/
│
├── 🧠 models/
│   └── churn_pipeline.pkl         ← Trained model artifact
│
├── 📊 data/
│   └── Telco-Customer-Churn-data.csv
│
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## ✦ Quick Start

### Run locally

```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn app.main:app --reload --port 8000
```

Open **http://localhost:8000** — the full web UI will be there.

### Run with Docker

```bash
docker compose up --build
```

---

## ✦ API

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Web UI |
| `GET` | `/health` | Health check |
| `POST` | `/predict` | Predict churn |

### Example

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "gender": "Female",
    "seniorcitizen": "0",
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

```json
{
  "churn_probability": 0.6823,
  "churn_prediction": 1,
  "churn_label": "CHURN",
  "threshold_used": 0.35
}
```

---

## ✦ Model Performance

```
══════════════════════════════════════════════
  Algorithm   : Gradient Boosting
  Estimators  : 300 trees
  Threshold   : 0.35 (tuned on validation set)
══════════════════════════════════════════════
  Accuracy    : 77.2%
  Precision   : 55.9%
  Recall      : 66.8%   ← catches 2 in 3 churners
  F1-Score    : 60.9%
  ROC-AUC     : 83.6%
══════════════════════════════════════════════
```

> **Why tune the threshold?**  
> The default 0.5 cutoff ignores class imbalance (only ~27% of customers churn).  
> Lowering to 0.35 significantly improves Recall — catching more churners at the cost of slightly more false positives. In a business context, missing a churner is more costly than an unnecessary retention offer.

---

## ✦ Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.10 |
| ML | scikit-learn — GradientBoostingClassifier |
| Data | pandas, numpy |
| API | FastAPI + Uvicorn |
| UI | HTML / CSS / Vanilla JS |
| Container | Docker + Docker Compose |
| Dataset | [Kaggle — Telco Customer Churn](https://www.kaggle.com/blastchar/telco-customer-churn) |

---

<div align="center">

Built by **Morad El-Nahla**

</div>
