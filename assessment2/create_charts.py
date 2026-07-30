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