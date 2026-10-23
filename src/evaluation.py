"""
EduPredict AI - Model Evaluation Module
Generates metrics, confusion matrices, and comparison charts.
"""

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report
)

CHARTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "charts")
os.makedirs(CHARTS_DIR, exist_ok=True)

CLASS_LABELS = ["Low", "Medium", "High"]


def evaluate_model(model, X_test, y_test):
    """
    Evaluate a trained model on test data.
    
    Returns:
        dict with accuracy, precision, recall, f1, predictions, and report.
    """
    y_pred = model.predict(X_test)
    
    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, average="weighted", zero_division=0),
        "recall": recall_score(y_test, y_pred, average="weighted", zero_division=0),
        "f1_score": f1_score(y_test, y_pred, average="weighted", zero_division=0),
        "confusion_matrix": confusion_matrix(y_test, y_pred, labels=CLASS_LABELS),
        "classification_report": classification_report(
            y_test, y_pred, labels=CLASS_LABELS, zero_division=0
        ),
        "y_pred": y_pred,
    }
    return metrics


def plot_confusion_matrix(y_true, y_pred, title="Confusion Matrix", save_path=None):
    """
    Plot and optionally save a confusion matrix heatmap.
    """
    cm = confusion_matrix(y_true, y_pred, labels=CLASS_LABELS)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(
        cm, annot=True, fmt="d", cmap="Blues",
        xticklabels=CLASS_LABELS, yticklabels=CLASS_LABELS, ax=ax
    )
    ax.set_xlabel("Predicted Label", fontsize=12)
    ax.set_ylabel("True Label", fontsize=12)
    ax.set_title(title, fontsize=14, fontweight="bold")
    plt.tight_layout()
    
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
        print(f"Confusion matrix saved to {save_path}")
    
    plt.close(fig)
    return fig


def plot_model_comparison(results_dict, save_path=None):
    """
    Bar chart comparing accuracy, precision, recall, F1 across models.
    
    Args:
        results_dict: {model_name: {accuracy, precision, recall, f1_score}}
    """
    model_names = list(results_dict.keys())
    metrics_names = ["accuracy", "precision", "recall", "f1_score"]
    display_names = ["Accuracy", "Precision", "Recall", "F1-Score"]
    
    x = np.arange(len(model_names))
    width = 0.2
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    for i, (metric, display) in enumerate(zip(metrics_names, display_names)):
        values = [results_dict[m][metric] for m in model_names]
        bars = ax.bar(x + i * width, values, width, label=display)
        # Add value labels on bars
        for bar, val in zip(bars, values):
            ax.text(
                bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.005,
                f"{val:.3f}", ha="center", va="bottom", fontsize=8
            )
    
    ax.set_xlabel("Model", fontsize=12)
    ax.set_ylabel("Score", fontsize=12)
    ax.set_title("Model Comparison — Test Set Metrics", fontsize=14, fontweight="bold")
    ax.set_xticks(x + width * 1.5)
    ax.set_xticklabels(model_names)
    ax.legend(loc="lower right")
    ax.set_ylim(0, 1.15)
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
        print(f"Model comparison chart saved to {save_path}")
    
    plt.close(fig)
    return fig


def plot_feature_importance(model, feature_names, top_n=15, save_path=None):
    """
    Plot feature importance for tree-based models.
    
    Args:
        model: A fitted pipeline whose last step has feature_importances_.
        feature_names: List of feature names after preprocessing.
        top_n: Number of top features to display.
    """
    try:
        # Get the classifier from the pipeline
        if hasattr(model, 'named_steps'):
            classifier = model.named_steps.get('classifier', model)
        else:
            classifier = model
        
        if not hasattr(classifier, 'feature_importances_'):
            print("Model does not have feature_importances_ attribute.")
            return None
        
        importances = classifier.feature_importances_
        
        # Sort by importance
        indices = np.argsort(importances)[::-1][:top_n]
        top_features = [feature_names[i] for i in indices]
        top_importances = importances[indices]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = sns.color_palette("viridis", len(top_features))
        ax.barh(range(len(top_features)), top_importances[::-1], color=colors)
        ax.set_yticks(range(len(top_features)))
        ax.set_yticklabels(top_features[::-1])
        ax.set_xlabel("Feature Importance", fontsize=12)
        ax.set_title(f"Top {top_n} Feature Importances", fontsize=14, fontweight="bold")
        ax.grid(axis="x", alpha=0.3)
        plt.tight_layout()
        
        if save_path:
            fig.savefig(save_path, dpi=150, bbox_inches="tight")
            print(f"Feature importance chart saved to {save_path}")
        
        plt.close(fig)
        return fig
    
    except Exception as e:
        print(f"Could not plot feature importance: {e}")
        return None


def plot_grade_distribution(y, save_path=None):
    """
    Plot the distribution of performance categories in the dataset.
    """
    fig, ax = plt.subplots(figsize=(8, 5))
    
    counts = {}
    for label in CLASS_LABELS:
        counts[label] = sum(1 for val in y if val == label)
    
    colors = ["#e74c3c", "#f39c12", "#27ae60"]
    bars = ax.bar(counts.keys(), counts.values(), color=colors, edgecolor="white", linewidth=1.5)
    
    for bar, count in zip(bars, counts.values()):
        ax.text(
            bar.get_x() + bar.get_width() / 2, bar.get_height() + 2,
            str(count), ha="center", va="bottom", fontweight="bold", fontsize=12
        )
    
    ax.set_xlabel("Performance Category", fontsize=12)
    ax.set_ylabel("Number of Students", fontsize=12)
    ax.set_title("Student Performance Distribution", fontsize=14, fontweight="bold")
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
        print(f"Grade distribution chart saved to {save_path}")
    
    plt.close(fig)
    return fig
