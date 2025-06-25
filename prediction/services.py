import pandas as pd
import joblib
from django.conf import settings
import os

class MLPredictionService:
    """
    Service class to handle ML model operations 
    This encapsulates model loading and prediction logic
    """
    def __init__(self):
        self.model = None
        self.model_columns = None
        self.load_model()

    def load_model(self):
        """
        Load the ML model and model columns at startup
        This is called once when the service is instentiated
        """
        try:
            # load model from joblib file
            model_path = getattr(settings, 'ML_MODEL_PATH', 'notebook3_rf_model.joblib')
            self.model = joblib.load(model_path)
            # load model columns for feature alignment
            columns_path = getattr(settings, "ML_COLUMNS_PATH", 'notebook3_rf_model.joblib')
            with open(columns_path, 'r') as f:
                self.model_columns = [line.strip() for line in f]
        except Exception as e:
            raise Exception(f"failed to load model: {str(e)}")
    def preprocess_data(self, df):
        """
        Apply preprocessing steps from our preprocess.py
        This ensures data is in the same format as training data
        """
        from . import preprocess
        processed = preprocess.binary_cols(df)
        processed = preprocess.fix_cylinderPreference(processed)
        processed = preprocess.ordinal_cols(processed)
        processed = preprocess.remove_unnecessary_cols(processed)
        processed = preprocess.monthlyExpense_col(processed)
        processed = processed.drop(columns=['foodFuelExpensePercent'], errors='ignore')
        processed = preprocess.oneHotEncoding_cols(processed)
        # align columns with trained model
        for col in self.model_columns:
            if col not in processed.columns:
                processed[col]=0
        processed = processed[self.model_columns]
        return processed
    def predict(self, input_data):
        """
        Make prediction using the loaded model
        Returns score and risk category
        """
        try:
            df = pd.DataFrame([input_data])
            processed = self.preprocess_data(df)
            prediction = self.model.predict(processed)
            score = float(prediction[0])
            # Rescale to CIBIL-like score (300-900)
            cibil_score = 300 + score * 600
            if cibil_score < 400:
                risk_category = "High Risk"
            elif cibil_score <= 700:
                risk_category = "Medium Risk"
            else:
                risk_category = "Low Risk"
            return {
                'score': cibil_score,
                'risk_category': risk_category
            }
        except Exception as e:
            raise Exception(f"Prediction failed: {str(e)}")
        
# craete singleton instance-loaded once when django starts
ml_service = MLPredictionService()