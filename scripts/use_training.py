import os
import warnings
import numpy as np
import pandas as pd
import optuna

from sklearn.model_selection import KFold, cross_val_score, cross_val_predict
from sklearn.metrics import accuracy_score, classification_report, recall_score
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier

from joblib import dump
from src.logger import get_logger
from rich.table import Table
from rich.console import Console

# ==============================================
# CONFIG
# ==============================================
warnings.filterwarnings("ignore")
logger = get_logger('use_training', 'training.log')
console = Console()

os.chdir(r'C:\SML_Projects\SML_CVE_type_cwe_predict')

# ==============================================
# LOAD DATA
# ==============================================
X_train = pd.read_csv('data/preprocessed/preprocessed_x_train.csv')
X_test  = pd.read_csv('data/preprocessed/preprocessed_x_test.csv')

y_train = pd.read_csv('data/split/y_train.csv')
y_test  = pd.read_csv('data/split/y_test.csv')

targets = y_train.columns.tolist()

# ==============================================
# CV SETUP
# ==============================================
kf = KFold(n_splits=3, shuffle=True, random_state=42)

# ==============================================
# OPTUNA OBJECTIVE (RECALL MACRO)
# ==============================================
def gb_objective(trial):

    gb = RandomForestClassifier(
        n_estimators=trial.suggest_int('n_estimators', 200, 600),
        max_depth=trial.suggest_int('max_depth', 5, 30),
        min_samples_split=trial.suggest_int('min_samples_split', 2, 20),
        min_samples_leaf=trial.suggest_int('min_samples_leaf', 1, 10),
        max_features=trial.suggest_categorical(
            'max_features', ['sqrt', 'log2', None]
        ),
        n_jobs=-1,
        random_state=42
    )

    model = MultiOutputClassifier(gb, n_jobs=-1)

    y_pred = cross_val_predict(
        model,
        X_train,
        y_train,
        cv=kf,
        n_jobs=-1
    )

    recalls = []
    for i, col in enumerate(targets):
        recalls.append(
            recall_score(
                y_train[col],
                y_pred[:, i],
                average='macro'
            )
        )

    return float(np.mean(recalls))

# ==============================================
# RUN OPTUNA
# ==============================================
logger.info("===== START GRADIENT BOOSTING TUNING (RECALL MACRO) =====")

study = optuna.create_study(direction='maximize')
study.optimize(gb_objective, n_trials=30)

logger.info(f"BEST CV RECALL: {study.best_value:.4f}")
logger.info(f"BEST PARAMS: {study.best_params}")

# ==============================================
# FINAL MODEL
# ==============================================
best_gb = RandomForestClassifier(
    **study.best_params,
    random_state=42
)

model = MultiOutputClassifier(best_gb, n_jobs=-1)
model.fit(X_train, y_train)

# ==============================================
# BASELINE PREDICTIONS (0.5)
# ==============================================
y_pred_train = model.predict(X_train)
y_pred_test  = model.predict(X_test)

# ==============================================
# BASELINE REPORT
# ==============================================
for i, target in enumerate(targets):
    logger.info(f"\n===== {target.upper()} | BASELINE =====")
    logger.info(f"Train accuracy: {accuracy_score(y_train[target], y_pred_train[:, i]):.3f}")
    logger.info(f"Test  accuracy: {accuracy_score(y_test[target], y_pred_test[:, i]):.3f}")
    logger.info("\n" + classification_report(y_test[target], y_pred_test[:, i]))

# ==============================================
# THRESHOLD TUNING (MAX RECALL)
# ==============================================
logger.info("===== THRESHOLD TUNING (RECALL MAX) =====")

probas_train = model.predict_proba(X_train)
best_thresholds = {}

for i, target in enumerate(targets):
    probs = probas_train[i][:, 1]

    best_thr = 0.5
    best_rec = 0.0

    for thr in np.linspace(0.05, 0.95, 19):
        preds = (probs >= thr).astype(int)
        rec = recall_score(y_train[target], preds, average='macro')

        if rec > best_rec:
            best_rec = rec
            best_thr = thr

    best_thresholds[target] = float(best_thr)
    logger.info(f"{target}: threshold={best_thr:.2f} | recall={best_rec:.3f}")

# ==============================================
# PREDICT WITH THRESHOLDS
# ==============================================
def predict_with_threshold(model, X, thresholds):
    probas = model.predict_proba(X)
    preds = []

    for i, thr in enumerate(thresholds):
        preds.append((probas[i][:, 1] >= thr).astype(int))

    return np.column_stack(preds)

threshold_list = [best_thresholds[t] for t in targets]
y_pred_test_thr = predict_with_threshold(model, X_test, threshold_list)

# ==============================================
# FINAL REPORT (THRESHOLD TUNED)
# ==============================================
for i, target in enumerate(targets):
    logger.info(f"\n===== {target.upper()} | THRESHOLD TUNED =====")
    logger.info("\n" + classification_report(
        y_test[target],
        y_pred_test_thr[:, i]
    ))

# ==============================================
# SAVE MODEL
# ==============================================
os.makedirs('pipeline', exist_ok=True)
dump(model, 'pipeline/final_pipeline.joblib', compress=3)
logger.info("Final model pipeline saved.")

# ==============================================
# RESULTS TABLE
# ==============================================
results = []

console = Console()

table = Table(title="Optuna (GradientBoosting Recall Tuned)", show_lines=True)
table.add_column("Algorithm")
table.add_column("Accuracy")
table.add_column("Precision")
table.add_column("Recall")
table.add_column("F1-score")
table.add_column("K-Fold mean")
table.add_column("K-Fold std")

for row in results:
    algo, acc, prec, rec, f1, kmean, kstd = row

    table.add_row(
        algo,
        f"{acc:.2f}",
        prec,
        rec,
        f"{f1:.2f}",
        f"{kmean:.2f}",
        f"{kstd:.2f}"
    )

console.print(table)

# ==============================================
# SAVE RESULTS
# ==============================================
os.makedirs('results', exist_ok=True)
temp_console = Console(record=True)
temp_console.print(table)

with open('results/final_results.txt', 'a', encoding='utf-8') as f:
    f.write(temp_console.export_text())
