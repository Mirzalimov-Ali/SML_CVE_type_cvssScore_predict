import os
import pandas as pd
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.metrics import accuracy_score, classification_report
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from joblib import dump
from src.logger import get_logger
from rich.table import Table
from rich.console import Console

logger = get_logger('use_training', 'training.log')
console = Console()

os.chdir(r'C:\SML_Projects\SML_CVE_type_cwe_predict')

df = pd.read_csv('data/preprocessed/preprocessed_dataset.csv')
df = df.sample(frac=0.1, random_state=42).reset_index(drop=True)

X = df.drop(columns=['type', 'cvss_score'], errors='ignore')
y = df[['type', 'cvss_score']]

model = MultiOutputClassifier(
    RandomForestClassifier(n_estimators=220, max_depth=5, random_state=42)
)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model.fit(X_train, y_train)

y_pred_train = model.predict(X_train)
y_pred_test = model.predict(X_test)

for i, target in enumerate(y.columns):
    logger.info(f"\n===== {target.upper()} =====")
    logger.info(f"Train accuracy: {accuracy_score(y_train[target], y_pred_train[:, i]):.3f}")
    logger.info(f"Test  accuracy: {accuracy_score(y_test[target], y_pred_test[:, i]):.3f}")
    logger.info("\n" + classification_report(y_test[target], y_pred_test[:, i]))

kf = KFold(n_splits=3, shuffle=True, random_state=42)
cv_results = {}

for target in y.columns:
    gb = GradientBoostingClassifier(n_estimators=220, max_depth=5, random_state=42)
    scores = cross_val_score(gb, X, y[target], cv=kf, scoring='f1_macro')
    cv_results[target] = scores
    logger.info(f"{target} 3-Fold CV F1 macro: {scores.mean():.3f} ± {scores.std():.3f}")

os.makedirs('pipeline', exist_ok=True)
dump(model, 'pipeline/final_pipeline.joblib', compress=3)
logger.info("Final model pipeline saved.")

# ==============================================
results = []

for target in y.columns:
    test_acc = accuracy_score(y_test[target], y_pred_test[:, y.columns.get_loc(target)])
    scores = cv_results[target]
    kf_mean = scores.mean()
    kf_std = scores.std()
    
    results.append([
        "GradientBoosting",
        test_acc,
        kf_mean,
        kf_std,
        target
    ])

for row in results:
    combined = (row[1] + row[2]) / 2
    row.append(combined)

results_sorted = sorted(results, key=lambda x: x[-1], reverse=True)
best_model = max(results_sorted, key=lambda x: x[-1])
worst_model = min(results_sorted, key=lambda x: x[-1])

table = Table(title="GradientBoosting MultiOutput Results", show_lines=True)
table.add_column("Algorithm")
table.add_column("Target")
table.add_column("Test Acc")
table.add_column("K-Fold Mean")
table.add_column("K-Fold Std")
table.add_column("Combined", justify="right")

for row in results_sorted:
    algo, test_acc, kf_mean, kf_std, target, combined = row

    if row == best_model:
        table.add_row(f"[bold green]{algo}[/bold green]",
                      f"[bold green]{target}[/bold green]",
                      f"[bold green]{test_acc:.2f}[/bold green]",
                      f"[bold green]{kf_mean:.2f}[/bold green]",
                      f"[bold green]{kf_std:.2f}[/bold green]",
                      f"[bold green]{combined:.2f}[/bold green]")
    elif row == worst_model:
        table.add_row(f"[bold red]{algo}[/bold red]",
                      f"[bold red]{target}[/bold red]",
                      f"[bold red]{test_acc:.2f}[/bold red]",
                      f"[bold red]{kf_mean:.2f}[/bold red]",
                      f"[bold red]{kf_std:.2f}[/bold red]",
                      f"[bold red]{combined:.2f}[/bold red]")
    else:
        table.add_row(algo, target, f"{test_acc:.2f}", f"{kf_mean:.2f}", f"{kf_std:.2f}", f"{combined:.2f}")

console.print(table)

os.makedirs('results', exist_ok=True)
df_results = pd.DataFrame(results_sorted, columns=["Algorithm", "Test Acc", "K-Fold Mean", "K-Fold Std", "Target", "Combined"])
df_results.to_csv('results/final_results.csv', index=False)

print("Results saved to results/final_results.csv")
