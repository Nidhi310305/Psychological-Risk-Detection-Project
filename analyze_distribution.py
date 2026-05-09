import csv
import numpy as np

# Load scores and true labels
scores = {'LOW': [], 'MODERATE': [], 'HIGH': []}

with open('data/stage2_dataset_synthetic_v2.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        true_label = row['profile_hint']
        score = float(row['risk_score'])
        scores[true_label].append(score)

# Analyze distribution
print("=== CURRENT SCORE DISTRIBUTION ===")
for label in ['LOW', 'MODERATE', 'HIGH']:
    scores_list = scores[label]
    print(f"\n{label}:")
    print(f"  Count: {len(scores_list)}")
    print(f"  Mean: {np.mean(scores_list):.2f}")
    print(f"  Std: {np.std(scores_list):.2f}")
    print(f"  Min: {np.min(scores_list):.2f}")
    print(f"  Max: {np.max(scores_list):.2f}")
    print(f"  Median: {np.median(scores_list):.2f}")
    print(f"  Q1-Q3: {np.percentile(scores_list, 25):.2f} - {np.percentile(scores_list, 75):.2f}")

# Find optimal thresholds for 3-class classification
print("\n=== FINDING OPTIMAL THRESHOLDS ===")
print("Testing threshold combinations...")

all_scores = []
all_labels = []
for label in ['LOW', 'MODERATE', 'HIGH']:
    all_scores.extend(scores[label])
    all_labels.extend([label] * len(scores[label]))

all_scores = np.array(all_scores)
all_labels = np.array(all_labels)

best_acc = 0
best_t1, best_t2 = 33, 67

# Test different threshold combinations
for t1 in np.arange(20, 45, 1):
    for t2 in np.arange(50, 75, 1):
        if t2 <= t1:
            continue
        
        predictions = []
        for score in all_scores:
            if score < t1:
                predictions.append('LOW')
            elif score < t2:
                predictions.append('MODERATE')
            else:
                predictions.append('HIGH')
        
        acc = np.mean(np.array(predictions) == all_labels)
        if acc > best_acc:
            best_acc = acc
            best_t1, best_t2 = t1, t2

print(f"\nBest thresholds: LOW < {best_t1}, MODERATE < {best_t2}, HIGH >= {best_t2}")
print(f"Accuracy with optimized thresholds: {best_acc:.4f}")

# Also test if we need to boost HIGH detection with red-flag weights
print("\n=== TESTING RED-FLAG BOOST STRATEGY ===")
print("What if we give red-flag detected rows +20 bonus points?")

# This would be implemented in the model code
print("(This requires modifying my_model.py to apply red-flag boost)")
