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