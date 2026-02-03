"""
main.py
───────
FastAPI application entry point.

This file:
  • Creates the FastAPI app
  • Registers all routes
  • Triggers model loading at startup
  • Provides automatic OpenAPI docs at /docs

Run with:
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas import (
    DiabetesInput, DiabetesResponse,
    GlucoseInput, GlucoseResponse,
    HealthResponse
)
from predict import predict_diabetes, predict_glucose
from model_loader import model_loader
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════
# APP INITIALIZATION
# ═══════════════════════════════════════════════════════════════════

app = FastAPI(
    title="DiabetScope-AI API",
    description=(
        "Machine Learning API for diabetes prediction and glucose level estimation.\n\n"
        "**Endpoints:**\n"
        "- `POST /predict/diabetes` → Binary classification (Diabetic / Non-Diabetic)\n"
        "- `POST /predict/glucose` → Regression (Predicted glucose level)\n"
        "- `GET /health` → Health check\n\n"
        "**Models:**\n"
        "- Classification: Best model from 5 experiments (LR, DT, KNN, RF, XGBoost)\n"
        "- Regression: Best model from 5 experiments (Linear, Ridge, Lasso, RF, GB)\n\n"
        "All models trained on Pima Indians Diabetes Database (768 samples)."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


# ═══════════════════════════════════════════════════════════════════
# CORS MIDDLEWARE (for mobile/web frontend)
# ═══════════════════════════════════════════════════════════════════

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ═══════════════════════════════════════════════════════════════════
# STARTUP EVENT — Load models once
# ═══════════════════════════════════════════════════════════════════

@app.on_event("startup")
async def startup_event():
    """
    Triggered when FastAPI starts.
    
    The ModelLoader singleton will load all .pkl files from disk
    and cache them in memory. This happens ONCE, not per request.
    """
    logger.info("🚀 Starting DiabetScope-AI API...")
    logger.info("📦 Loading ML models...")
    
    # Force model loading by accessing the singleton
    # (ModelLoader.__init__ loads everything on first instantiation)
    if model_loader.is_loaded():
        logger.info("✅ All models loaded successfully")
    else:
        logger.error("❌ Model loading failed")
        raise RuntimeError("Failed to load ML models at startup")


# ═══════════════════════════════════════════════════════════════════
# HEALTH CHECK
# ═══════════════════════════════════════════════════════════════════

@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        - status: "healthy" if models are loaded
        - message: descriptive message
        - models_loaded: boolean flag
    """
    models_loaded = model_loader.is_loaded()
    
    if models_loaded:
        return HealthResponse(
            status="healthy",
            message="API is running. All models loaded.",
            models_loaded=True
        )
    else:
        return HealthResponse(
            status="unhealthy",
            message="API is running but models failed to load.",
            models_loaded=False
        )


# ═══════════════════════════════════════════════════════════════════
# PREDICTION ENDPOINTS
# ═══════════════════════════════════════════════════════════════════

@app.post(
    "/predict/diabetes",
    response_model=DiabetesResponse,
    tags=["Predictions"],
    summary="Predict diabetes status (classification)"
)
async def diabetes_prediction(data: DiabetesInput):
    """
    Predict whether a patient is diabetic or non-diabetic.
    
    **Input:** 8 clinical features (validated by Pydantic)
    
    **Output:** 
    - `prediction`: "Diabetic" or "Non-Diabetic"
    - `probability`: Probability of being diabetic (0.0 - 1.0)
    
    **Example Request:**
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
    
    **Example Response:**
    ```json
    {
      "prediction": "Diabetic",
      "probability": 0.82
    }
    ```
    """
    try:
        result = predict_diabetes(data)
        logger.info(f"Diabetes prediction: {result.prediction} (p={result.probability:.4f})")
        return result
    
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@app.post(
    "/predict/glucose",
    response_model=GlucoseResponse,
    tags=["Predictions"],
    summary="Predict glucose level (regression)"
)
async def glucose_prediction(data: GlucoseInput):
    """
    Predict blood glucose level in mg/dL.
    
    **Input:** 7 clinical features (glucose excluded since it's the target)
    
    **Output:** 
    - `predicted_glucose`: Continuous glucose level in mg/dL
    
    **Example Request:**
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
    
    **Example Response:**
    ```json
    {
      "predicted_glucose": 138.6
    }
    ```
    """
    try:
        result = predict_glucose(data)
        logger.info(f"Glucose prediction: {result.predicted_glucose:.2f} mg/dL")
        return result
    
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


# ═══════════════════════════════════════════════════════════════════
# ROOT ENDPOINT
# ═══════════════════════════════════════════════════════════════════

@app.get("/", tags=["System"])
async def root():
    """
    API root — redirects to /docs for interactive documentation.
    """
    return {
        "message": "DiabetScope-AI API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "endpoints": {
            "diabetes_prediction": "POST /predict/diabetes",
            "glucose_prediction": "POST /predict/glucose"
        }
    }


# ═══════════════════════════════════════════════════════════════════
# DEVELOPMENT SERVER
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes (dev only)
        log_level="info"
    )