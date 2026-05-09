import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score
import warnings

warnings.filterwarnings('ignore')

def main():
    # Load dataset
    df = pd.read_csv('data/stage2_dataset_synthetic_v2.csv')
    
    # Feature selection: Use LIWC and Sentiment features
    features = [
        'sentiment_compound', 'sentiment_positive', 'sentiment_negative',
        'liwc_positive_emotion', 'liwc_negative_emotion', 'liwc_anxiety',
        'liwc_hopelessness', 'liwc_death', 'liwc_isolation', 'liwc_social',
        'pronoun_i_percentage', 'pronoun_we_percentage'
    ]
    
    # Check if Risk_level is what we are predicting
    target = 'risk_level'
    
    X = df[features]
    y = df[target]
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Define models
    models = {
        'Random Forest (Best Accuracy expected)': RandomForestClassifier(n_estimators=100, random_state=42),
        'Gradient Boosting': GradientBoostingClassifier(random_state=42),
        'Support Vector Machine (SVM)': SVC(kernel='rbf', probability=True, random_state=42),
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42)
    }
    
    print("Evaluating Models...\n")
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        acc = accuracy_score(y_test, y_pred)
        # Using macro average since it's a multi-class classification (LOW, MODERATE, HIGH)
        prec = precision_score(y_test, y_pred, average='macro')
        rec = recall_score(y_test, y_pred, average='macro')
        
        print(f"Model: {name}")
        print(f"  Accuracy:  {acc:.4f}")
        print(f"  Precision: {prec:.4f}")
        print(f"  Recall:    {rec:.4f}\n")

if __name__ == '__main__':
    main()
