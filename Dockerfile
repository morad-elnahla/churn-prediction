# ── Stage 1: Build ───────────────────────────────────────────────────────────
FROM python:3.10-slim AS base

WORKDIR /app

# Install dependencies first (layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/    ./app/
COPY models/ ./models/

# ── Stage 2: Runtime ─────────────────────────────────────────────────────────
EXPOSE 8000

ENV MODEL_PATH=models/churn_pipeline.pkl

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
