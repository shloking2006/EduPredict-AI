"""
EduPredict AI - Prediction Module
Loads trained model and makes predictions for new students.
"""

import os
import joblib
import pandas as pd
import numpy as np

MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models")

RISK_INFO = {
    "Low": {
        "risk_level": "High Risk",
        "color": "red",
        "emoji": "🔴",
        "description": "This student may need significant academic support. "
                       "Consider tutoring, mentoring, or counseling services.",
        "recommendations": [
            "Schedule regular meetings with academic advisor",
            "Enroll in tutoring or peer-study groups",
            "Review study habits and time management",
            "Consider reducing extracurricular commitments",
            "Seek help early — do not wait until exams",
        ],
    },
    "Medium": {
        "risk_level": "Moderate Risk",
        "color": "orange",
        "emoji": "🟡",
        "description": "This student is performing at an average level. "
                       "With targeted effort, performance can improve.",
        "recommendations": [
            "Focus on weaker subjects with extra study time",
            "Participate actively in class discussions",
            "Form or join study groups",
            "Set specific, measurable academic goals",
            "Use office hours for clarification",
        ],
    },
    "High": {
        "risk_level": "Low Risk",
        "color": "green",
        "emoji": "🟢",
        "description": "This student is performing well. "
                       "Encourage continued effort and advanced opportunities.",
        "recommendations": [
            "Explore advanced courses or research projects",
            "Consider mentoring fellow students",
            "Participate in academic competitions",
            "Maintain healthy work-life balance",
            "Set goals for further academic excellence",
        ],
    },
}


def load_model(model_path=None):
    """
    Load a saved model pipeline from disk.
    
    Args:
        model_path: Path to the .joblib file. If None, loads the best model.
    
    Returns:
        The loaded sklearn Pipeline.
    """
    if model_path is None:
        model_path = os.path.join(MODELS_DIR, "best_model.joblib")
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Model not found at {model_path}. "
            f"Run train_model.py first to train and save the model."
        )
    
    model = joblib.load(model_path)
    return model


def load_model_metadata(metadata_path=None):
    """
    Load saved model metadata (metrics, feature names, etc.).
    """
    if metadata_path is None:
        metadata_path = os.path.join(MODELS_DIR, "model_metadata.joblib")
    
    if not os.path.exists(metadata_path):
        return None
    
    return joblib.load(metadata_path)


def predict_performance(model, student_data):
    """
    Make a prediction for a single student.
    
    Args:
        model: Trained sklearn Pipeline.
        student_data: dict or pd.DataFrame with student features.
    
    Returns:
        dict with prediction, probabilities (if available), and risk info.
    """
    if isinstance(student_data, dict):
        student_df = pd.DataFrame([student_data])
    else:
        student_df = student_data.copy()
    
    prediction = model.predict(student_df)[0]
    
    result = {
        "prediction": prediction,
        "risk_info": get_risk_category(prediction),
    }
    
    # Try to get prediction probabilities
    if hasattr(model, "predict_proba"):
        try:
            probas = model.predict_proba(student_df)[0]
            classes = model.classes_
            result["probabilities"] = dict(zip(classes, probas))
        except Exception:
            result["probabilities"] = None
    else:
        result["probabilities"] = None
    
    return result


def get_risk_category(prediction):
    """
    Map a prediction label to a risk category with description.
    
    Args:
        prediction: One of 'Low', 'Medium', 'High'.
    
    Returns:
        dict with risk_level, color, emoji, description, recommendations.
    """
    return RISK_INFO.get(prediction, RISK_INFO["Medium"])
