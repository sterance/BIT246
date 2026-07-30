# BIT246 A2 — Programming Step-by-Step Guide
Dataset: `hicsp.csv` | Target: `Response` (0/1)

This covers only the code you need to write. Documentation/report writing is tracked separately.

---

## Step 1 — Setup & Load
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split

df = pd.read_csv("hicsp.csv")
df.shape
df.info()
df.describe()
df.head()
```
- [ ] Confirm 381,109 rows, 12 columns load correctly
- [ ] Check dtypes match expectations (Region_Code and Policy_Sales_Channel are floats but are really categorical codes — note this for later)

---

## Step 2 — Data Exploration Charts
```python
# Missing values
df.isnull().sum()
sns.heatmap(df.isnull(), cbar=False)
plt.show()

# Class balance of target
sns.countplot(x="Response", data=df)
plt.title("Class Balance: Response")
plt.show()
df["Response"].value_counts(normalize=True)

# Numeric distributions
for col in ["Age", "Annual_Premium", "Vintage"]:
    sns.histplot(df[col], kde=True)
    plt.title(f"Distribution: {col}")
    plt.show()

    sns.boxplot(x=df[col])
    plt.title(f"Boxplot: {col}")
    plt.show()

# Correlation heatmap (numeric columns only)
numeric_df = df.select_dtypes(include=[np.number])
sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm")
plt.show()

# Categorical breakdowns
for col in ["Gender", "Vehicle_Age", "Vehicle_Damage"]:
    sns.countplot(x=col, hue="Response", data=df)
    plt.title(f"{col} vs Response")
    plt.show()
```
- [ ] Run each chart and save/screenshot outputs
- [ ] Note anything unusual (e.g., outliers in Annual_Premium, imbalance in Response)

---

## Step 3 — Data Cleaning (two techniques)
```python
# Technique 1: Handle missing values
# (this dataset typically has no nulls, but confirm and handle defensively)
df = df.dropna(subset=["Age", "Annual_Premium"])          # drop rows missing critical fields
df["Vintage"] = df["Vintage"].fillna(df["Vintage"].median())  # impute if any nulls appear

# Technique 2: Remove outliers/inconsistencies (Annual_Premium has extreme values)
Q1 = df["Annual_Premium"].quantile(0.25)
Q3 = df["Annual_Premium"].quantile(0.75)
IQR = Q3 - Q1
lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR
df = df[(df["Annual_Premium"] >= lower) & (df["Annual_Premium"] <= upper)]

df.shape  # confirm rows dropped
```
- [ ] Confirm row count after cleaning
- [ ] Re-check boxplot of Annual_Premium to confirm outliers reduced

---

## Step 4 — Data Transformation (one technique)
```python
from sklearn.preprocessing import StandardScaler, LabelEncoder

# Encode categorical variables
label_cols = ["Gender", "Vehicle_Age", "Vehicle_Damage"]
le = LabelEncoder()
for col in label_cols:
    df[col] = le.fit_transform(df[col])

# Scale numeric features
scaler = StandardScaler()
num_cols = ["Age", "Annual_Premium", "Vintage"]
df[num_cols] = scaler.fit_transform(df[num_cols])

df.head()
```
- [ ] Confirm categorical columns are now numeric
- [ ] Confirm scaled columns have mean ~0, std ~1

---

## Step 5 — Train/Test Split
```python
X = df.drop(columns=["id", "Response"])
y = df["Response"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
```
- [ ] Confirm split sizes with `X_train.shape`, `X_test.shape`

---

## Step 6 — Model Variation 1: Baseline Random Forest
```python
from sklearn.ensemble import RandomForestClassifier

rf1 = RandomForestClassifier(random_state=42)
rf1.fit(X_train, y_train)
y_pred1 = rf1.predict(X_test)
y_proba1 = rf1.predict_proba(X_test)[:, 1]
```

---

## Step 7 — Model Variation 2: Tuned / Class-Balanced Random Forest
```python
rf2 = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    class_weight="balanced",   # addresses class imbalance seen in Step 2
    random_state=42
)
rf2.fit(X_train, y_train)
y_pred2 = rf2.predict(X_test)
y_proba2 = rf2.predict_proba(X_test)[:, 1]
```

---

## Step 8 — Evaluate Both Models
```python
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

evaluate("RF Baseline", y_test, y_pred1, y_proba1)
evaluate("RF Tuned/Balanced", y_test, y_pred2, y_proba2)

# ROC curve comparison
fpr1, tpr1, _ = roc_curve(y_test, y_proba1)
fpr2, tpr2, _ = roc_curve(y_test, y_proba2)
plt.plot(fpr1, tpr1, label="RF Baseline")
plt.plot(fpr2, tpr2, label="RF Tuned/Balanced")
plt.plot([0, 1], [0, 1], linestyle="--", color="grey")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.legend()
plt.title("ROC Curve Comparison")
plt.show()
```
- [ ] Run and capture all metrics for both models
- [ ] Screenshot the ROC curve comparison

---

## Step 9 — Feature Importance (optional but strengthens results)
```python
importances = pd.Series(rf2.feature_importances_, index=X.columns).sort_values(ascending=False)
sns.barplot(x=importances.values, y=importances.index)
plt.title("Feature Importance (RF Tuned/Balanced)")
plt.show()
```

---

## Step 10 — Sanity Checks Before Moving to Report
- [ ] Full notebook/script runs top to bottom with no errors on a fresh restart
- [ ] All charts render and are saved as images for the appendix
- [ ] Both model metrics are printed and captured
- [ ] Confirm `test.csv` / `sample_submission.csv` were not used anywhere
