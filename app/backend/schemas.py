"""
schemas.py
──────────
Pydantic models for input validation.

WHY Pydantic?
  • Automatic type checking
  • Clear error messages for invalid input
  • OpenAPI documentation generation
  • Industry-standard practice

Each field has validation constraints matching the Pima dataset's
valid ranges. This prevents garbage input from reaching your ML models.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional


# ═══════════════════════════════════════════════════════════════════
# CLASSIFICATION INPUT — Diabetes Prediction
# ═══════════════════════════════════════════════════════════════════

class DiabetesInput(BaseModel):
    """
    Input schema for diabetes binary classification.
    
    All 8 original features from the Pima Indians Diabetes dataset.
    Validation ranges based on dataset profiling.
    """
    pregnancies: int = Field(
        ...,
        ge=0,
        le=20,
        description="Number of times pregnant (0-20)",
        example=2
    )
    
    glucose: float = Field(
        ...,
        gt=0,
        le=250,
        description="Plasma glucose concentration (mg/dL). Must be > 0.",
        example=130.0
    )
    
    blood_pressure: float = Field(
        ...,
        gt=0,
        le=150,
        description="Diastolic blood pressure (mm Hg). Must be > 0.",
        example=85.0
    )
    
    skin_thickness: float = Field(
        ...,
        ge=0,
        le=100,
        description="Triceps skin fold thickness (mm). 0 = not measured.",
        example=25.0
    )
    
    insulin: float = Field(
        ...,
        ge=0,
        le=900,
        description="2-Hour serum insulin (μU/mL). 0 = not measured.",
        example=120.0
    )
    
    bmi: float = Field(
        ...,
        gt=0,
        le=70,
        description="Body Mass Index (kg/m²). Must be > 0.",
        example=32.1
    )
    
    diabetes_pedigree: float = Field(
        ...,
        gt=0,
        le=3.0,
        description="Diabetes pedigree function (genetic score).",
        example=0.45
    )
    
    age: int = Field(
        ...,
        ge=18,
        le=120,
        description="Age in years (18-120).",
        example=45
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "pregnancies": 2,
                "glucose": 130.0,
                "blood_pressure": 85.0,
                "skin_thickness": 25.0,
                "insulin": 120.0,
                "bmi": 32.1,
                "diabetes_pedigree": 0.45,
                "age": 45
            }
        }


# ═══════════════════════════════════════════════════════════════════
# REGRESSION INPUT — Glucose Prediction
# ═══════════════════════════════════════════════════════════════════

class GlucoseInput(BaseModel):
    """
    Input schema for glucose level regression.
    
    Same as DiabetesInput but WITHOUT the glucose field
    (since we're predicting it).
    """
    pregnancies: int = Field(
        ...,
        ge=0,
        le=20,
        description="Number of times pregnant (0-20)",
        example=2
    )
    
    blood_pressure: float = Field(
        ...,
        gt=0,
        le=150,
        description="Diastolic blood pressure (mm Hg). Must be > 0.",
        example=85.0
    )
    
    skin_thickness: float = Field(
        ...,
        ge=0,
        le=100,
        description="Triceps skin fold thickness (mm). 0 = not measured.",
        example=25.0
    )
    
    insulin: float = Field(
        ...,
        ge=0,
        le=900,
        description="2-Hour serum insulin (μU/mL). 0 = not measured.",
        example=120.0
    )
    
    bmi: float = Field(
        ...,
        gt=0,
        le=70,
        description="Body Mass Index (kg/m²). Must be > 0.",
        example=32.1
    )
    
    diabetes_pedigree: float = Field(
        ...,
        gt=0,
        le=3.0,
        description="Diabetes pedigree function (genetic score).",
        example=0.45
    )
    
    age: int = Field(
        ...,
        ge=18,
        le=120,
        description="Age in years (18-120).",
        example=45
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "pregnancies": 2,
                "blood_pressure": 85.0,
                "skin_thickness": 25.0,
                "insulin": 120.0,
                "bmi": 32.1,
                "diabetes_pedigree": 0.45,
                "age": 45
            }
        }


# ═══════════════════════════════════════════════════════════════════
# RESPONSE SCHEMAS
# ═══════════════════════════════════════════════════════════════════

class DiabetesResponse(BaseModel):
    """
    Response schema for diabetes prediction.
    """
    prediction: str = Field(
        ...,
        description="Either 'Diabetic' or 'Non-Diabetic'",
        example="Diabetic"
    )
    
    probability: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Probability of being diabetic (0.0 - 1.0)",
        example=0.82
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "prediction": "Diabetic",
                "probability": 0.82
            }
        }


class GlucoseResponse(BaseModel):
    """
    Response schema for glucose prediction.
    """
    predicted_glucose: float = Field(
        ...,
        description="Predicted glucose level in mg/dL",
        example=138.6
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "predicted_glucose": 138.6
            }
        }


class HealthResponse(BaseModel):
    """
    Response schema for health check endpoint.
    """
    status: str
    message: str
    models_loaded: bool