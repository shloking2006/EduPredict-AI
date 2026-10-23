"""
EduPredict AI - Model Training Module
Trains, compares, and optimizes ML models for student performance prediction.
"""

import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score, GridSearchCV
from src.preprocessing import create_preprocessor


def get_models():
    """
    Return a dictionary of candidate models to evaluate.
    
    Returns:
        dict: {model_name: sklearn classifier instance}
    """
    return {
        "Random Forest": RandomForestClassifier(
            n_estimators=100, random_state=42, n_jobs=-1
        ),
        "SVM": SVC(
            kernel="rbf", probability=True, random_state=42
        ),
        "Gradient Boosting": GradientBoostingClassifier(
            n_estimators=100, random_state=42
        ),
    }


def create_model_pipeline(classifier):
    """
    Create a complete pipeline: preprocessor → classifier.
    This ensures no data leakage — preprocessing is fit only on training data.
    
    Args:
        classifier: An sklearn classifier instance.
    
    Returns:
        sklearn Pipeline.
    """
    preprocessor = create_preprocessor()
    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", classifier),
    ])
    return pipeline


def train_and_compare(X_train, y_train, cv_folds=5):
    """
    Train all candidate models using cross-validation and compare them.
    
    Args:
        X_train: Training feature DataFrame.
        y_train: Training target Series.
        cv_folds: Number of cross-validation folds.
    
    Returns:
        dict: {model_name: {pipeline, cv_scores, cv_mean, cv_std}}
    """
    models = get_models()
    results = {}
    
    for name, classifier in models.items():
        print(f"\nTraining {name}...")
        
        pipeline = create_model_pipeline(classifier)
        
        # Cross-validation for robust evaluation
        cv_scores = cross_val_score(
            pipeline, X_train, y_train,
            cv=cv_folds, scoring="accuracy", n_jobs=-1
        )
        
        # Fit on full training set for later evaluation on test set
        pipeline.fit(X_train, y_train)
        
        results[name] = {
            "pipeline": pipeline,
            "cv_scores": cv_scores,
            "cv_mean": cv_scores.mean(),
            "cv_std": cv_scores.std(),
        }
        
        print(f"  CV Accuracy: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
        print(f"  Individual folds: {[f'{s:.4f}' for s in cv_scores]}")
    
    return results


def select_best_model(results):
    """
    Select the best model based on cross-validation mean accuracy.
    
    Args:
        results: Output from train_and_compare().
    
    Returns:
        tuple: (best_model_name, best_pipeline)
    """
    best_name = max(results, key=lambda k: results[k]["cv_mean"])
    best_pipeline = results[best_name]["pipeline"]
    
    print(f"\nBest model: {best_name} "
          f"(CV Accuracy: {results[best_name]['cv_mean']:.4f})")
    
    return best_name, best_pipeline


def optimize_model(X_train, y_train, model_name):
    """
    Hyperparameter tuning for the selected best model using GridSearchCV.
    
    Args:
        X_train: Training features.
        y_train: Training target.
        model_name: Name of the model to optimize.
    
    Returns:
        dict: {best_pipeline, best_params, best_score}
    """
    # Define parameter grids for each model
    param_grids = {
        "Random Forest": {
            "classifier__n_estimators": [100, 200],
            "classifier__max_depth": [None, 10, 20],
            "classifier__min_samples_split": [2, 5],
            "classifier__min_samples_leaf": [1, 2],
        },
        "SVM": {
            "classifier__C": [0.1, 1, 10],
            "classifier__kernel": ["rbf", "linear"],
            "classifier__gamma": ["scale", "auto"],
        },
        "Gradient Boosting": {
            "classifier__n_estimators": [100, 200],
            "classifier__max_depth": [3, 5, 7],
            "classifier__learning_rate": [0.05, 0.1, 0.2],
        },
    }
    
    if model_name not in param_grids:
        print(f"No parameter grid defined for {model_name}.")
        return None
    
    print(f"\nOptimizing {model_name} with GridSearchCV...")
    
    # Create a fresh pipeline for grid search
    models = get_models()
    pipeline = create_model_pipeline(models[model_name])
    
    grid_search = GridSearchCV(
        pipeline,
        param_grids[model_name],
        cv=5,
        scoring="accuracy",
        n_jobs=-1,
        verbose=1,
    )
    
    grid_search.fit(X_train, y_train)
    
    print(f"  Best params: {grid_search.best_params_}")
    print(f"  Best CV score: {grid_search.best_score_:.4f}")
    
    return {
        "best_pipeline": grid_search.best_estimator_,
        "best_params": grid_search.best_params_,
        "best_score": grid_search.best_score_,
    }
