"""
Telco Customer Churn Prediction — FastAPI Service
"""

import os
import pickle
from pathlib import Path

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from pydantic import BaseModel, Field

# ── App ───────────────────────────────────────────────────────────────────────
BASE_DIR   = Path(__file__).parent
TMPL_DIR   = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(
    title="ChurnGuard — Churn Prediction API",
    description="Predicts whether a Telco customer is likely to churn.",
    version="2.0.0",
)

templates = Jinja2Templates(directory=str(TMPL_DIR))

if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# ── Load model at startup ─────────────────────────────────────────────────────
MODEL_PATH = Path(os.getenv("MODEL_PATH", "models/churn_pipeline.pkl"))

try:
    with open(MODEL_PATH, "rb") as f:
        artifact = pickle.load(f)
    pipeline  = artifact["pipeline"]
    threshold = float(artifact["threshold"])
    print(f"[OK] Model loaded — threshold = {threshold:.2f}")
except FileNotFoundError:
    raise RuntimeError(
        f"Model not found at '{MODEL_PATH}'. "
        "Run the notebook first to generate 'models/churn_pipeline.pkl'."
    )


# ── Schemas ───────────────────────────────────────────────────────────────────
class CustomerFeatures(BaseModel):
    gender: str           = Field(..., example="Female")
    seniorcitizen: str    = Field(..., example="0")
    partner: str          = Field(..., example="Yes")
    dependents: str       = Field(..., example="No")
    phoneservice: str     = Field(..., example="Yes")
    multiplelines: str    = Field(..., example="No")
    internetservice: str  = Field(..., example="Fiber optic")
    onlinesecurity: str   = Field(..., example="No")
    onlinebackup: str     = Field(..., example="No")
    deviceprotection: str = Field(..., example="No")
    techsupport: str      = Field(..., example="No")
    streamingtv: str      = Field(..., example="Yes")
    streamingmovies: str  = Field(..., example="Yes")
    contract: str         = Field(..., example="Month-to-month")
    paperlessbilling: str = Field(..., example="Yes")
    paymentmethod: str    = Field(..., example="Electronic check")
    tenure: int           = Field(..., example=5,    ge=0)
    monthlycharges: float = Field(..., example=90.0, ge=0)
    totalcharges: float   = Field(..., example=450.0, ge=0)


class PredictionResponse(BaseModel):
    churn_probability: float
    churn_prediction: int
    churn_label: str
    threshold_used: float


# ── Routes ────────────────────────────────────────────────────────────────────
@app.get("/", response_class=HTMLResponse, tags=["UI"])
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok", "threshold": threshold}


@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
def predict(customer: CustomerFeatures):
    """
    Returns churn probability, binary prediction, label, and threshold used.
    """
    try:
        input_df = pd.DataFrame([customer.model_dump()])
        prob = float(pipeline.predict_proba(input_df)[0, 1])
        pred = int(prob >= threshold)
        return PredictionResponse(
            churn_probability=round(prob, 4),
            churn_prediction=pred,
            churn_label="CHURN" if pred == 1 else "NO CHURN",
            threshold_used=round(threshold, 2),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
