from fastapi import FastAPI
from pydantic import BaseModel
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
import joblib, os
from prometheus_fastapi_instrumentator import Instrumentator

MODEL_PATH = os.getenv("MODEL_PATH", "model.pkl")

app = FastAPI(title="ML Service")
Instrumentator().instrument(app).expose(app)

class PredictIn(BaseModel):
    features: list[float]

def ensure_model():
    if not os.path.exists(MODEL_PATH):
        # train simple model
        data = load_iris()
        X, y = data.data, data.target
        clf = LogisticRegression(max_iter=200)
        clf.fit(X, y)
        joblib.dump(clf, MODEL_PATH)

@app.on_event("startup")
def startup():
    ensure_model()

@app.get("/health")
def health():
    return {"status": "ok", "service": "ml"}

@app.post("/train")
def train():
    data = load_iris()
    X, y = data.data, data.target
    clf = LogisticRegression(max_iter=200)
    clf.fit(X, y)
    joblib.dump(clf, MODEL_PATH)
    return {"status": "trained", "classes": list(map(int, clf.classes_))}

@app.post("/predict")
def predict(payload: PredictIn):
    clf = joblib.load(MODEL_PATH)
    import numpy as np
    X = np.array(payload.features).reshape(1, -1)
    pred = int(clf.predict(X)[0])
    prob = clf.predict_proba(X)[0].tolist()
    return {"prediction": pred, "probabilities": prob}
