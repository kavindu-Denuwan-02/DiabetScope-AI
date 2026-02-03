"""
predict.py
──────────
Core prediction logic for both classification and regression.

Flow:
  1. Receive validated Pydantic input
  2. Engineer interaction features (same as training notebooks)
  3. Apply scaler (fit during training)
  4. Run model.predict() / model.predict_proba()
  5. Format response

WHY separate this from main.py?
  • Separation of concerns (route logic vs ML logic)
  • Easier to unit test
  • Cleaner codebase
"""

import numpy as np
from schemas import DiabetesInput, GlucoseInput, DiabetesResponse, GlucoseResponse
from model_loader import model_loader


# ═══════════════════════════════════════════════════════════════════
# HELPER: Feature Engineering
# ═══════════════════════════════════════════════════════════════════

def engineer_classification_features(data: DiabetesInput) -> np.ndarray:
    """
    Convert DiabetesInput to feature array with interaction terms.
    
    Feature order (must match training notebooks):
      0. Pregnancies
      1. Glucose
      2. BloodPressure
      3. SkinThickness
      4. Insulin
      5. BMI
      6. DiabetesPedigreeFunction
      7. Age
      8. Age_Glucose          ← interaction
      9. BMI_Age              ← interaction
     10. Glucose_BMI          ← interaction
    
    Returns:
        np.ndarray of shape (1, 11)
    """
    # Original 8 features
    pregnancies = data.pregnancies
    glucose = data.glucose
    blood_pressure = data.blood_pressure
    skin_thickness = data.skin_thickness
    insulin = data.insulin
    bmi = data.bmi
    diabetes_pedigree = data.diabetes_pedigree
    age = data.age
    
    # Engineer 3 interaction terms (same as notebooks)
    age_glucose = age * glucose
    bmi_age = bmi * age
    glucose_bmi = glucose * bmi
    
    # Assemble feature vector
    features = np.array([[
        pregnancies,
        glucose,
        blood_pressure,
        skin_thickness,
        insulin,
        bmi,
        diabetes_pedigree,
        age,
        age_glucose,
        bmi_age,
        glucose_bmi
    ]])
    
    return features


def engineer_regression_features(data: GlucoseInput) -> np.ndarray:
    """
    Convert GlucoseInput to feature array.
    
    NOTE: Glucose is the TARGET for regression, so it's NOT in the input.
    We can't compute the 3 interaction terms that involve glucose.
    
    Feature order (must match training notebooks):
      0. Pregnancies
      1. BloodPressure
      2. SkinThickness
      3. Insulin
      4. BMI
      5. DiabetesPedigreeFunction
      6. Age
      7. BMI_Age              ← only this interaction is computable
    
    ⚠️  IMPORTANT: Check your regression notebook to see which features
        it actually uses. This assumes glucose-free features only.
        
        If your notebook used all 11 features (including glucose interactions),
        you'll need to either:
          a) Retrain the regressor without glucose-dependent features, OR
          b) Require glucose as input for regression (defeats the purpose)
    
    For now, this returns the 8 features that DON'T depend on glucose.
    
    Returns:
        np.ndarray of shape (1, 8)
    """
    pregnancies = data.pregnancies
    blood_pressure = data.blood_pressure
    skin_thickness = data.skin_thickness
    insulin = data.insulin
    bmi = data.bmi
    diabetes_pedigree = data.diabetes_pedigree
    age = data.age
    
    # Only BMI_Age is computable (doesn't need glucose)
    bmi_age = bmi * age
    
    features = np.array([[
        pregnancies,
        blood_pressure,
        skin_thickness,
        insulin,
        bmi,
        diabetes_pedigree,
        age,
        bmi_age
    ]])
    
    return features


# ═══════════════════════════════════════════════════════════════════
# CLASSIFICATION PREDICTION
# ═══════════════════════════════════════════════════════════════════

def predict_diabetes(data: DiabetesInput) -> DiabetesResponse:
    """
    Predict diabetes status (binary classification).
    
    Steps:
      1. Engineer features
      2. Scale features
      3. Predict class + probability
      4. Format response
    
    Args:
        data: Validated DiabetesInput from Pydantic
    
    Returns:
        DiabetesResponse with prediction and probability
    """
    # Get models from singleton
    classifier = model_loader.get_classifier()
    scaler = model_loader.get_classification_scaler()
    
    # 1. Engineer features (11 features including interactions)
    features = engineer_classification_features(data)
    
    # 2. Scale features (same scaler fit during training)
    features_scaled = scaler.transform(features)
    
    # 3. Predict
    prediction_class = classifier.predict(features_scaled)[0]  # 0 or 1
    prediction_proba = classifier.predict_proba(features_scaled)[0]  # [prob_0, prob_1]
    
    # 4. Format response
    label = "Diabetic" if prediction_class == 1 else "Non-Diabetic"
    probability = float(prediction_proba[1])  # probability of class 1 (diabetic)
    
    return DiabetesResponse(
        prediction=label,
        probability=round(probability, 4)
    )


# ═══════════════════════════════════════════════════════════════════
# REGRESSION PREDICTION
# ═══════════════════════════════════════════════════════════════════

def predict_glucose(data: GlucoseInput) -> GlucoseResponse:
    """
    Predict glucose level (regression).
    
    Steps:
      1. Engineer features (without glucose)
      2. Scale features
      3. Predict continuous value
      4. Format response
    
    Args:
        data: Validated GlucoseInput from Pydantic
    
    Returns:
        GlucoseResponse with predicted glucose level
    """
    # Get models from singleton
    regressor = model_loader.get_regressor()
    scaler = model_loader.get_regression_scaler()
    
    # 1. Engineer features (8 features, no glucose-dependent interactions)
    features = engineer_regression_features(data)
    
    # 2. Scale features
    features_scaled = scaler.transform(features)
    
    # 3. Predict
    predicted_glucose = regressor.predict(features_scaled)[0]
    
    # 4. Format response
    return GlucoseResponse(
        predicted_glucose=round(float(predicted_glucose), 2)
    )