def clean_data(df):
    # Handle missing values (this dataset typically has no nulls, but confirm and handle defensively)
    df = df.dropna(subset=["Age", "Annual_Premium"])
    df["Vintage"] = df["Vintage"].fillna(df["Vintage"].median())

    # Remove outliers/inconsistencies (Annual_Premium has extreme values)
    Q1 = df["Annual_Premium"].quantile(0.25)
    Q3 = df["Annual_Premium"].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    df = df[(df["Annual_Premium"] >= lower) & (df["Annual_Premium"] <= upper)]

    return df