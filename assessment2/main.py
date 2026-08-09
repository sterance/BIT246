import pandas as pd
import os

from create_charts import generate_exploration_charts
from clean_data import clean_data, demonstrate_imputation
from transform_data import transform_data
from split_data import split_data
from train_models import train_baseline_rf, train_balanced_rf
from evaluate_models import evaluate, plot_roc_comparison
from feature_importance import plot_feature_importance

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(BASE_DIR, "hicsp.csv"))

print("=== Step 1: Load ===")
print("Shape:", df.shape)
print(df.info())
print(df.describe())
print(df.head())

print("\n=== Step 2: Exploration Charts ===")
generate_exploration_charts(df)

print("\n=== Step 3: Data Cleaning ===")
print("\n--- Imputation Strategy Demonstration (simulated, data unchanged) ---")
demonstrate_imputation(df)

df = clean_data(df)
print("Shape after cleaning:", df.shape)

print("\n=== Step 4: Data Transformation ===")
df = transform_data(df)
print(df.head())

print("\n=== Step 5: Train/Test Split ===")
X_train, X_test, y_train, y_test = split_data(df)

print("\n=== Step 6 & 7: Train Models ===")
rf1 = train_baseline_rf(X_train, y_train)
rf2 = train_balanced_rf(X_train, y_train)

y_pred1 = rf1.predict(X_test)
y_proba1 = rf1.predict_proba(X_test)[:, 1]

y_pred2 = rf2.predict(X_test)
y_proba2 = rf2.predict_proba(X_test)[:, 1]

print("\n=== Step 8: Evaluate Models ===")
evaluate("RF Baseline", y_test, y_pred1, y_proba1)
evaluate("RF Tuned/Balanced", y_test, y_pred2, y_proba2)
plot_roc_comparison(y_test, y_proba1, y_proba2)

print("\n=== Step 9: Feature Importance ===")
plot_feature_importance(rf2, X_train.columns)