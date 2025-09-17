from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os, httpx
from prometheus_fastapi_instrumentator import Instrumentator

ML_URL = os.getenv("ML_SERVICE_URL", "http://localhost:9000")
ORDERS_URL = os.getenv("ORDERS_SERVICE_URL", "http://localhost:7000")

app = FastAPI(title="Gateway Service")

Instrumentator().instrument(app).expose(app)

class PredictIn(BaseModel):
    features: list[float]

@app.get("/health")
def health():
    return {"status": "ok", "service": "gateway"}

@app.get("/orders")
async def orders():
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{ORDERS_URL}/orders", timeout=10)
        r.raise_for_status()
        return r.json()

@app.post("/predict")
async def predict(payload: PredictIn):
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{ML_URL}/predict", json=payload.dict(), timeout=10)
        if r.status_code != 200:
            raise HTTPException(status_code=r.status_code, detail=r.text)
        return r.json()
