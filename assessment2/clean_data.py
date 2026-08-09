import numpy as np
import pandas as pd


def demonstrate_imputation(df, numeric_col="Vintage", categorical_col="Gender", missing_frac=0.05, random_state=42):
    rng = np.random.default_rng(random_state)
    sim_df = df.copy()

    # --- Simulate missingness (MCAR) on a numeric and a categorical column ---
    n_missing = int(len(sim_df) * missing_frac)
    numeric_idx = rng.choice(sim_df.index, size=n_missing, replace=False)
    categorical_idx = rng.choice(sim_df.index, size=n_missing, replace=False)

    ground_truth_numeric = sim_df.loc[numeric_idx, numeric_col].copy()
    ground_truth_categorical = sim_df.loc[categorical_idx, categorical_col].copy()

    sim_df.loc[numeric_idx, numeric_col] = np.nan
    sim_df.loc[categorical_idx, categorical_col] = np.nan

    # --- Technique 1: Median imputation (numeric column) ---
    median_value = sim_df[numeric_col].median()
    sim_df.loc[numeric_idx, numeric_col] = median_value

    # --- Technique 2: Mode imputation (categorical column) ---
    mode_value = sim_df[categorical_col].mode()[0]
    sim_df.loc[categorical_idx, categorical_col] = mode_value

    # --- Validate imputation quality against known ground truth ---
    numeric_mae = (ground_truth_numeric - median_value).abs().mean()
    categorical_match_rate = (ground_truth_categorical == mode_value).mean()

    print(f"[Imputation demo] Simulated {n_missing} missing values in "
          f"'{numeric_col}' and '{categorical_col}' ({missing_frac:.0%} each).")
    print(f"[Imputation demo] Median imputation on '{numeric_col}': "
          f"MAE vs. true values = {numeric_mae:.2f}")
    print(f"[Imputation demo] Mode imputation on '{categorical_col}': "
          f"{categorical_match_rate:.1%} of imputed values matched the true value.")

    return {
        "numeric_column": numeric_col,
        "categorical_column": categorical_col,
        "n_missing": n_missing,
        "numeric_mae": numeric_mae,
        "categorical_match_rate": categorical_match_rate,
    }

def clean_data(df):
    # --- Cleaning technique 1: remove exact duplicate records ---
    before = len(df)
    df = df.drop_duplicates(subset=df.columns.difference(["id"]))
    removed_duplicates = before - len(df)
    print(f"[Cleaning] Removed {removed_duplicates} duplicate rows "
          f"({removed_duplicates / before:.2%} of data).")

    # --- Cleaning technique 2: remove outliers/inconsistencies
    Q1 = df["Annual_Premium"].quantile(0.25)
    Q3 = df["Annual_Premium"].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    before = len(df)
    df = df[(df["Annual_Premium"] >= lower) & (df["Annual_Premium"] <= upper)]
    print(f"[Cleaning] Removed {before - len(df)} outlier rows from "
          f"Annual_Premium (IQR bounds: {lower:.2f}-{upper:.2f}).")
    
    return df