"""
EduPredict AI - Tests for Preprocessing Functions
"""

import os
import sys
import pytest
import pandas as pd
import numpy as np

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from src.preprocessing import categorize_grade, clean_data, prepare_features_and_target, create_preprocessor
from src.data_loader import load_student_data, get_categorical_features, get_numerical_features


class TestCategorizeGrade:
    """Test the grade categorization function."""
    
    def test_low_grades(self):
        """Grades 0-9 should be categorized as Low."""
        assert categorize_grade(0) == "Low"
        assert categorize_grade(5) == "Low"
        assert categorize_grade(9) == "Low"
    
    def test_medium_grades(self):
        """Grades 10-14 should be categorized as Medium."""
        assert categorize_grade(10) == "Medium"
        assert categorize_grade(12) == "Medium"
        assert categorize_grade(14) == "Medium"
    
    def test_high_grades(self):
        """Grades 15-20 should be categorized as High."""
        assert categorize_grade(15) == "High"
        assert categorize_grade(18) == "High"
        assert categorize_grade(20) == "High"
    
    def test_boundary_values(self):
        """Test exact boundary values between categories."""
        assert categorize_grade(9) == "Low"
        assert categorize_grade(10) == "Medium"
        assert categorize_grade(14) == "Medium"
        assert categorize_grade(15) == "High"


class TestCleanData:
    """Test the data cleaning function."""
    
    def test_no_missing_values(self):
        """UCI dataset has no missing values, so cleaning should preserve all rows."""
        df = load_student_data()
        df_clean = clean_data(df)
        assert df_clean.isnull().sum().sum() == 0
    
    def test_handles_missing_values(self):
        """Test that missing values are handled correctly."""
        df = load_student_data()
        # Introduce some missing values
        df_with_na = df.copy()
        df_with_na.loc[0, "age"] = np.nan
        df_with_na.loc[1, "school"] = np.nan
        
        df_clean = clean_data(df_with_na)
        assert df_clean.isnull().sum().sum() == 0
    
    def test_valid_grade_range(self):
        """Cleaned data should only contain G3 values between 0 and 20."""
        df = load_student_data()
        df_clean = clean_data(df)
        assert df_clean["G3"].min() >= 0
        assert df_clean["G3"].max() <= 20
    
    def test_returns_dataframe(self):
        """clean_data should return a pandas DataFrame."""
        df = load_student_data()
        result = clean_data(df)
        assert isinstance(result, pd.DataFrame)


class TestPrepareFeatures:
    """Test the feature/target preparation function."""
    
    def test_target_categories(self):
        """Target should only contain Low, Medium, High."""
        df = load_student_data()
        X, y = prepare_features_and_target(df)
        assert set(y.unique()).issubset({"Low", "Medium", "High"})
    
    def test_feature_columns(self):
        """Features should not contain the target column G3."""
        df = load_student_data()
        X, y = prepare_features_and_target(df)
        assert "G3" not in X.columns
    
    def test_feature_count(self):
        """Features should include all categorical and numerical features."""
        df = load_student_data()
        X, y = prepare_features_and_target(df)
        expected_cols = get_categorical_features() + get_numerical_features()
        assert list(X.columns) == expected_cols
    
    def test_same_length(self):
        """X and y should have the same number of rows."""
        df = load_student_data()
        X, y = prepare_features_and_target(df)
        assert len(X) == len(y)


class TestPreprocessor:
    """Test the preprocessing pipeline creation."""
    
    def test_preprocessor_creation(self):
        """Preprocessor should be created without error."""
        preprocessor = create_preprocessor()
        assert preprocessor is not None
    
    def test_preprocessor_fit_transform(self):
        """Preprocessor should fit and transform data without error."""
        df = load_student_data()
        X, y = prepare_features_and_target(df)
        preprocessor = create_preprocessor()
        
        X_transformed = preprocessor.fit_transform(X)
        
        # Should produce a 2D array
        assert X_transformed.ndim == 2
        # Should have same number of rows
        assert X_transformed.shape[0] == X.shape[0]
        # Should have more columns (due to one-hot encoding)
        assert X_transformed.shape[1] > X.shape[1]
    
    def test_no_nan_after_transform(self):
        """Transformed data should have no NaN values."""
        df = load_student_data()
        X, y = prepare_features_and_target(df)
        preprocessor = create_preprocessor()
        
        X_transformed = preprocessor.fit_transform(X)
        assert not np.isnan(X_transformed).any()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
