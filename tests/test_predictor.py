"""
EduPredict AI - Tests for Prediction Functions
"""

import os
import sys
import pytest
import pandas as pd

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from src.predictor import load_model, predict_performance, get_risk_category, RISK_INFO


class TestRiskCategory:
    """Test the risk category mapping."""
    
    def test_low_performance_high_risk(self):
        """Low performance should map to High Risk."""
        risk = get_risk_category("Low")
        assert risk["risk_level"] == "High Risk"
        assert risk["color"] == "red"
    
    def test_medium_performance_moderate_risk(self):
        """Medium performance should map to Moderate Risk."""
        risk = get_risk_category("Medium")
        assert risk["risk_level"] == "Moderate Risk"
        assert risk["color"] == "orange"
    
    def test_high_performance_low_risk(self):
        """High performance should map to Low Risk."""
        risk = get_risk_category("High")
        assert risk["risk_level"] == "Low Risk"
        assert risk["color"] == "green"
    
    def test_risk_has_recommendations(self):
        """Each risk category should have recommendations."""
        for label in ["Low", "Medium", "High"]:
            risk = get_risk_category(label)
            assert "recommendations" in risk
            assert len(risk["recommendations"]) > 0
    
    def test_risk_has_description(self):
        """Each risk category should have a description."""
        for label in ["Low", "Medium", "High"]:
            risk = get_risk_category(label)
            assert "description" in risk
            assert len(risk["description"]) > 0
    
    def test_unknown_category_defaults(self):
        """Unknown category should default to Medium."""
        risk = get_risk_category("Unknown")
        assert risk["risk_level"] == "Moderate Risk"


class TestLoadModel:
    """Test model loading."""
    
    def test_model_file_exists(self):
        """Check that the trained model file exists."""
        model_path = os.path.join(PROJECT_ROOT, "models", "best_model.joblib")
        assert os.path.exists(model_path), \
            "Model file not found. Run train_model.py first."
    
    def test_load_model_success(self):
        """Model should load without error."""
        model = load_model()
        assert model is not None
    
    def test_model_has_predict(self):
        """Loaded model should have a predict method."""
        model = load_model()
        assert hasattr(model, "predict")
    
    def test_model_has_predict_proba(self):
        """Loaded model should have predict_proba method."""
        model = load_model()
        assert hasattr(model, "predict_proba")


class TestPrediction:
    """Test the prediction function."""
    
    @pytest.fixture
    def model(self):
        """Load the trained model."""
        return load_model()
    
    @pytest.fixture
    def sample_student(self):
        """Create a sample student data dict."""
        return {
            "school": "GP", "sex": "F", "age": 17, "address": "U",
            "famsize": "GT3", "Pstatus": "T", "Medu": 3, "Fedu": 3,
            "Mjob": "services", "Fjob": "other", "reason": "course",
            "guardian": "mother", "traveltime": 1, "studytime": 2,
            "failures": 0, "schoolsup": "no", "famsup": "yes",
            "paid": "no", "activities": "yes", "nursery": "yes",
            "higher": "yes", "internet": "yes", "romantic": "no",
            "famrel": 4, "freetime": 3, "goout": 3, "Dalc": 1,
            "Walc": 1, "health": 3, "absences": 4, "G1": 12, "G2": 13,
        }
    
    def test_prediction_returns_dict(self, model, sample_student):
        """Prediction should return a dictionary."""
        result = predict_performance(model, sample_student)
        assert isinstance(result, dict)
    
    def test_prediction_has_required_keys(self, model, sample_student):
        """Result should have prediction and risk_info keys."""
        result = predict_performance(model, sample_student)
        assert "prediction" in result
        assert "risk_info" in result
        assert "probabilities" in result
    
    def test_prediction_valid_category(self, model, sample_student):
        """Prediction should be one of Low, Medium, High."""
        result = predict_performance(model, sample_student)
        assert result["prediction"] in ["Low", "Medium", "High"]
    
    def test_probabilities_sum_to_one(self, model, sample_student):
        """If probabilities are returned, they should sum to approximately 1."""
        result = predict_performance(model, sample_student)
        if result["probabilities"] is not None:
            total = sum(result["probabilities"].values())
            assert abs(total - 1.0) < 0.01
    
    def test_prediction_with_dataframe(self, model, sample_student):
        """Prediction should work with a DataFrame input too."""
        df = pd.DataFrame([sample_student])
        result = predict_performance(model, df)
        assert result["prediction"] in ["Low", "Medium", "High"]
    
    def test_low_performing_student(self, model):
        """A student with very low grades should likely be predicted as Low."""
        student = {
            "school": "GP", "sex": "M", "age": 18, "address": "R",
            "famsize": "GT3", "Pstatus": "A", "Medu": 1, "Fedu": 1,
            "Mjob": "other", "Fjob": "other", "reason": "other",
            "guardian": "other", "traveltime": 3, "studytime": 1,
            "failures": 3, "schoolsup": "no", "famsup": "no",
            "paid": "no", "activities": "no", "nursery": "no",
            "higher": "no", "internet": "no", "romantic": "yes",
            "famrel": 1, "freetime": 5, "goout": 5, "Dalc": 4,
            "Walc": 5, "health": 1, "absences": 30, "G1": 4, "G2": 3,
        }
        result = predict_performance(model, student)
        # With G1=4, G2=3, this should very likely be "Low"
        assert result["prediction"] == "Low"
    
    def test_high_performing_student(self, model):
        """A student with high grades should likely be predicted as High."""
        student = {
            "school": "GP", "sex": "F", "age": 16, "address": "U",
            "famsize": "LE3", "Pstatus": "T", "Medu": 4, "Fedu": 4,
            "Mjob": "teacher", "Fjob": "health", "reason": "reputation",
            "guardian": "mother", "traveltime": 1, "studytime": 4,
            "failures": 0, "schoolsup": "no", "famsup": "yes",
            "paid": "yes", "activities": "yes", "nursery": "yes",
            "higher": "yes", "internet": "yes", "romantic": "no",
            "famrel": 5, "freetime": 3, "goout": 2, "Dalc": 1,
            "Walc": 1, "health": 5, "absences": 0, "G1": 18, "G2": 19,
        }
        result = predict_performance(model, student)
        # With G1=18, G2=19, this should very likely be "High"
        assert result["prediction"] == "High"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
