import pandas as pd
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
import warnings

warnings.filterwarnings('ignore')

def main():
    dataset_path = 'data/stage2_dataset_synthetic_v2.csv'
    try:
        df = pd.read_csv(dataset_path)
    except FileNotFoundError:
        print(f"Error: Could not find dataset at {dataset_path}")
        return

    # Extracted linguistic and sentiment features mimicking LIWC
    features = [
        'sentiment_compound', 'sentiment_positive', 'sentiment_negative',
        'liwc_positive_emotion', 'liwc_negative_emotion', 'liwc_anxiety',
        'liwc_hopelessness', 'liwc_death', 'liwc_isolation', 'liwc_social',
        'pronoun_i_percentage', 'pronoun_we_percentage'
    ]
    
    # Check if Risk_level is what we are predicting
    target = 'risk_level'
    
    # Ensure features exist in dataframe
    missing_features = [f for f in features if f not in df.columns]
    if missing_features:
        print(f"Warning: Missing features in dataset: {missing_features}")
        features = [f for f in features if f in df.columns]
        
    X = df[features]
    y = df[target]
    
    # 1. Random Forest
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    
    # 2. Gradient Boosting
    gb_model = GradientBoostingClassifier(random_state=42)
    
    # 3. SVM (Requires scaled data)
    svm_model = make_pipeline(StandardScaler(), SVC(kernel='rbf', probability=True, random_state=42))
    
    # 4. Logistic Regression (Requires scaled data for better convergence)
    lr_model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000, random_state=42))
    
    models = {
        'Random Forest': rf_model,
        'Gradient Boosting': gb_model,
        'Support Vector Machine': svm_model,
        'Logistic Regression': lr_model
    }
    
    scoring_metrics = ['accuracy', 'precision_macro', 'recall_macro']
    
    print("=====================================================")
    print("      Research Paper Classification Benchmarks       ")
    print("=====================================================\n")
    print(f"Dataset Rows: {len(df)}")
    print(f"Features: {len(features)} extracted linguistic/sentiment measures")
    print(f"Target: Predicting DASS-21 mapped Risk Levels (LOW, MODERATE, HIGH)\n")
    
    # Evaluate each model using 5-Fold Cross Validation
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    for name, model in models.items():
        print(f"Evaluating {name}...")
        
        # We use cross_validate to get a robust estimate across multiple folds
        scores = cross_validate(model, X, y, cv=cv, scoring=scoring_metrics)
        
        acc = scores['test_accuracy'].mean()
        prec = scores['test_precision_macro'].mean()
        rec = scores['test_recall_macro'].mean()
        
        print(f"  Accuracy:  {acc:.4f} ({acc*100:.1f}%)")
        print(f"  Precision: {prec:.4f} ({prec*100:.1f}%)")
        print(f"  Recall:    {rec:.4f} ({rec*100:.1f}%)\n")

if __name__ == '__main__':
    main()
