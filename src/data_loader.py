"""
EduPredict AI - Data Loader Module
Handles loading the UCI Student Performance dataset and provides
dataset information and feature descriptions.
"""

import os
import pandas as pd

# Path to the data directory (relative to project root)
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")


def load_student_data(filepath=None):
    """
    Load the UCI Student Performance dataset (Mathematics course).
    
    Args:
        filepath: Path to student-mat.csv. If None, uses default location.
    
    Returns:
        pd.DataFrame with 395 rows and 33 columns.
    
    Raises:
        FileNotFoundError: If dataset file is not found.
    """
    if filepath is None:
        filepath = os.path.join(DATA_DIR, "student-mat.csv")
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(
            f"Dataset not found at {filepath}.\n"
            f"Please download it from: "
            f"https://archive.ics.uci.edu/ml/datasets/Student+Performance\n"
            f"See DATASET_INFO.md for detailed instructions."
        )
    
    # The UCI dataset uses semicolon as separator
    df = pd.read_csv(filepath, sep=";")
    return df


def get_feature_descriptions():
    """
    Return a dictionary mapping feature names to their descriptions.
    Based on the official UCI dataset documentation.
    """
    return {
        "school": "Student's school (GP: Gabriel Pereira, MS: Mousinho da Silveira)",
        "sex": "Student's sex (F: female, M: male)",
        "age": "Student's age (15 to 22)",
        "address": "Home address type (U: urban, R: rural)",
        "famsize": "Family size (LE3: ≤3, GT3: >3)",
        "Pstatus": "Parent's cohabitation status (T: living together, A: apart)",
        "Medu": "Mother's education (0: none, 1: primary, 2: 5th-9th grade, 3: secondary, 4: higher)",
        "Fedu": "Father's education (0: none, 1: primary, 2: 5th-9th grade, 3: secondary, 4: higher)",
        "Mjob": "Mother's job (teacher, health, services, at_home, other)",
        "Fjob": "Father's job (teacher, health, services, at_home, other)",
        "reason": "Reason to choose this school (home, reputation, course, other)",
        "guardian": "Student's guardian (mother, father, other)",
        "traveltime": "Home to school travel time (1: <15 min, 2: 15-30 min, 3: 30-60 min, 4: >60 min)",
        "studytime": "Weekly study time (1: <2 hrs, 2: 2-5 hrs, 3: 5-10 hrs, 4: >10 hrs)",
        "failures": "Number of past class failures (0 to 4)",
        "schoolsup": "Extra educational support (yes/no)",
        "famsup": "Family educational support (yes/no)",
        "paid": "Extra paid classes (yes/no)",
        "activities": "Extra-curricular activities (yes/no)",
        "nursery": "Attended nursery school (yes/no)",
        "higher": "Wants to take higher education (yes/no)",
        "internet": "Internet access at home (yes/no)",
        "romantic": "In a romantic relationship (yes/no)",
        "famrel": "Quality of family relationships (1: very bad to 5: excellent)",
        "freetime": "Free time after school (1: very low to 5: very high)",
        "goout": "Going out with friends (1: very low to 5: very high)",
        "Dalc": "Workday alcohol consumption (1: very low to 5: very high)",
        "Walc": "Weekend alcohol consumption (1: very low to 5: very high)",
        "health": "Current health status (1: very bad to 5: very good)",
        "absences": "Number of school absences (0 to 93)",
        "G1": "First period grade (0 to 20)",
        "G2": "Second period grade (0 to 20)",
        "G3": "Final grade — TARGET (0 to 20)",
    }


def get_categorical_features():
    """Return list of categorical feature names."""
    return [
        "school", "sex", "address", "famsize", "Pstatus",
        "Mjob", "Fjob", "reason", "guardian",
        "schoolsup", "famsup", "paid", "activities",
        "nursery", "higher", "internet", "romantic",
    ]


def get_numerical_features():
    """Return list of numerical feature names."""
    return [
        "age", "Medu", "Fedu", "traveltime", "studytime", "failures",
        "famrel", "freetime", "goout", "Dalc", "Walc", "health",
        "absences", "G1", "G2",
    ]


def get_dataset_summary(df):
    """
    Return a summary dictionary with dataset statistics.
    
    Args:
        df: The student performance DataFrame.
    
    Returns:
        dict with shape, missing values, dtypes, and basic stats.
    """
    return {
        "num_rows": df.shape[0],
        "num_columns": df.shape[1],
        "missing_values": int(df.isnull().sum().sum()),
        "column_names": list(df.columns),
        "dtypes": df.dtypes.value_counts().to_dict(),
        "numeric_stats": df.describe().to_dict(),
    }
