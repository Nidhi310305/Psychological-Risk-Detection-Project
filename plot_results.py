import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score
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

    features = [
        'sentiment_compound', 'sentiment_positive', 'sentiment_negative',
        'liwc_positive_emotion', 'liwc_negative_emotion', 'liwc_anxiety',
        'liwc_hopelessness', 'liwc_death', 'liwc_isolation', 'liwc_social',
        'pronoun_i_percentage', 'pronoun_we_percentage'
    ]
    target = 'risk_level'
    
    # Ensure features exist in dataframe
    features = [f for f in features if f in df.columns]
    X = df[features]
    y = df[target]
    
    models = {
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'Gradient Boosting': GradientBoostingClassifier(random_state=42),
        'Support Vector Machine': make_pipeline(StandardScaler(), SVC(kernel='rbf', probability=True, random_state=42)),
        'Logistic Regression': make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000, random_state=42))
    }
    
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    labels = sorted(df[target].unique())
    
    # Store metrics for graphing
    metrics_data = {
        'Model': [],
        'Accuracy': [],
        'Precision_Macro': [],
        'Recall_Macro': [],
        'Precision_Weighted': [],
        'Recall_Weighted': []
    }
    
    # Create a 2x2 grid for confusion matrices
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    axes = axes.flatten()
    
    # Generate predictions and populate data
    for i, (name, model) in enumerate(models.items()):
        print(f"Generating predictions for {name}...")
        y_pred = cross_val_predict(model, X, y, cv=cv)
        
        acc = accuracy_score(y, y_pred)
        p_macro = precision_score(y, y_pred, average='macro')
        r_macro = recall_score(y, y_pred, average='macro')
        p_weight = precision_score(y, y_pred, average='weighted')
        r_weight = recall_score(y, y_pred, average='weighted')
        
        metrics_data['Model'].append(name)
        metrics_data['Accuracy'].append(acc)
        metrics_data['Precision_Macro'].append(p_macro)
        metrics_data['Recall_Macro'].append(r_macro)
        metrics_data['Precision_Weighted'].append(p_weight)
        metrics_data['Recall_Weighted'].append(r_weight)
        
        # Plot Confusion Matrix
        cm = confusion_matrix(y, y_pred, labels=labels)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[i], 
                    xticklabels=labels, yticklabels=labels)
        axes[i].set_title(f'{name} Confusion Matrix')
        axes[i].set_xlabel('Predicted')
        axes[i].set_ylabel('Actual')
        
    plt.tight_layout()
    plt.savefig('confusion_matrices.png', dpi=300)
    print("Saved confusion_matrices.png")
    
    # Create Comparative Visual for Macro vs Weighted
    df_metrics = pd.DataFrame(metrics_data)
    
    # Create a table for the user
    print("\nBenchmark Summary Table:")
    print(df_metrics[['Model', 'Accuracy', 'Precision_Macro', 'Precision_Weighted']].to_string(index=False))

    # Reshape for easier plotting
    plot_df = df_metrics.melt(id_vars='Model', var_name='Metric', value_name='Score')
    
    plt.figure(figsize=(14, 8))
    sns.barplot(x='Model', y='Score', hue='Metric', data=plot_df, palette='magma')
    plt.title('Comprehensive Metrics: Macro vs Weighted Averaging')
    plt.ylim(0.85, 1.02)
    plt.xticks(rotation=15)
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2)
    plt.tight_layout()
    plt.savefig('averaging_comparison.png', dpi=300)
    print("Saved averaging_comparison.png")

if __name__ == '__main__':
    main()
