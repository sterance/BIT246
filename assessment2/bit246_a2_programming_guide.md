# BIT246 A2 — Programming Step-by-Step Guide
Dataset: `hicsp.csv` | Target: `Response` (0/1)

This covers only the code you need to write. Documentation/report writing is tracked separately.

Each step lives in its own file (same pattern as `create_charts.py`), and `main.py` imports and
calls them in order. Keep all files in the same folder as `hicsp.csv` so imports and the CSV path
resolve cleanly. `main.py` prints a short result after each module call so you can see progress in
the console as it runs.

**Project files:**
```
assessment2/
├── hicsp.csv
├── main.py
├── create_charts.py       (Step 2)
├── clean_data.py           (Step 3)
├── transform_data.py       (Step 4)
├── split_data.py           (Step 5)
├── train_models.py         (Steps 6 & 7)
├── evaluate_models.py      (Step 8)
└── feature_importance.py   (Step 9)
```

---

## Step 1 — Setup & Load
This step stays in `main.py` itself since it's the entry point everything else depends on.

**`main.py`** (starting point — will grow as later steps are added):
```python
import pandas as pd

df = pd.read_csv("hicsp.csv")
print("=== Step 1: Load ===")
print("Shape:", df.shape)
print(df.info())
print(df.describe())
print(df.head())
```
- [x] Confirm 381,109 rows, 12 columns load correctly
- [x] Check dtypes match expectations (Region_Code and Policy_Sales_Channel are floats but are really categorical codes — note this for later)

---

## Step 2 — Data Exploration Charts
> Note: on WSL/headless environments matplotlib has no display server, so `plt.show()` does nothing
> (you'll see a `FigureCanvasAgg is non-interactive` warning). Use `plt.savefig(...)` instead — this
> also gives you the image files you need for the report appendix anyway.

First, create a folder to hold the chart images:
```bash
mkdir -p charts
```

**`create_charts.py`**:
```python
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def generate_exploration_charts(df, output_dir="charts"):
    os.makedirs(output_dir, exist_ok=True)

    # Missing values
    df.isnull().sum()
    sns.heatmap(df.isnull(), cbar=False)
    plt.title("Missing Values Heatmap")
    plt.savefig(f"{output_dir}/01_missing_values.png", dpi=150, bbox_inches="tight")
    plt.close()

    # Class balance of target
    sns.countplot(x="Response", data=df)
    plt.title("Class Balance: Response")
    plt.savefig(f"{output_dir}/02_class_balance.png", dpi=150, bbox_inches="tight")
    plt.close()
    print(df["Response"].value_counts(normalize=True))

    # Numeric distributions
    for col in ["Age", "Annual_Premium", "Vintage"]:
        sns.histplot(df[col], kde=True)
        plt.title(f"Distribution: {col}")
        plt.savefig(f"{output_dir}/03_dist_{col}.png", dpi=150, bbox_inches="tight")
        plt.close()

        sns.boxplot(x=df[col])
        plt.title(f"Boxplot: {col}")
        plt.savefig(f"{output_dir}/04_boxplot_{col}.png", dpi=150, bbox_inches="tight")
        plt.close()

    # Correlation heatmap (numeric columns only)
    numeric_df = df.select_dtypes(include=[np.number])
    sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm")
    plt.title("Correlation Heatmap")
    plt.savefig(f"{output_dir}/05_correlation_heatmap.png", dpi=150, bbox_inches="tight")
    plt.close()

    # Categorical breakdowns
    for col in ["Gender", "Vehicle_Age", "Vehicle_Damage"]:
        sns.countplot(x=col, hue="Response", data=df)
        plt.title(f"{col} vs Response")
        plt.savefig(f"{output_dir}/06_{col}_vs_response.png", dpi=150, bbox_inches="tight")
        plt.close()

    print(f"Saved 12 exploration charts to '{output_dir}/'")
```

**`main.py`** update — add the import at the top and the call at the bottom:
```python
import pandas as pd
from create_charts import generate_exploration_charts

df = pd.read_csv("hicsp.csv")
print("=== Step 1: Load ===")
print("Shape:", df.shape)
print(df.info())
print(df.describe())
print(df.head())

print("\n=== Step 2: Exploration Charts ===")
generate_exploration_charts(df)
```
- [x] Confirm `create_charts.py` and `main.py` are in the same folder (so the import resolves)
- [x] Run `python main.py` and confirm each `.png` file appears in `charts/`
- [x] Open the saved images to review them (VS Code's file explorer will preview `.png` files directly)
- [x] Note anything unusual (e.g., outliers in Annual_Premium, imbalance in Response)

---

## Step 3 — Data Cleaning (two techniques)
**`clean_data.py`**:
```python
def clean_data(df):
    rows_before = df.shape[0]

    # Technique 1: Handle missing values
    # (this dataset typically has no nulls, but confirm and handle defensively)
    df = df.dropna(subset=["Age", "Annual_Premium"])              # drop rows missing critical fields
    df["Vintage"] = df["Vintage"].fillna(df["Vintage"].median())  # impute if any nulls appear

    # Technique 2: Remove outliers/inconsistencies (Annual_Premium has extreme values)
    Q1 = df["Annual_Premium"].quantile(0.25)
    Q3 = df["Annual_Premium"].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    df = df[(df["Annual_Premium"] >= lower) & (df["Annual_Premium"] <= upper)]

    rows_after = df.shape[0]
    print(f"Rows before cleaning: {rows_before} | after: {rows_after} | dropped: {rows_before - rows_after}")

    return df
```

**`main.py`** update:
```python
import pandas as pd
from create_charts import generate_exploration_charts
from clean_data import clean_data

df = pd.read_csv("hicsp.csv")
print("=== Step 1: Load ===")
print("Shape:", df.shape)
print(df.info())
print(df.describe())
print(df.head())

print("\n=== Step 2: Exploration Charts ===")
generate_exploration_charts(df)

print("\n=== Step 3: Data Cleaning ===")
df = clean_data(df)
print("Shape after cleaning:", df.shape)
```
- [ ] Confirm row count after cleaning
- [ ] Re-check boxplot of Annual_Premium to confirm outliers reduced (can re-run `generate_exploration_charts(df)` after cleaning to compare)

---

## Step 4 — Data Transformation (one technique)
**`transform_data.py`**:
```python
from sklearn.preprocessing import StandardScaler, LabelEncoder


def transform_data(df):
    # Encode categorical variables
    label_cols = ["Gender", "Vehicle_Age", "Vehicle_Damage"]
    le = LabelEncoder()
    for col in label_cols:
        df[col] = le.fit_transform(df[col])

    # Scale numeric features
    scaler = StandardScaler()
    num_cols = ["Age", "Annual_Premium", "Vintage"]
    df[num_cols] = scaler.fit_transform(df[num_cols])

    print("Encoded columns:", label_cols)
    print("Scaled columns:", num_cols)
    print(df[num_cols].describe().loc[["mean", "std"]])

    return df
```

**`main.py`** update:
```python
import pandas as pd
from create_charts import generate_exploration_charts
from clean_data import clean_data
from transform_data import transform_data

df = pd.read_csv("hicsp.csv")
print("=== Step 1: Load ===")
print("Shape:", df.shape)
print(df.info())
print(df.describe())
print(df.head())

print("\n=== Step 2: Exploration Charts ===")
generate_exploration_charts(df)

print("\n=== Step 3: Data Cleaning ===")
df = clean_data(df)
print("Shape after cleaning:", df.shape)

print("\n=== Step 4: Data Transformation ===")
df = transform_data(df)
print(df.head())
```
- [ ] Confirm categorical columns are now numeric
- [ ] Confirm scaled columns have mean ~0, std ~1

---

## Step 5 — Train/Test Split
**`split_data.py`**:
```python
from sklearn.model_selection import train_test_split


def split_data(df):
    X = df.drop(columns=["id", "Response"])
    y = df["Response"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print("X_train:", X_train.shape, "| X_test:", X_test.shape)
    print("y_train class balance:")
    print(y_train.value_counts(normalize=True))

    return X_train, X_test, y_train, y_test
```

**`main.py`** update:
```python
import pandas as pd
from create_charts import generate_exploration_charts
from clean_data import clean_data
from transform_data import transform_data
from split_data import split_data

df = pd.read_csv("hicsp.csv")
print("=== Step 1: Load ===")
print("Shape:", df.shape)
print(df.info())
print(df.describe())
print(df.head())

print("\n=== Step 2: Exploration Charts ===")
generate_exploration_charts(df)

print("\n=== Step 3: Data Cleaning ===")
df = clean_data(df)
print("Shape after cleaning:", df.shape)

print("\n=== Step 4: Data Transformation ===")
df = transform_data(df)
print(df.head())

print("\n=== Step 5: Train/Test Split ===")
X_train, X_test, y_train, y_test = split_data(df)
```
- [ ] Confirm split sizes with `X_train.shape`, `X_test.shape`

---

## Step 6 & 7 — Random Forest Model Variations
**`train_models.py`**:
```python
from sklearn.ensemble import RandomForestClassifier


def train_baseline_rf(X_train, y_train):
    rf1 = RandomForestClassifier(random_state=42)
    rf1.fit(X_train, y_train)
    print("RF Baseline trained:", rf1.n_estimators, "trees, max_depth =", rf1.max_depth)
    return rf1


def train_balanced_rf(X_train, y_train):
    rf2 = RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        class_weight="balanced",   # addresses class imbalance seen in Step 2
        random_state=42
    )
    rf2.fit(X_train, y_train)
    print("RF Tuned/Balanced trained:", rf2.n_estimators, "trees, max_depth =", rf2.max_depth)
    return rf2
```

**`main.py`** update:
```python
import pandas as pd
from create_charts import generate_exploration_charts
from clean_data import clean_data
from transform_data import transform_data
from split_data import split_data
from train_models import train_baseline_rf, train_balanced_rf

df = pd.read_csv("hicsp.csv")
print("=== Step 1: Load ===")
print("Shape:", df.shape)
print(df.info())
print(df.describe())
print(df.head())

print("\n=== Step 2: Exploration Charts ===")
generate_exploration_charts(df)

print("\n=== Step 3: Data Cleaning ===")
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
```
- [ ] Confirm both models train without errors
- [ ] Note training time difference (rf2 has more trees + depth, will take longer)

---

## Step 8 — Evaluate Both Models
**`evaluate_models.py`**:
```python
import os
import matplotlib.pyplot as plt
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, confusion_matrix, roc_curve
)


def evaluate(name, y_test, y_pred, y_proba):
    print(f"--- {name} ---")
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Precision:", precision_score(y_test, y_pred))
    print("Recall:", recall_score(y_test, y_pred))
    print("F1:", f1_score(y_test, y_pred))
    print("ROC-AUC:", roc_auc_score(y_test, y_proba))
    print(confusion_matrix(y_test, y_pred))


def plot_roc_comparison(y_test, y_proba1, y_proba2, output_dir="charts"):
    os.makedirs(output_dir, exist_ok=True)
    fpr1, tpr1, _ = roc_curve(y_test, y_proba1)
    fpr2, tpr2, _ = roc_curve(y_test, y_proba2)
    plt.plot(fpr1, tpr1, label="RF Baseline")
    plt.plot(fpr2, tpr2, label="RF Tuned/Balanced")
    plt.plot([0, 1], [0, 1], linestyle="--", color="grey")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.legend()
    plt.title("ROC Curve Comparison")
    plt.savefig(f"{output_dir}/07_roc_curve_comparison.png", dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved ROC curve comparison to '{output_dir}/07_roc_curve_comparison.png'")
```

**`main.py`** update:
```python
import pandas as pd
from create_charts import generate_exploration_charts
from clean_data import clean_data
from transform_data import transform_data
from split_data import split_data
from train_models import train_baseline_rf, train_balanced_rf
from evaluate_models import evaluate, plot_roc_comparison

df = pd.read_csv("hicsp.csv")
print("=== Step 1: Load ===")
print("Shape:", df.shape)
print(df.info())
print(df.describe())
print(df.head())

print("\n=== Step 2: Exploration Charts ===")
generate_exploration_charts(df)

print("\n=== Step 3: Data Cleaning ===")
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
```
- [ ] Run and capture all metrics for both models (console output)
- [ ] Confirm `charts/07_roc_curve_comparison.png` was saved

---

## Step 9 — Feature Importance (optional but strengthens results)
**`feature_importance.py`**:
```python
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def plot_feature_importance(model, feature_names, output_dir="charts"):
    os.makedirs(output_dir, exist_ok=True)
    importances = pd.Series(model.feature_importances_, index=feature_names).sort_values(ascending=False)
    sns.barplot(x=importances.values, y=importances.index)
    plt.title("Feature Importance (RF Tuned/Balanced)")
    plt.savefig(f"{output_dir}/08_feature_importance.png", dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved feature importance chart to '{output_dir}/08_feature_importance.png'")
    print(importances)
```

**`main.py`** update — final version:
```python
import pandas as pd
from create_charts import generate_exploration_charts
from clean_data import clean_data
from transform_data import transform_data
from split_data import split_data
from train_models import train_baseline_rf, train_balanced_rf
from evaluate_models import evaluate, plot_roc_comparison
from feature_importance import plot_feature_importance

df = pd.read_csv("hicsp.csv")
print("=== Step 1: Load ===")
print("Shape:", df.shape)
print(df.info())
print(df.describe())
print(df.head())

print("\n=== Step 2: Exploration Charts ===")
generate_exploration_charts(df)

print("\n=== Step 3: Data Cleaning ===")
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
```
- [ ] Confirm `charts/08_feature_importance.png` was saved

---

## Step 10 — Sanity Checks Before Moving to Report
- [ ] Full `main.py` runs top to bottom with no errors on a fresh restart
- [ ] All charts render and are saved as images in `charts/` for the appendix
- [ ] Both model metrics are printed and captured
- [ ] Confirm `test.csv` / `sample_submission.csv` were not used anywhere
