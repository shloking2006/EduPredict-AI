"""
EduPredict AI — Student Performance Prediction System
=====================================================
Streamlit Dashboard Application

Run with:  streamlit run app.py
"""

import os
import sys
import json
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

from src.data_loader import (
    load_student_data, get_feature_descriptions,
    get_categorical_features, get_numerical_features, get_dataset_summary,
)
from src.preprocessing import categorize_grade, clean_data, prepare_features_and_target
from src.predictor import load_model, load_model_metadata, predict_performance, RISK_INFO
from src.evaluation import CLASS_LABELS

# ── Page Configuration ───────────────────────────────────────────
st.set_page_config(
    page_title="EduPredict AI — Student Performance Prediction",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ───────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1a5276;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #5d6d7e;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .risk-high { background-color: #ffcccc; padding: 1rem; border-radius: 8px; border-left: 4px solid #e74c3c; }
    .risk-medium { background-color: #fff3cd; padding: 1rem; border-radius: 8px; border-left: 4px solid #f39c12; }
    .risk-low { background-color: #d4edda; padding: 1rem; border-radius: 8px; border-left: 4px solid #27ae60; }
    .disclaimer {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 1rem;
        font-size: 0.85rem;
        color: #6c757d;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)


# ── Helper Functions ─────────────────────────────────────────────
@st.cache_data
def load_data():
    """Load and cache the dataset."""
    return load_student_data()

@st.cache_resource
def load_trained_model():
    """Load and cache the trained model."""
    try:
        return load_model()
    except FileNotFoundError:
        return None

@st.cache_data
def load_metadata():
    """Load and cache model metadata."""
    return load_model_metadata()

def load_chart(filename):
    """Load a chart image if it exists."""
    path = os.path.join(PROJECT_ROOT, "charts", filename)
    if os.path.exists(path):
        return path
    return None


# ── Sidebar Navigation ──────────────────────────────────────────
st.sidebar.image("https://img.icons8.com/color/96/graduation-cap.png", width=80)
st.sidebar.title("🎓 EduPredict AI")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Home",
        "🔮 Predict Performance",
        "📊 Model Evaluation",
        "📈 Visualizations",
        "📋 Dataset Overview",
        "ℹ️ About",
    ],
)

st.sidebar.markdown("---")
st.sidebar.caption(
    "⚠️ **Disclaimer:** Predictions are statistical estimates "
    "based on historical data. They are NOT guarantees of actual "
    "student outcomes."
)

# ═══════════════════════════════════════════════════════════════
# PAGE: HOME
# ═══════════════════════════════════════════════════════════════
if page == "🏠 Home":
    st.markdown('<div class="main-header">🎓 EduPredict AI</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">'
        'Student Performance Prediction System — AIML Assignment No. 12'
        '</div>',
        unsafe_allow_html=True,
    )
    
    # Key Metrics Row
    metadata = load_metadata()
    
    col1, col2, col3, col4 = st.columns(4)
    
    if metadata:
        best_name = metadata.get("best_model_name", "N/A")
        opt_results = metadata.get("optimized_test_results", {})
        
        col1.metric("🏆 Best Model", best_name)
        col2.metric("🎯 Test Accuracy", f"{opt_results.get('accuracy', 0):.1%}")
        col3.metric("📐 F1-Score", f"{opt_results.get('f1_score', 0):.1%}")
        col4.metric("📊 Dataset Size", f"{metadata.get('train_size', 0) + metadata.get('test_size', 0)}")
    else:
        col1.metric("🏆 Best Model", "Not trained")
        col2.metric("🎯 Test Accuracy", "—")
        col3.metric("📐 F1-Score", "—")
        col4.metric("📊 Dataset Size", "—")
        st.warning("⚠️ Model not trained yet. Run `python train_model.py` first.")
    
    st.markdown("---")
    
    # Project Overview
    st.subheader("📖 Project Overview")
    st.markdown("""
    **EduPredict AI** is a machine learning system that predicts student academic performance
    based on demographic, social, and academic factors. It uses the
    [UCI Student Performance Dataset](https://archive.ics.uci.edu/ml/datasets/Student+Performance)
    to train classification models that categorize students into three performance levels:
    
    | Category | Grade Range (G3) | Risk Level | Description |
    |----------|-----------------|------------|-------------|
    | 🔴 **Low** | 0 – 9 | High Risk | May need significant academic support |
    | 🟡 **Medium** | 10 – 14 | Moderate Risk | Average; can improve with effort |
    | 🟢 **High** | 15 – 20 | Low Risk | Performing well |
    """)
    
    st.markdown("---")
    
    # How It Works
    st.subheader("⚙️ How It Works")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown("### 1️⃣ Data Collection")
        st.markdown("UCI Student Performance dataset with 33 attributes covering "
                     "demographics, family, and academic history.")
    with col_b:
        st.markdown("### 2️⃣ ML Training")
        st.markdown("Three models (Random Forest, SVM, Gradient Boosting) are trained "
                     "and compared using cross-validation.")
    with col_c:
        st.markdown("### 3️⃣ Prediction")
        st.markdown("Enter student details to get a performance prediction "
                     "with an academic risk assessment.")


# ═══════════════════════════════════════════════════════════════
# PAGE: PREDICT PERFORMANCE
# ═══════════════════════════════════════════════════════════════
elif page == "🔮 Predict Performance":
    st.header("🔮 Student Performance Prediction")
    st.markdown("Enter student details below to predict academic performance.")
    
    model = load_trained_model()
    if model is None:
        st.error("❌ Model not found. Run `python train_model.py` first.")
        st.stop()
    
    st.markdown("---")
    
    # ── Input Form ───────────────────────────────────────────────
    with st.form("prediction_form"):
        st.subheader("📝 Student Information")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Personal Details**")
            school = st.selectbox("School", ["GP", "MS"],
                                  help="GP: Gabriel Pereira, MS: Mousinho da Silveira")
            sex = st.selectbox("Sex", ["F", "M"])
            age = st.slider("Age", 15, 22, 17)
            address = st.selectbox("Address Type", ["U", "R"],
                                   help="U: Urban, R: Rural")
            famsize = st.selectbox("Family Size", ["LE3", "GT3"],
                                   help="LE3: ≤3, GT3: >3")
            Pstatus = st.selectbox("Parent Status", ["T", "A"],
                                   help="T: Together, A: Apart")
        
        with col2:
            st.markdown("**Family & Education**")
            Medu = st.slider("Mother's Education", 0, 4, 2,
                             help="0: None, 1: Primary, 2: 5th-9th, 3: Secondary, 4: Higher")
            Fedu = st.slider("Father's Education", 0, 4, 2)
            Mjob = st.selectbox("Mother's Job", ["teacher", "health", "services", "at_home", "other"])
            Fjob = st.selectbox("Father's Job", ["teacher", "health", "services", "at_home", "other"])
            guardian = st.selectbox("Guardian", ["mother", "father", "other"])
            reason = st.selectbox("Reason for School Choice",
                                  ["home", "reputation", "course", "other"])
        
        with col3:
            st.markdown("**Academic & Lifestyle**")
            traveltime = st.slider("Travel Time", 1, 4, 1,
                                   help="1: <15min, 2: 15-30min, 3: 30-60min, 4: >60min")
            studytime = st.slider("Weekly Study Time", 1, 4, 2,
                                  help="1: <2hrs, 2: 2-5hrs, 3: 5-10hrs, 4: >10hrs")
            failures = st.slider("Past Failures", 0, 4, 0)
            absences = st.number_input("Absences", 0, 93, 4)
        
        st.markdown("---")
        col4, col5 = st.columns(2)
        
        with col4:
            st.markdown("**Support & Activities**")
            schoolsup = st.selectbox("Extra Educational Support", ["no", "yes"])
            famsup = st.selectbox("Family Educational Support", ["yes", "no"])
            paid = st.selectbox("Extra Paid Classes", ["no", "yes"])
            activities = st.selectbox("Extra-curricular Activities", ["yes", "no"])
            nursery = st.selectbox("Attended Nursery School", ["yes", "no"])
            higher = st.selectbox("Wants Higher Education", ["yes", "no"])
            internet = st.selectbox("Internet Access at Home", ["yes", "no"])
            romantic = st.selectbox("In Romantic Relationship", ["no", "yes"])
        
        with col5:
            st.markdown("**Social & Health**")
            famrel = st.slider("Family Relationship Quality", 1, 5, 4,
                               help="1: Very bad → 5: Excellent")
            freetime = st.slider("Free Time After School", 1, 5, 3)
            goout = st.slider("Going Out with Friends", 1, 5, 3)
            Dalc = st.slider("Workday Alcohol Consumption", 1, 5, 1,
                             help="1: Very low → 5: Very high")
            Walc = st.slider("Weekend Alcohol Consumption", 1, 5, 1)
            health = st.slider("Health Status", 1, 5, 3,
                               help="1: Very bad → 5: Very good")
            st.markdown("---")
            st.markdown("**Prior Grades (0–20)**")
            G1 = st.slider("First Period Grade (G1)", 0, 20, 10)
            G2 = st.slider("Second Period Grade (G2)", 0, 20, 10)
        
        submitted = st.form_submit_button("🔮 Predict Performance", use_container_width=True)
    
    # ── Display Prediction ───────────────────────────────────────
    if submitted:
        student_data = {
            "school": school, "sex": sex, "age": age, "address": address,
            "famsize": famsize, "Pstatus": Pstatus, "Medu": Medu, "Fedu": Fedu,
            "Mjob": Mjob, "Fjob": Fjob, "reason": reason, "guardian": guardian,
            "traveltime": traveltime, "studytime": studytime, "failures": failures,
            "schoolsup": schoolsup, "famsup": famsup, "paid": paid,
            "activities": activities, "nursery": nursery, "higher": higher,
            "internet": internet, "romantic": romantic, "famrel": famrel,
            "freetime": freetime, "goout": goout, "Dalc": Dalc, "Walc": Walc,
            "health": health, "absences": absences, "G1": G1, "G2": G2,
        }
        
        result = predict_performance(model, student_data)
        prediction = result["prediction"]
        risk = result["risk_info"]
        
        st.markdown("---")
        st.subheader("📊 Prediction Result")
        
        # Result card
        col_r1, col_r2 = st.columns([1, 2])
        with col_r1:
            st.markdown(f"### {risk['emoji']} Predicted: **{prediction}** Performance")
            st.markdown(f"**Academic Risk:** {risk['risk_level']}")
            
            if result["probabilities"]:
                st.markdown("**Confidence:**")
                for label, prob in sorted(result["probabilities"].items()):
                    st.progress(float(prob), text=f"{label}: {prob:.1%}")
        
        with col_r2:
            css_class = {
                "Low": "risk-high",
                "Medium": "risk-medium",
                "High": "risk-low",
            }.get(prediction, "risk-medium")
            
            st.markdown(
                f'<div class="{css_class}">'
                f'<strong>{risk["description"]}</strong>'
                f'</div>',
                unsafe_allow_html=True,
            )
            
            st.markdown("**Recommendations:**")
            for rec in risk["recommendations"]:
                st.markdown(f"  - {rec}")
        
        # Disclaimer
        st.markdown(
            '<div class="disclaimer">'
            '⚠️ <strong>Important:</strong> This prediction is a statistical estimate based on '
            'historical data patterns. It is NOT a guarantee of actual student performance. '
            'Many factors beyond this model\'s scope can influence academic outcomes. '
            'Use this tool as one of many inputs for academic guidance decisions.'
            '</div>',
            unsafe_allow_html=True,
        )


# ═══════════════════════════════════════════════════════════════
# PAGE: MODEL EVALUATION
# ═══════════════════════════════════════════════════════════════
elif page == "📊 Model Evaluation":
    st.header("📊 Model Evaluation & Comparison")
    
    metadata = load_metadata()
    if metadata is None:
        st.warning("⚠️ Model metadata not found. Run `python train_model.py` first.")
        st.stop()
    
    # ── Cross-Validation Results ─────────────────────────────────
    st.subheader("🔄 Cross-Validation Results (5-Fold)")
    cv_data = []
    for name, cv in metadata.get("cv_results", {}).items():
        cv_data.append({
            "Model": name,
            "CV Mean Accuracy": f"{cv['cv_mean']:.4f}",
            "CV Std": f"± {cv['cv_std']:.4f}",
            "Fold Scores": ", ".join(f"{s:.4f}" for s in cv["cv_scores"]),
        })
    st.table(pd.DataFrame(cv_data))
    
    # ── Test Set Results ─────────────────────────────────────────
    st.subheader("🧪 Test Set Results")
    test_data = []
    for name, metrics in metadata.get("test_results", {}).items():
        test_data.append({
            "Model": name,
            "Accuracy": f"{metrics['accuracy']:.4f}",
            "Precision": f"{metrics['precision']:.4f}",
            "Recall": f"{metrics['recall']:.4f}",
            "F1-Score": f"{metrics['f1_score']:.4f}",
        })
    st.table(pd.DataFrame(test_data))
    
    # Optimized model
    opt = metadata.get("optimized_test_results", {})
    if opt:
        st.success(
            f"🏆 **Best Model ({metadata.get('best_model_name', 'N/A')} — Optimized):** "
            f"Accuracy = {opt.get('accuracy', 0):.4f}, "
            f"Precision = {opt.get('precision', 0):.4f}, "
            f"Recall = {opt.get('recall', 0):.4f}, "
            f"F1-Score = {opt.get('f1_score', 0):.4f}"
        )
    
    # Best params
    best_params = metadata.get("best_params", {})
    if best_params:
        st.subheader("⚙️ Optimized Hyperparameters")
        params_df = pd.DataFrame(
            [{"Parameter": k, "Value": str(v)} for k, v in best_params.items()]
        )
        st.table(params_df)
    
    # ── Charts ───────────────────────────────────────────────────
    st.subheader("📈 Evaluation Charts")
    
    tab1, tab2, tab3 = st.tabs(["Model Comparison", "Confusion Matrix", "Feature Importance"])
    
    with tab1:
        chart = load_chart("model_comparison.png")
        if chart:
            st.image(chart, caption="Model Comparison — Test Set Metrics", use_container_width=True)
        else:
            st.info("Chart not generated yet.")
    
    with tab2:
        chart = load_chart("confusion_matrix_best.png")
        if chart:
            st.image(chart, caption="Confusion Matrix — Best Model (Optimized)", use_container_width=True)
        else:
            st.info("Chart not generated yet.")
        
        # Show individual model confusion matrices
        for name in metadata.get("test_results", {}):
            safe_name = name.lower().replace(" ", "_")
            chart = load_chart(f"confusion_matrix_{safe_name}.png")
            if chart:
                with st.expander(f"Confusion Matrix — {name}"):
                    st.image(chart, use_container_width=True)
    
    with tab3:
        chart = load_chart("feature_importance.png")
        if chart:
            st.image(chart, caption="Top Feature Importances", use_container_width=True)
        else:
            st.info("Feature importance chart not available (only for tree-based models).")


# ═══════════════════════════════════════════════════════════════
# PAGE: VISUALIZATIONS
# ═══════════════════════════════════════════════════════════════
elif page == "📈 Visualizations":
    st.header("📈 Data Visualizations")
    
    try:
        df = load_data()
    except FileNotFoundError:
        st.error("Dataset not found.")
        st.stop()
    
    # Grade Distribution
    st.subheader("📊 Grade Distribution")
    chart = load_chart("grade_distribution.png")
    if chart:
        st.image(chart, caption="Student Performance Category Distribution", use_container_width=True)
    
    st.markdown("---")
    
    # Interactive plots
    st.subheader("🔍 Explore Relationships")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # G3 distribution histogram
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.hist(df["G3"], bins=21, range=(-0.5, 20.5), color="#3498db",
                edgecolor="white", alpha=0.8)
        ax.axvline(x=9.5, color="#e74c3c", linestyle="--", label="Low/Medium boundary")
        ax.axvline(x=14.5, color="#f39c12", linestyle="--", label="Medium/High boundary")
        ax.set_xlabel("Final Grade (G3)")
        ax.set_ylabel("Number of Students")
        ax.set_title("Distribution of Final Grades")
        ax.legend()
        ax.grid(axis="y", alpha=0.3)
        st.pyplot(fig)
        plt.close(fig)
    
    with col2:
        # G1 vs G2 vs G3
        fig, ax = plt.subplots(figsize=(8, 5))
        scatter = ax.scatter(df["G1"], df["G3"], c=df["G2"], cmap="viridis",
                           alpha=0.6, edgecolors="white", linewidth=0.5)
        ax.set_xlabel("First Period Grade (G1)")
        ax.set_ylabel("Final Grade (G3)")
        ax.set_title("G1 vs G3 (colored by G2)")
        plt.colorbar(scatter, ax=ax, label="G2")
        ax.grid(alpha=0.3)
        st.pyplot(fig)
        plt.close(fig)
    
    st.markdown("---")
    
    # Correlation heatmap (numerical features only)
    st.subheader("🔗 Feature Correlations")
    numeric_cols = get_numerical_features() + ["G3"]
    corr = df[numeric_cols].corr()
    
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdYlBu_r",
                center=0, ax=ax, square=True, linewidths=0.5)
    ax.set_title("Correlation Matrix — Numerical Features", fontsize=14, fontweight="bold")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    
    st.markdown("---")
    
    # Study time vs performance
    st.subheader("📚 Study Time vs Performance")
    df_viz = df.copy()
    df_viz["Performance"] = df_viz["G3"].apply(categorize_grade)
    
    col3, col4 = st.columns(2)
    with col3:
        fig, ax = plt.subplots(figsize=(8, 5))
        study_labels = {1: "<2 hrs", 2: "2-5 hrs", 3: "5-10 hrs", 4: ">10 hrs"}
        df_viz["Study Label"] = df_viz["studytime"].map(study_labels)
        order = ["<2 hrs", "2-5 hrs", "5-10 hrs", ">10 hrs"]
        sns.boxplot(data=df_viz, x="Study Label", y="G3", order=order,
                   palette="viridis", ax=ax)
        ax.set_xlabel("Weekly Study Time")
        ax.set_ylabel("Final Grade (G3)")
        ax.set_title("Study Time vs Final Grade")
        ax.grid(axis="y", alpha=0.3)
        st.pyplot(fig)
        plt.close(fig)
    
    with col4:
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.boxplot(data=df_viz, x="Performance", y="absences",
                   order=["Low", "Medium", "High"], palette=["#e74c3c", "#f39c12", "#27ae60"],
                   ax=ax)
        ax.set_xlabel("Performance Category")
        ax.set_ylabel("Number of Absences")
        ax.set_title("Absences by Performance Category")
        ax.grid(axis="y", alpha=0.3)
        st.pyplot(fig)
        plt.close(fig)


# ═══════════════════════════════════════════════════════════════
# PAGE: DATASET OVERVIEW
# ═══════════════════════════════════════════════════════════════
elif page == "📋 Dataset Overview":
    st.header("📋 Dataset Overview")
    
    try:
        df = load_data()
    except FileNotFoundError:
        st.error("Dataset not found. See DATASET_INFO.md for download instructions.")
        st.stop()
    
    # Summary stats
    st.subheader("📊 Summary Statistics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Missing Values", int(df.isnull().sum().sum()))
    col4.metric("Duplicate Rows", int(df.duplicated().sum()))
    
    st.markdown("---")
    
    # Feature descriptions
    st.subheader("📖 Feature Descriptions")
    descriptions = get_feature_descriptions()
    desc_df = pd.DataFrame([
        {"Feature": k, "Type": str(df[k].dtype), "Description": v}
        for k, v in descriptions.items()
    ])
    st.dataframe(desc_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Data preview
    st.subheader("👀 Data Preview")
    n_rows = st.slider("Number of rows to display", 5, 50, 10)
    st.dataframe(df.head(n_rows), use_container_width=True)
    
    st.markdown("---")
    
    # Descriptive statistics
    st.subheader("📐 Descriptive Statistics")
    st.dataframe(df.describe().round(2), use_container_width=True)
    
    st.markdown("---")
    
    # Data source
    st.subheader("📚 Data Source")
    st.markdown("""
    **Dataset:** UCI Machine Learning Repository — Student Performance Data Set  
    **URL:** [https://archive.ics.uci.edu/ml/datasets/Student+Performance](https://archive.ics.uci.edu/ml/datasets/Student+Performance)  
    **Authors:** Paulo Cortez, University of Minho, Portugal  
    **Year:** 2014  
    **File used:** `student-mat.csv` (Mathematics course, 395 students, 33 attributes)  
    
    **Citation:**  
    P. Cortez and A. Silva. *Using Data Mining to Predict Secondary School Student Performance.*
    In A. Brito and J. Teixeira (Eds.), Proceedings of 5th FUture BUsiness TEChnology Conference
    (FUBUTEC 2008), pp. 5-12, Porto, Portugal, April, 2008, EUROSIS, ISBN 978-9077381-39-7.
    """)


# ═══════════════════════════════════════════════════════════════
# PAGE: ABOUT
# ═══════════════════════════════════════════════════════════════
elif page == "ℹ️ About":
    st.header("ℹ️ About EduPredict AI")
    
    st.markdown("""
    ### 🎓 EduPredict AI — Student Performance Prediction System
    
    **Assignment:** AIML Assignment No. 12  
    **Course:** Third Year Information Technology  
    **University:** Savitribai Phule Pune University (SPPU), 2024 Pattern  
    
    ---
    
    ### 🎯 Objective
    Predict student academic performance using machine learning techniques and
    identify students who may need academic support, enabling early intervention.
    
    ### 🛠️ Technology Stack
    | Component | Technology |
    |-----------|-----------|
    | Language | Python 3.12 |
    | Data Processing | Pandas, NumPy |
    | Machine Learning | Scikit-learn |
    | Visualization | Matplotlib, Seaborn |
    | Dashboard | Streamlit |
    | Model Persistence | Joblib |
    
    ### 📋 Models Compared
    1. **Random Forest Classifier** — Ensemble of decision trees  
    2. **Support Vector Machine (SVC)** — Finds optimal hyperplane  
    3. **Gradient Boosting Classifier** — Sequential ensemble learning  
    
    ### 🔄 Methodology
    1. Load the UCI Student Performance dataset  
    2. Clean data and handle missing values  
    3. Encode categorical features (OneHotEncoder)  
    4. Scale numerical features (StandardScaler)  
    5. Split into 80% training / 20% test sets (stratified)  
    6. Train models using 5-fold cross-validation  
    7. Compare models on accuracy, precision, recall, F1-score  
    8. Optimize best model using GridSearchCV  
    9. Evaluate final model on held-out test set  
    10. Save model pipeline with Joblib  
    
    ### ⚠️ Limitations
    - Dataset contains only 395 records from two Portuguese schools  
    - Predictions are statistical estimates, not deterministic outcomes  
    - Model reflects patterns in historical data and may not generalize  
    - Cultural and regional factors limit transferability  
    - Features like G1 and G2 (mid-term grades) strongly influence the prediction  
    
    ### 📜 License
    This project is for educational purposes as part of the SPPU curriculum.
    The dataset is publicly available from the UCI ML Repository.
    """)
    
    st.markdown("---")
    st.caption("Built with ❤️ using Python, Scikit-learn, and Streamlit")
