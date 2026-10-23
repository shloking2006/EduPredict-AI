"""
EduPredict AI - Data Preprocessing Module
Handles data cleaning, encoding, feature engineering, and
building the scikit-learn preprocessing pipeline.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from src.data_loader import get_categorical_features, get_numerical_features


# Performance categories for classification
GRADE_BINS = {
    "Low": (0, 9),       # Grade 0–9: needs academic support
    "Medium": (10, 14),  # Grade 10–14: average performance
    "High": (15, 20),    # Grade 15–20: good performance
}


def categorize_grade(g3_value):
    """
    Convert a numeric G3 grade (0–20) into a performance category.
    
    Args:
        g3_value: Integer grade from 0 to 20.
    
    Returns:
        str: 'Low', 'Medium', or 'High'.
    """
    if g3_value <= 9:
        return "Low"
    elif g3_value <= 14:
        return "Medium"
    else:
        return "High"


def clean_data(df):
    """
    Clean the raw dataset:
    - Handle missing values (if any)
    - Remove duplicates
    - Validate value ranges
    
    Args:
        df: Raw DataFrame from data_loader.
    
    Returns:
        Cleaned DataFrame.
    """
    df_clean = df.copy()
    
    # Report missing values
    missing = df_clean.isnull().sum()
    if missing.sum() > 0:
        print(f"Found {missing.sum()} missing values:")
        print(missing[missing > 0])
        # Fill numerical missing with median, categorical with mode
        for col in df_clean.columns:
            if df_clean[col].isnull().any():
                if df_clean[col].dtype in ['int64', 'float64']:
                    df_clean[col] = df_clean[col].fillna(df_clean[col].median())
                else:
                    df_clean[col] = df_clean[col].fillna(df_clean[col].mode()[0])
    else:
        print("No missing values found in the dataset.")
    
    # Remove exact duplicates (keep first)
    n_before = len(df_clean)
    df_clean.drop_duplicates(inplace=True)
    n_removed = n_before - len(df_clean)
    if n_removed > 0:
        print(f"Removed {n_removed} duplicate rows.")
    else:
        print("No duplicate rows found.")
    
    # Validate G3 range
    if "G3" in df_clean.columns:
        df_clean = df_clean[(df_clean["G3"] >= 0) & (df_clean["G3"] <= 20)]
    
    return df_clean


def prepare_features_and_target(df):
    """
    Separate features and target. Create performance category from G3.
    
    Args:
        df: Cleaned DataFrame with G3 column.
    
    Returns:
        X (pd.DataFrame): Feature matrix (G3 removed).
        y (pd.Series): Target variable (performance category).
    """
    # Create target variable by categorizing G3
    y = df["G3"].apply(categorize_grade)
    
    # Features = all columns except G3 (target)
    feature_cols = get_categorical_features() + get_numerical_features()
    X = df[feature_cols].copy()
    
    return X, y


def create_preprocessor():
    """
    Create a scikit-learn ColumnTransformer for preprocessing.
    
    - StandardScaler for numerical features
    - OneHotEncoder for categorical features
    
    Returns:
        ColumnTransformer ready to be used in a Pipeline.
    """
    categorical_features = get_categorical_features()
    numerical_features = get_numerical_features()
    
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numerical_features),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical_features),
        ],
        remainder="drop",  # Drop any columns not listed
    )
    
    return preprocessor


def get_feature_names_after_preprocessing(preprocessor, X):
    """
    Get feature names after ColumnTransformer preprocessing.
    
    Args:
        preprocessor: Fitted ColumnTransformer.
        X: Original feature DataFrame.
    
    Returns:
        List of feature names after transformation.
    """
    try:
        return list(preprocessor.get_feature_names_out())
    except AttributeError:
        # Fallback for older sklearn versions
        num_features = get_numerical_features()
        cat_features = get_categorical_features()
        
        ohe = preprocessor.named_transformers_["cat"]
        cat_encoded = list(ohe.get_feature_names_out(cat_features))
        
        return num_features + cat_encoded
