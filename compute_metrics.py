import csv

labels = ['LOW', 'MODERATE', 'HIGH']
y_true = []
y_pred = []

with open('data/stage2_dataset_synthetic_v2.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        y_true.append(row['profile_hint'])
        y_pred.append(row['risk_level'])

# Confusion matrix
cm = {l1: {l2: 0 for l2 in labels} for l1 in labels}
for t, p in zip(y_true, y_pred):
    cm[t][p] += 1

# Support (instances per class)
support_counts = {l: sum(cm[l].values()) for l in labels}

# Precision, Recall, F1 per class
precision = {}
recall = {}
f1 = {}
for label in labels:
    tp = cm[label][label]
    fp = sum(cm[other][label] for other in labels if other != label)
    fn = sum(cm[label][other] for other in labels if other != label)
    
    prec = tp / (tp + fp) if (tp + fp) > 0 else 0
    rec = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1_score = 2 * (prec * rec) / (prec + rec) if (prec + rec) > 0 else 0
    
    precision[label] = prec
    recall[label] = rec
    f1[label] = f1_score

# Accuracy
accuracy = sum(cm[l][l] for l in labels) / len(y_true)

# Print results
print('=== CONFUSION MATRIX ===')
print('Predicted →  LOW  MODERATE  HIGH')
for true_label in labels:
    row_str = f'{true_label:8s}    {cm[true_label]["LOW"]:3d}    {cm[true_label]["MODERATE"]:3d}     {cm[true_label]["HIGH"]:3d}'
    print(row_str)

print('\n=== METRICS PER CLASS ===')
print(f'{"Class":<10} {"Precision":>10} {"Recall":>10} {"F1-Score":>10} {"Support":>10}')
print('-' * 50)
for label in labels:
    print(f'{label:<10} {precision[label]:>10.4f} {recall[label]:>10.4f} {f1[label]:>10.4f} {support_counts[label]:>10d}')

# Macro and weighted averages
macro_prec = sum(precision.values()) / len(labels)
macro_recall = sum(recall.values()) / len(labels)
macro_f1 = sum(f1.values()) / len(labels)

weighted_prec = sum(precision[l] * support_counts[l] for l in labels) / len(y_true)
weighted_recall = sum(recall[l] * support_counts[l] for l in labels) / len(y_true)
weighted_f1 = sum(f1[l] * support_counts[l] for l in labels) / len(y_true)

print('-' * 50)
print(f'{"Macro Avg":<10} {macro_prec:>10.4f} {macro_recall:>10.4f} {macro_f1:>10.4f}')
print(f'{"Weighted Avg":<10} {weighted_prec:>10.4f} {weighted_recall:>10.4f} {weighted_f1:>10.4f}')
print(f'\nOverall Accuracy: {accuracy:.4f}')
print(f'Total Samples: {len(y_true)}')
