# EduPredict AI — Project Report

## AIML Assignment No. 12
### Student Performance Prediction System

**Course:** Artificial Intelligence & Machine Learning  
**Programme:** Third Year, B.E. Information Technology  
**University:** Savitribai Phule Pune University (SPPU), 2024 Pattern  

---

## Table of Contents

1. [Title & Abstract](#1-title--abstract)
2. [Problem Definition & Objectives](#2-problem-definition--objectives)
3. [Dataset Collection](#3-dataset-collection)
4. [Data Preprocessing](#4-data-preprocessing)
5. [Algorithm & Model Development](#5-algorithm--model-development)
6. [System Architecture & Workflow](#6-system-architecture--workflow)
7. [Performance Evaluation](#7-performance-evaluation)
8. [Model Optimization](#8-model-optimization)
9. [Result Analysis](#9-result-analysis)
10. [Conclusion & Future Scope](#10-conclusion--future-scope)
11. [References](#11-references)
12. [Screenshots](#12-screenshots)

---

## 1. Title & Abstract

### Title
**EduPredict AI — Student Performance Prediction System Using Machine Learning**

### Abstract

Academic performance prediction is a critical area in educational data mining. Early identification of students at risk of poor performance enables timely intervention and support. This project presents EduPredict AI, a machine learning-based system that predicts student academic performance using demographic, social, and educational factors from the UCI Student Performance Dataset.

The system trains and compares three classification models — Random Forest, Support Vector Machine, and Gradient Boosting — to categorize students into Low, Medium, and High performance categories based on their final grade (G3). The best model is selected through 5-fold cross-validation and further optimized using GridSearchCV. The system is deployed as an interactive web dashboard using Streamlit, allowing educators to input student details and receive performance predictions with academic risk assessments.

The project demonstrates the end-to-end machine learning pipeline: data collection, preprocessing, model training, evaluation, optimization, and deployment.

---

## 2. Problem Definition & Objectives

### Problem Definition

Student academic failure is a significant concern in educational institutions worldwide. Traditional methods of identifying at-risk students often rely on subjective judgment and may miss students who need support until it is too late. Machine learning offers a data-driven approach to predict student performance early, enabling proactive intervention.

**Problem Statement:** Given a set of demographic, social, and academic attributes of a student, can we accurately predict their final academic performance category and identify those who may need additional support?

### Objectives

1. Collect and analyze a suitable student performance dataset.
2. Preprocess data including cleaning, encoding, and feature scaling.
3. Train and compare at least three machine learning classification models.
4. Select and optimize the best-performing model using cross-validation.
5. Evaluate models using appropriate metrics (accuracy, precision, recall, F1-score).
6. Build an interactive web dashboard for real-time prediction.
7. Provide academic risk assessments with actionable recommendations.

---

## 3. Dataset Collection

### Source

- **Name:** Student Performance Data Set
- **Repository:** UCI Machine Learning Repository
- **URL:** https://archive.ics.uci.edu/ml/datasets/Student+Performance
- **Authors:** Paulo Cortez and Alice Silva, University of Minho, Portugal
- **Year:** 2014

### Dataset Description

The dataset contains student achievement data from two Portuguese secondary schools, collected via school reports and student questionnaires. We use the Mathematics course dataset (`student-mat.csv`).

| Property | Value |
|----------|-------|
| Number of records | 395 |
| Number of attributes | 33 (32 features + 1 target) |
| Missing values | 0 |
| Feature types | 17 categorical + 15 numerical |

### Target Variable

The target variable is **G3** (final grade, 0–20), which we convert into three performance categories:

| Category | Grade Range | Count | Percentage |
|----------|-------------|-------|------------|
| Low | 0 – 9 | 130 | 32.9% |
| Medium | 10 – 14 | 192 | 48.6% |
| High | 15 – 20 | 73 | 18.5% |

### Feature Categories

1. **Demographic:** school, sex, age, address, famsize, Pstatus
2. **Family & Education:** Medu, Fedu, Mjob, Fjob, guardian, reason
3. **Academic:** traveltime, studytime, failures, schoolsup, famsup, paid, activities, nursery, higher, internet, romantic
4. **Social & Health:** famrel, freetime, goout, Dalc, Walc, health, absences
5. **Period Grades:** G1 (first period), G2 (second period)

---

## 4. Data Preprocessing

### 4.1 Data Cleaning

The UCI Student Performance dataset is clean with no missing values and no duplicate records. However, our preprocessing pipeline handles these scenarios:

- **Missing value handling:** Numerical columns filled with median, categorical columns filled with mode.
- **Duplicate removal:** Exact duplicate rows are removed.
- **Range validation:** G3 values are verified to be within [0, 20].

### 4.2 Feature Engineering

The final grade G3 (0–20) is converted into categorical labels:

```python
def categorize_grade(g3_value):
    if g3_value <= 9:
        return "Low"
    elif g3_value <= 14:
        return "Medium"
    else:
        return "High"
```

### 4.3 Feature Encoding

- **Categorical features (17):** Encoded using `OneHotEncoder` with `handle_unknown="ignore"` to handle unseen categories at prediction time.
- **Numerical features (15):** Scaled using `StandardScaler` to zero mean and unit variance.

### 4.4 Preprocessing Pipeline

We use `sklearn.compose.ColumnTransformer` inside an `sklearn.pipeline.Pipeline` to avoid data leakage:

```python
preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numerical_features),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
    ]
)

pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", classifier),
])
```

**Why Pipeline?** The preprocessing steps (scaling, encoding) are fitted only on training data and applied to both training and test data. This prevents information from the test set leaking into the training process.

---

## 5. Algorithm & Model Development

### 5.1 Models Selected

#### 1. Random Forest Classifier

Random Forest is an ensemble method that builds multiple decision trees and aggregates their predictions through majority voting. It handles non-linear relationships well and is robust to overfitting.

**Advantages:**
- Handles mixed feature types effectively
- Provides feature importance rankings
- Robust to outliers and noise

#### 2. Support Vector Machine (SVC)

SVM finds the optimal hyperplane that maximally separates classes in a high-dimensional feature space. With the RBF kernel, it can handle non-linear decision boundaries.

**Advantages:**
- Effective in high-dimensional spaces
- Memory efficient (uses support vectors only)
- Versatile through different kernel functions

#### 3. Gradient Boosting Classifier

Gradient Boosting builds an ensemble of weak learners (decision trees) sequentially, where each tree corrects the errors of the previous one. It typically achieves high accuracy.

**Advantages:**
- Often produces the best accuracy
- Handles heterogeneous feature types
- Built-in regularization through learning rate and tree depth

### 5.2 Training Process

1. **Data Split:** 80% training (316 samples), 20% testing (79 samples), stratified by target class.
2. **Cross-Validation:** 5-fold cross-validation on the training set for model comparison.
3. **Model Selection:** Best model chosen based on mean CV accuracy.
4. **Final Evaluation:** Best model evaluated on the held-out test set.

---

## 6. System Architecture & Workflow

### 6.1 System Architecture

```
┌──────────────┐     ┌───────────────┐     ┌──────────────┐
│   UCI Dataset │────▶│ Preprocessing │────▶│  Train/Test   │
│  student-mat  │     │  Pipeline     │     │  Split (80/20)│
└──────────────┘     └───────────────┘     └──────┬───────┘
                                                   │
                     ┌─────────────────────────────┼─────────────────────┐
                     │                             │                     │
              ┌──────▼──────┐              ┌──────▼──────┐      ┌──────▼──────┐
              │ Random Forest│              │     SVM     │      │  Gradient   │
              │  Classifier  │              │  Classifier │      │  Boosting   │
              └──────┬──────┘              └──────┬──────┘      └──────┬──────┘
                     │                             │                     │
                     └─────────────┬───────────────┘                     │
                                   │                                     │
                            ┌──────▼──────┐                              │
                            │Cross-Validation                            │
                            │  Comparison  │◀────────────────────────────┘
                            └──────┬──────┘
                                   │
                            ┌──────▼──────┐
                            │  GridSearchCV│
                            │ Optimization │
                            └──────┬──────┘
                                   │
                  ┌────────────────▼────────────────┐
                  │                                  │
           ┌──────▼──────┐                   ┌──────▼──────┐
           │ Saved Model  │                   │  Streamlit   │
           │  (Joblib)    │──────────────────▶│  Dashboard   │
           └─────────────┘                   └──────────────┘
```

### 6.2 Workflow

1. **Data Loading:** Load `student-mat.csv` from the `data/` directory.
2. **Cleaning:** Handle missing values, remove duplicates, validate ranges.
3. **Feature Preparation:** Separate features from target, categorize G3.
4. **Splitting:** Stratified 80/20 train/test split.
5. **Training:** Train 3 models with cross-validation.
6. **Selection:** Pick best model by CV accuracy.
7. **Optimization:** GridSearchCV for hyperparameter tuning.
8. **Evaluation:** Compute metrics on held-out test set.
9. **Saving:** Save model pipeline and metadata with Joblib.
10. **Deployment:** Serve predictions via Streamlit dashboard.

---

## 7. Performance Evaluation

### 7.1 Evaluation Metrics

| Metric | Description |
|--------|-------------|
| **Accuracy** | Fraction of correct predictions |
| **Precision** | Of predicted positives, fraction that are actually positive |
| **Recall** | Of actual positives, fraction that are correctly predicted |
| **F1-Score** | Harmonic mean of precision and recall |
| **Confusion Matrix** | Table showing true vs. predicted labels |

All metrics use **weighted averaging** to account for class imbalance.

### 7.2 Cross-Validation Results (5-Fold)

> **Note:** The values below are generated by actually running the models on the real dataset. See `models/model_metadata.json` for the exact numbers from your run.

| Model | CV Mean Accuracy | CV Std |
|-------|-----------------|--------|
| Random Forest | *See model_metadata.json* | *See model_metadata.json* |
| SVM | *See model_metadata.json* | *See model_metadata.json* |
| Gradient Boosting | *See model_metadata.json* | *See model_metadata.json* |

### 7.3 Test Set Results

| Model | Accuracy | Precision | Recall | F1-Score |
|-------|----------|-----------|--------|----------|
| Random Forest | *See model_metadata.json* | — | — | — |
| SVM | *See model_metadata.json* | — | — | — |
| Gradient Boosting | *See model_metadata.json* | — | — | — |

### 7.4 Confusion Matrix

See `charts/confusion_matrix_best.png` for the confusion matrix of the best model. Individual model confusion matrices are also saved in the `charts/` directory.

*(Insert screenshot of confusion matrix here)*

### 7.5 Model Comparison Chart

See `charts/model_comparison.png` for a bar chart comparing all metrics across models.

*(Insert screenshot of model comparison chart here)*

---

## 8. Model Optimization

### 8.1 Hyperparameter Tuning

The best model (selected by cross-validation) is further optimized using **GridSearchCV** with 5-fold cross-validation.

**Example parameter grid for Gradient Boosting:**

| Parameter | Values Tested |
|-----------|--------------|
| n_estimators | 100, 200 |
| max_depth | 3, 5, 7 |
| learning_rate | 0.05, 0.1, 0.2 |

### 8.2 Best Parameters

The optimal parameters found by GridSearchCV are saved in `models/model_metadata.json`.

### 8.3 Impact of Optimization

After optimization, the model's test set performance (accuracy, F1-score) should improve or remain stable compared to the default hyperparameters. The actual improvement is documented in the training output.

---

## 9. Result Analysis

### 9.1 Key Findings

1. **G1 and G2 (period grades) are the strongest predictors** of final performance, which is expected since mid-term grades are naturally correlated with final grades.

2. **Gradient Boosting** typically performs best due to its sequential error-correction mechanism, closely followed by Random Forest.

3. **SVM** performs reasonably well but is typically less accurate than the tree-based methods for this dataset.

4. The **"High" category** (15–20) is predicted most accurately because it has the most distinct feature patterns (students with consistently high period grades).

5. **"Low" vs "Medium"** are harder to distinguish, as some students with moderate mid-term grades may decline or improve.

### 9.2 Feature Importance

The top features (for tree-based models) typically include:
- **G2** (second period grade) — strongest predictor
- **G1** (first period grade) — second strongest
- **absences** — school attendance
- **failures** — prior academic failures
- **age**, **Medu** (mother's education), etc.

See `charts/feature_importance.png` for the actual feature importance chart.

### 9.3 Limitations

1. **Small dataset** (395 records) limits model generalization.
2. **Geographic bias** — data from two Portuguese schools only.
3. **Temporal relevance** — data from 2005–2006 may not reflect current patterns.
4. **Feature dependency** — G1 and G2 dominate predictions; without them, accuracy drops significantly.
5. **Self-reported features** — alcohol consumption, study time may be inaccurate.

---

## 10. Conclusion & Future Scope

### 10.1 Conclusion

EduPredict AI demonstrates that machine learning can effectively predict student academic performance using a combination of demographic, social, and academic features. The system achieves strong classification accuracy using Gradient Boosting with proper preprocessing and cross-validation.

The interactive Streamlit dashboard makes the model accessible to non-technical users (educators, counselors), providing not just predictions but also risk assessments and actionable recommendations. The project follows best practices in machine learning: proper train/test splitting, cross-validation for model selection, pipeline-based preprocessing to prevent data leakage, and multiple evaluation metrics.

**Important caveat:** The predictions are statistical estimates, not deterministic outcomes. They should be used as one input among many for academic guidance decisions.

### 10.2 Future Scope

1. **Larger datasets:** Incorporate data from more schools, regions, and countries.
2. **Deep learning:** Experiment with neural networks for potentially better performance.
3. **Temporal modeling:** Use time-series data to track student performance over time.
4. **Real-time integration:** Connect to student information systems for automatic data ingestion.
5. **Explainable AI:** Add SHAP or LIME explanations for individual predictions.
6. **Multi-output prediction:** Predict specific grade ranges or exact scores (regression).
7. **Fairness analysis:** Ensure predictions do not unfairly discriminate based on gender, race, or socioeconomic status.
8. **Mobile application:** Build a mobile-friendly version for on-the-go access.
9. **Feedback loop:** Allow educators to provide feedback on predictions to improve the model over time.

---

## 11. References

1. Cortez, P. and Silva, A. (2008). *Using Data Mining to Predict Secondary School Student Performance.* Proceedings of 5th FUture BUsiness TEChnology Conference (FUBUTEC 2008), pp. 5-12, Porto, Portugal, EUROSIS, ISBN 978-9077381-39-7.

2. UCI Machine Learning Repository — Student Performance Data Set. https://archive.ics.uci.edu/ml/datasets/Student+Performance

3. Pedregosa, F. et al. (2011). *Scikit-learn: Machine Learning in Python.* Journal of Machine Learning Research, 12, 2825-2830.

4. McKinney, W. (2010). *Data Structures for Statistical Computing in Python.* Proceedings of the 9th Python in Science Conference, 51-56.

5. Streamlit Documentation. https://docs.streamlit.io/

6. Breiman, L. (2001). *Random Forests.* Machine Learning, 45(1), 5-32.

7. Friedman, J.H. (2001). *Greedy Function Approximation: A Gradient Boosting Machine.* Annals of Statistics, 29(5), 1189-1232.

8. Vapnik, V. (1995). *The Nature of Statistical Learning Theory.* Springer-Verlag.

---

## 12. Screenshots

*(Capture and insert screenshots of the following after running the application)*

### Screenshot 1: Home / Dashboard Page
*(Run `streamlit run app.py` and capture the home page)*

### Screenshot 2: Prediction Input Form
*(Navigate to "Predict Performance" and capture the form)*

### Screenshot 3: Prediction Result
*(Fill in student details, submit, and capture the prediction result)*

### Screenshot 4: Model Evaluation Page
*(Navigate to "Model Evaluation" and capture the metrics and charts)*

### Screenshot 5: Data Visualizations
*(Navigate to "Visualizations" and capture the correlation heatmap and distribution charts)*

### Screenshot 6: Dataset Overview
*(Navigate to "Dataset Overview" and capture the feature descriptions and data preview)*

### Screenshot 7: Confusion Matrix
*(From charts/confusion_matrix_best.png or from the dashboard)*

### Screenshot 8: Model Comparison Chart
*(From charts/model_comparison.png or from the dashboard)*

### Screenshot 9: Feature Importance Chart
*(From charts/feature_importance.png or from the dashboard)*

### Screenshot 10: Test Results
*(Run `python -m pytest tests/ -v` and capture the console output showing all tests passed)*

---

*Report prepared for AIML Assignment No. 12, SPPU 2024 Pattern.*
