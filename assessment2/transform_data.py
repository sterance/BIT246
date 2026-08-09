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

    return df