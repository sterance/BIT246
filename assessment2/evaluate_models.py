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