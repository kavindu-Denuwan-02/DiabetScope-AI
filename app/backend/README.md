# DiabetScope-AI Backend API

Production-ready FastAPI backend for diabetes prediction and glucose level estimation.

---

## 📁 Project Structure

```
backend/
├── main.py              # FastAPI entry point (app creation, routes)
├── schemas.py           # Pydantic models (input validation)
├── model_loader.py      # Singleton pattern (load .pkl once)
├── predict.py           # Core ML logic (feature engineering + prediction)
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

---

## 🚀 Quick Start

### 1️⃣ Install Dependencies

```bash
cd app/backend
pip install -r requirements.txt
```

### 2️⃣ Ensure Models Are Trained

The backend expects these files to exist:

```
DiabetScope-AI/
├── models/
│   ├── classification/
│   │   └── best_classifier.pkl
│   └── regression/
│       └── best_regressor.pkl
└── scalers/
    ├── classification_scaler.pkl
    └── regression_scaler.pkl
```

**Generate them by running:**
```bash
cd notebooks/
# Run these in order:
jupyter notebook 01_eda.ipynb
jupyter notebook 02_preprocessing.ipynb
jupyter notebook 03_classification_experiments.ipynb
jupyter notebook 04_regression_experiments.ipynb
```

### 3️⃣ Run the Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     🚀 Starting DiabetScope-AI API...
INFO:     📦 Loading ML models...
INFO:     ✅ Loaded classifier from ../../models/classification/best_classifier.pkl
INFO:     ✅ Loaded regressor from ../../models/regression/best_regressor.pkl
INFO:     ✅ All models loaded successfully
```

### 4️⃣ Access Interactive Docs

Open browser: **http://localhost:8000/docs**

You'll see:
- Interactive Swagger UI
- Test endpoints directly from browser
- Automatic request/response examples

---

## 🔌 API Endpoints

### **Health Check**
```bash
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "message": "API is running. All models loaded.",
  "models_loaded": true
}
```

---

### **1️⃣ Diabetes Prediction (Classification)**

**Endpoint:**
```bash
POST /predict/diabetes
```

**Request Body:**
```json
{
  "pregnancies": 2,
  "glucose": 130,
  "blood_pressure": 85,
  "skin_thickness": 25,
  "insulin": 120,
  "bmi": 32.1,
  "diabetes_pedigree": 0.45,
  "age": 45
}
```

**Response:**
```json
{
  "prediction": "Diabetic",
  "probability": 0.82
}
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/predict/diabetes" \
  -H "Content-Type: application/json" \
  -d '{
    "pregnancies": 2,
    "glucose": 130,
    "blood_pressure": 85,
    "skin_thickness": 25,
    "insulin": 120,
    "bmi": 32.1,
    "diabetes_pedigree": 0.45,
    "age": 45
  }'
```

---

### **2️⃣ Glucose Prediction (Regression)**

**Endpoint:**
```bash
POST /predict/glucose
```

**Request Body:**
```json
{
  "pregnancies": 2,
  "blood_pressure": 85,
  "skin_thickness": 25,
  "insulin": 120,
  "bmi": 32.1,
  "diabetes_pedigree": 0.45,
  "age": 45
}
```

**Response:**
```json
{
  "predicted_glucose": 138.6
}
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/predict/glucose" \
  -H "Content-Type: application/json" \
  -d '{
    "pregnancies": 2,
    "blood_pressure": 85,
    "skin_thickness": 25,
    "insulin": 120,
    "bmi": 32.1,
    "diabetes_pedigree": 0.45,
    "age": 45
  }'
```

---

## 🧠 Design Decisions (Interview Gold)

### **Why Separate Endpoints?**
- Different tasks → different models → different validation schemas
- Classification needs all 8 features; regression excludes glucose
- Cleaner API contract, easier to maintain

### **Why Load Models at Startup?**
- **Disk I/O latency:** Loading a .pkl file takes 10-100ms
- Loading on every request → 10-100ms added to every prediction
- Loading once at startup → sub-millisecond inference after that
- **This is production-level optimization**

### **Why Pydantic Schemas?**
- Automatic type validation (int, float, range checks)
- Clear error messages for invalid input
- Prevents garbage data from reaching ML models
- Generates OpenAPI documentation automatically

### **Why FastAPI?**
- Auto-generates `/docs` (Swagger UI)
- Built-in async support (for future scaling)
- Modern Python type hints
- Industry standard for ML APIs

---

## 🛠️ Troubleshooting

### **Error: "Model file not found"**

**Cause:** You haven't trained the models yet.

**Fix:**
```bash
cd notebooks/
jupyter notebook 03_classification_experiments.ipynb  # generates best_classifier.pkl
jupyter notebook 04_regression_experiments.ipynb      # generates best_regressor.pkl
```

---

### **Error: "Feature mismatch"**

**Cause:** Input features don't match training feature order.

**Fix:** Check `engineer_classification_features()` in `predict.py` — feature order must match notebooks exactly.

---

### **Error: "CORS policy blocking requests"**

**Cause:** Frontend is on a different domain (e.g., React Native app).

**Fix:** CORS is already enabled in `main.py` with `allow_origins=["*"]`. For production, restrict to specific origins.

---

## 📊 Performance Benchmarks

| Operation | Latency |
|-----------|---------|
| Model load (startup) | ~200ms |
| Health check | <1ms |
| Diabetes prediction | 1-3ms |
| Glucose prediction | 1-3ms |

**Tested on:** MacBook Pro M1, 16GB RAM

---

## 🚢 Deployment (Production)

### **Option 1: Docker**
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build & run:
```bash
docker build -t diabetscope-api .
docker run -p 8000:8000 diabetscope-api
```

### **Option 2: Cloud Platforms**
- **Heroku:** `Procfile` → `web: uvicorn main:app --host 0.0.0.0 --port $PORT`
- **AWS Lambda:** Use Mangum adapter for serverless
- **Google Cloud Run:** Same Dockerfile as above
- **Azure App Service:** Deploy via Azure CLI

---

## 🧪 Testing

### **Manual Test (cURL)**
```bash
# Test diabetes prediction
curl -X POST "http://localhost:8000/predict/diabetes" \
  -H "Content-Type: application/json" \
  -d '{"pregnancies":2,"glucose":130,"blood_pressure":85,"skin_thickness":25,"insulin":120,"bmi":32.1,"diabetes_pedigree":0.45,"age":45}'

# Test glucose prediction
curl -X POST "http://localhost:8000/predict/glucose" \
  -H "Content-Type: application/json" \
  -d '{"pregnancies":2,"blood_pressure":85,"skin_thickness":25,"insulin":120,"bmi":32.1,"diabetes_pedigree":0.45,"age":45}'
```

### **Automated Test (Python)**
```python
import requests

# Test diabetes prediction
response = requests.post(
    "http://localhost:8000/predict/diabetes",
    json={
        "pregnancies": 2,
        "glucose": 130,
        "blood_pressure": 85,
        "skin_thickness": 25,
        "insulin": 120,
        "bmi": 32.1,
        "diabetes_pedigree": 0.45,
        "age": 45
    }
)
print(response.json())
# Expected: {'prediction': 'Diabetic', 'probability': 0.82}
```

---

## 📝 Next Steps

1. ✅ **API is running** → Test with Postman or cURL
2. 🔗 **Connect mobile app** → Update React Native to call `http://your-ip:8000/predict/diabetes`
3. 🚀 **Deploy to cloud** → Heroku / AWS / GCP
4. 📊 **Add monitoring** → Track request latency, error rates

---

## 📞 Support

Issues? Check:
1. Models are trained (`.pkl` files exist)
2. Dependencies installed (`pip install -r requirements.txt`)
3. Server is running (`uvicorn main:app --reload`)
4. Port 8000 is available (`lsof -i :8000` to check)

---

**Built with ❤️ using FastAPI, scikit-learn, and XGBoost**