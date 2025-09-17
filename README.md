# Cloud‑Native Infrastructure & MLOps Automation (Monorepo)

This repository is a **full, runnable reference project** demonstrating cloud‑native microservices, MLOps automation, and multi‑cloud Infrastructure‑as‑Code (IaC). It includes:

- **Microservices** (FastAPI + Node/Express) with a lightweight **API gateway**
- A simple **ML service** with train/infer endpoints and Prometheus metrics
- **Docker** and **Kubernetes** (manifests for local or cluster deploy)
- **CI/CD** example with GitHub Actions
- **Monitoring**: Prometheus & basic Grafana dashboard JSON
- **IaC** via **Terraform** (AWS) and **CloudFormation** (serverless API + DynamoDB)
- A minimal **React** frontend to call the gateway
- **Serverless** example (Lambda) for event processing

> ⚠️ This is a teaching/reference repo. It runs locally with Docker Compose out of the box. Cloud pieces are illustrative (safe defaults, no credentials).

---

## Monorepo layout

```
.
├─ services/
│  ├─ gateway/               # FastAPI edge service: routes to ml-service & orders-service
│  ├─ ml-service/            # FastAPI + scikit-learn model (train & predict)
│  └─ orders-service/        # Node/Express sample microservice
│
├─ frontend/                 # React (Vite) dashboard calling the gateway
│
├─ k8s/                      # Kubernetes manifests (Deployments, Services, Ingress)
├─ monitoring/               # Prometheus config and Grafana dashboard JSON
│
├─ infra/
│  ├─ terraform/aws/         # Terraform: S3 bucket + ECR repos (example)
│  └─ cloudformation/        # CloudFormation: serverless API (Lambda + DynamoDB + API GW)
│
├─ serverless/               # Lambda function source (for the CFN stack)
└─ .github/workflows/        # CI: build & test & containerize
```

---

## Quickstart (Local)

### Prereqs
- Docker & Docker Compose
- Node 18+ (only if you want to run frontend outside Docker)
- Python 3.10+ (only if you want to run the ML service directly)

### 1) Run everything with Docker Compose

```bash
docker compose up --build
```
Services:
- Gateway: http://localhost:8000/docs
- ML Service: http://localhost:9000/docs
- Orders Service: http://localhost:7000/health
- Frontend (Vite dev): http://localhost:5173

### 2) Try it out

**Predict** (via gateway → ml-service):

```bash
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"features":[5.1,3.5,1.4,0.2]}'
```

**Mock orders** (via gateway → orders-service):
```bash
curl http://localhost:8000/orders
```

**Train the model** (simple example):
```bash
curl -X POST http://localhost:9000/train
```

**Metrics**:
- Gateway: http://localhost:8000/metrics
- ML: http://localhost:9000/metrics

---

## Cloud‑Microservices & MLOps (Conceptual Overview)

- **Microservices**: Each service is independently buildable/deployable (own Dockerfile, health, metrics). The gateway fronts internal services and can apply auth/rate‑limit.
- **MLOps**: `ml-service` exposes `/train` and `/predict`, persisting a tiny scikit‑learn model artifact. A CI job shows how you’d build, test, and publish images/artifacts.
- **Observability**: Prometheus scrapes `/metrics`. A sample Grafana dashboard JSON is included.
- **IaC**:
  - **Terraform (AWS)** creates a demo S3 bucket and ECR repos you’d push images to.
  - **CloudFormation** shows a fully serverless API: API Gateway → Lambda → DynamoDB for event capture—handy for async processing, audit logs, or fallback when services are down.
- **Kubernetes**: Manifests deploy the services; plug into an Ingress if desired.

> Use this repo to **learn patterns** and as a starting point for production. Add secrets management (e.g., SSM, Vault), real CD (ArgoCD), stronger auth, tracing, etc.

---

## Run services individually (optional)

**Gateway**
```bash
cd services/gateway
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

**ML‑Service**
```bash
cd services/ml-service
pip install -r requirements.txt
python train.py         # one-off local training
uvicorn app:app --reload --port 9000
```

**Orders‑Service**
```bash
cd services/orders-service
npm install
npm run dev
```

**Frontend**
```bash
cd frontend
npm install
npm run dev -- --host
```

---

## Kubernetes (optional)

Apply basic manifests to a local cluster (e.g., kind, minikube):
```bash
kubectl apply -f k8s/
```
Then port‑forward or configure an Ingress.

---

## Terraform (AWS example)

**NOTE:** Edit bucket/repo names to be globally unique, and configure AWS credentials first.

```bash
cd infra/terraform/aws
terraform init
terraform plan
terraform apply
```

Creates:
- S3 bucket for ML artifacts
- ECR repos for the 3 services

---

## CloudFormation (Serverless API)

```bash
cd infra/cloudformation
# Package & deploy with AWS SAM or aws cloudformation deploy
# Example (SAM):
# sam build && sam deploy --guided
```

Creates:
- DynamoDB table
- Lambda function (in `serverless/`)
- API Gateway with route `/ingest`

---

## CI/CD

See `.github/workflows/ci.yaml`. On each push:
- Lint/format
- Run unit tests (very basic)
- Build Docker images (tagged by SHA)

Add registry auth (GHCR/ECR) as secrets to enable real pushes.

---

## License

MIT — use freely for learning and starter projects.
