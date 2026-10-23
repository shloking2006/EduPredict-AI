"""
EduPredict AI - Model Training Script
======================================
Run this script to train, evaluate, and save the best model.

Usage:
    python train_model.py

This script:
1. Loads the UCI Student Performance dataset
2. Cleans and preprocesses the data
3. Splits into train/test sets (80/20)
4. Trains and compares 3 ML models using cross-validation
5. Optimizes the best model's hyperparameters
6. Evaluates on the held-out test set
7. Saves the best model, metadata, and charts
"""

import os
import sys
import json
import joblib
import numpy as np
from sklearn.model_selection import train_test_split

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

from src.data_loader import load_student_data, get_dataset_summary
from src.preprocessing import clean_data, prepare_features_and_target, get_feature_names_after_preprocessing
from src.model_training import train_and_compare, select_best_model, optimize_model
from src.evaluation import (
    evaluate_model, plot_confusion_matrix, plot_model_comparison,
    plot_feature_importance, plot_grade_distribution, CHARTS_DIR,
)

MODELS_DIR = os.path.join(PROJECT_ROOT, "models")
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(CHARTS_DIR, exist_ok=True)


def main():
    print("=" * 60)
    print("  EduPredict AI — Student Performance Prediction System")
    print("  Model Training Pipeline")
    print("=" * 60)
    
    # ── Step 1: Load Dataset ─────────────────────────────────────
    print("\n📂 Step 1: Loading dataset...")
    df = load_student_data()
    summary = get_dataset_summary(df)
    print(f"  Dataset shape: {summary['num_rows']} rows × {summary['num_columns']} columns")
    print(f"  Missing values: {summary['missing_values']}")
    
    # ── Step 2: Clean Data ───────────────────────────────────────
    print("\n🧹 Step 2: Cleaning data...")
    df_clean = clean_data(df)
    print(f"  Clean dataset shape: {df_clean.shape}")
    
    # ── Step 3: Prepare Features and Target ──────────────────────
    print("\n🎯 Step 3: Preparing features and target...")
    X, y = prepare_features_and_target(df_clean)
    print(f"  Features shape: {X.shape}")
    print(f"  Target distribution:")
    for label in ["Low", "Medium", "High"]:
        count = (y == label).sum()
        pct = count / len(y) * 100
        print(f"    {label}: {count} ({pct:.1f}%)")
    
    # Plot grade distribution
    plot_grade_distribution(y, save_path=os.path.join(CHARTS_DIR, "grade_distribution.png"))
    
    # ── Step 4: Train/Test Split ─────────────────────────────────
    print("\n✂️  Step 4: Splitting data (80% train, 20% test)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"  Training set: {X_train.shape[0]} samples")
    print(f"  Test set:     {X_test.shape[0]} samples")
    
    # ── Step 5: Train and Compare Models ─────────────────────────
    print("\n🤖 Step 5: Training and comparing models (5-fold CV)...")
    results = train_and_compare(X_train, y_train, cv_folds=5)
    
    # Print comparison summary
    print("\n📊 Cross-Validation Summary:")
    print("-" * 50)
    for name, res in results.items():
        print(f"  {name:20s} | Accuracy: {res['cv_mean']:.4f} ± {res['cv_std']:.4f}")
    
    # ── Step 6: Select Best Model ────────────────────────────────
    print("\n🏆 Step 6: Selecting best model...")
    best_name, best_pipeline = select_best_model(results)
    
    # ── Step 7: Optimize Best Model ──────────────────────────────
    print("\n⚙️  Step 7: Optimizing best model hyperparameters...")
    optimized = optimize_model(X_train, y_train, best_name)
    
    if optimized is not None:
        best_pipeline = optimized["best_pipeline"]
        print(f"  Optimized CV score: {optimized['best_score']:.4f}")
    
    # ── Step 8: Evaluate on Test Set ─────────────────────────────
    print("\n📈 Step 8: Evaluating on test set...")
    
    # Evaluate all models on test set
    all_test_results = {}
    for name, res in results.items():
        metrics = evaluate_model(res["pipeline"], X_test, y_test)
        all_test_results[name] = metrics
        print(f"\n  {name}:")
        print(f"    Accuracy:  {metrics['accuracy']:.4f}")
        print(f"    Precision: {metrics['precision']:.4f}")
        print(f"    Recall:    {metrics['recall']:.4f}")
        print(f"    F1-Score:  {metrics['f1_score']:.4f}")
    
    # Evaluate optimized best model
    best_metrics = evaluate_model(best_pipeline, X_test, y_test)
    print(f"\n  {best_name} (Optimized):")
    print(f"    Accuracy:  {best_metrics['accuracy']:.4f}")
    print(f"    Precision: {best_metrics['precision']:.4f}")
    print(f"    Recall:    {best_metrics['recall']:.4f}")
    print(f"    F1-Score:  {best_metrics['f1_score']:.4f}")
    print(f"\n  Classification Report ({best_name} — Optimized):")
    print(best_metrics["classification_report"])
    
    # ── Step 9: Generate Charts ──────────────────────────────────
    print("\n📊 Step 9: Generating evaluation charts...")
    
    # Confusion matrix for best model
    plot_confusion_matrix(
        y_test, best_metrics["y_pred"],
        title=f"Confusion Matrix — {best_name} (Optimized)",
        save_path=os.path.join(CHARTS_DIR, "confusion_matrix_best.png"),
    )
    
    # Confusion matrix for each model
    for name, metrics in all_test_results.items():
        safe_name = name.lower().replace(" ", "_")
        plot_confusion_matrix(
            y_test, metrics["y_pred"],
            title=f"Confusion Matrix — {name}",
            save_path=os.path.join(CHARTS_DIR, f"confusion_matrix_{safe_name}.png"),
        )
    
    # Model comparison chart
    plot_model_comparison(
        all_test_results,
        save_path=os.path.join(CHARTS_DIR, "model_comparison.png"),
    )
    
    # Feature importance (if tree-based)
    try:
        preprocessor = best_pipeline.named_steps["preprocessor"]
        feature_names = get_feature_names_after_preprocessing(preprocessor, X_train)
        plot_feature_importance(
            best_pipeline, feature_names,
            save_path=os.path.join(CHARTS_DIR, "feature_importance.png"),
        )
    except Exception as e:
        print(f"  Could not generate feature importance chart: {e}")
    
    # ── Step 10: Save Model and Metadata ─────────────────────────
    print("\n💾 Step 10: Saving model and metadata...")
    
    # Save the best model pipeline
    model_path = os.path.join(MODELS_DIR, "best_model.joblib")
    joblib.dump(best_pipeline, model_path)
    print(f"  Model saved to: {model_path}")
    
    # Save metadata
    metadata = {
        "best_model_name": best_name,
        "best_params": optimized["best_params"] if optimized else {},
        "cv_results": {
            name: {
                "cv_mean": float(res["cv_mean"]),
                "cv_std": float(res["cv_std"]),
                "cv_scores": [float(s) for s in res["cv_scores"]],
            }
            for name, res in results.items()
        },
        "test_results": {
            name: {
                "accuracy": float(m["accuracy"]),
                "precision": float(m["precision"]),
                "recall": float(m["recall"]),
                "f1_score": float(m["f1_score"]),
            }
            for name, m in all_test_results.items()
        },
        "optimized_test_results": {
            "accuracy": float(best_metrics["accuracy"]),
            "precision": float(best_metrics["precision"]),
            "recall": float(best_metrics["recall"]),
            "f1_score": float(best_metrics["f1_score"]),
        },
        "feature_names": list(X.columns),
        "class_labels": ["Low", "Medium", "High"],
        "train_size": int(X_train.shape[0]),
        "test_size": int(X_test.shape[0]),
    }
    
    metadata_path = os.path.join(MODELS_DIR, "model_metadata.joblib")
    joblib.dump(metadata, metadata_path)
    print(f"  Metadata saved to: {metadata_path}")
    
    # Also save as JSON for easy inspection
    json_path = os.path.join(MODELS_DIR, "model_metadata.json")
    with open(json_path, "w") as f:
        json.dump(metadata, f, indent=2)
    print(f"  Metadata JSON saved to: {json_path}")
    
    # ── Done ─────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("  ✅ Training complete!")
    print(f"  Best model: {best_name}")
    print(f"  Test accuracy: {best_metrics['accuracy']:.4f}")
    print(f"  Charts saved to: {CHARTS_DIR}")
    print(f"  Model saved to: {MODELS_DIR}")
    print("=" * 60)
    print("\n  To launch the dashboard, run:")
    print("    streamlit run app.py")


if __name__ == "__main__":
    main()
