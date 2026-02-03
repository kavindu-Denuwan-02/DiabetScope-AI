"""
model_loader.py
───────────────
Singleton pattern for loading ML models and scalers at startup.

WHY load at startup instead of on every request?
  • Disk I/O is expensive (10-100ms per .pkl load)
  • Loading on every request = massive latency
  • Loading once = sub-millisecond inference

This is an industry-standard optimization that demonstrates
you understand production ML deployment.
"""

import joblib
import os
from typing import Optional, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelLoader:
    """
    Singleton class to load and cache ML models.
    
    Loads once when the FastAPI app starts, then serves
    from memory for all subsequent requests.
    """
    
    _instance: Optional['ModelLoader'] = None
    _initialized: bool = False
    
    def __new__(cls):
        """Singleton pattern — only one instance ever exists."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Load models only on first instantiation."""
        if not ModelLoader._initialized:
            self._load_models()
            ModelLoader._initialized = True
    
    def _load_models(self):
        """
        Load all .pkl files from the models/ and scalers/ directories.
        
        Expected file structure (relative to backend/):
            ../../models/classification/best_classifier.pkl
            ../../models/regression/best_regressor.pkl
            ../../scalers/classification_scaler.pkl
            ../../scalers/regression_scaler.pkl
        """
        # Paths relative to backend/ directory
        base_path = os.path.dirname(os.path.abspath(__file__))
        root_path = os.path.join(base_path, '..', '..')
        
        try:
            # ────────────────────────────────────────────────────────
            # CLASSIFICATION MODEL
            # ────────────────────────────────────────────────────────
            classifier_path = os.path.join(
                root_path, 'models', 'classification', 'best_classifier.pkl'
            )
            self.classifier = joblib.load(classifier_path)
            logger.info(f"✅ Loaded classifier from {classifier_path}")
            
            # ────────────────────────────────────────────────────────
            # REGRESSION MODEL
            # ────────────────────────────────────────────────────────
            regressor_path = os.path.join(
                root_path, 'models', 'regression', 'best_regressor.pkl'
            )
            self.regressor = joblib.load(regressor_path)
            logger.info(f"✅ Loaded regressor from {regressor_path}")
            
            # ────────────────────────────────────────────────────────
            # CLASSIFICATION SCALER
            # ────────────────────────────────────────────────────────
            classification_scaler_path = os.path.join(
                root_path, 'scalers', 'classification_scaler.pkl'
            )
            self.classification_scaler = joblib.load(classification_scaler_path)
            logger.info(f"✅ Loaded classification scaler from {classification_scaler_path}")
            
            # ────────────────────────────────────────────────────────
            # REGRESSION SCALER
            # ────────────────────────────────────────────────────────
            regression_scaler_path = os.path.join(
                root_path, 'scalers', 'regression_scaler.pkl'
            )
            self.regression_scaler = joblib.load(regression_scaler_path)
            logger.info(f"✅ Loaded regression scaler from {regression_scaler_path}")
            
            logger.info("🎉 All models and scalers loaded successfully")
            
        except FileNotFoundError as e:
            logger.error(f"❌ Model file not found: {e}")
            logger.error("Make sure you've run the notebooks to generate .pkl files")
            raise
        except Exception as e:
            logger.error(f"❌ Error loading models: {e}")
            raise
    
    def get_classifier(self) -> Any:
        """Return the loaded classification model."""
        return self.classifier
    
    def get_regressor(self) -> Any:
        """Return the loaded regression model."""
        return self.regressor
    
    def get_classification_scaler(self) -> Any:
        """Return the scaler for classification features."""
        return self.classification_scaler
    
    def get_regression_scaler(self) -> Any:
        """Return the scaler for regression features."""
        return self.regression_scaler
    
    def is_loaded(self) -> bool:
        """Check if all models are loaded."""
        return all([
            hasattr(self, 'classifier'),
            hasattr(self, 'regressor'),
            hasattr(self, 'classification_scaler'),
            hasattr(self, 'regression_scaler')
        ])


# ═══════════════════════════════════════════════════════════════════
# Global singleton instance
# ═══════════════════════════════════════════════════════════════════

model_loader = ModelLoader()