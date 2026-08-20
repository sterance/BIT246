from sklearn.preprocessing import StandardScaler, LabelEncoder

def transform_data(df):
    # Encodes the columns "Gender", "Vehicle_Age" and "Vehicle_Damage" using sklearn.preprocessing LabelEncoder
    label_cols = ["Gender", "Vehicle_Age", "Vehicle_Damage"]
    le = LabelEncoder()
    for col in label_cols:
        df[col] = le.fit_transform(df[col])

    # Scales "Age", "Annual_Premium" and "Vintage" using sklearn.preprocessing StandardScaler to normalise data for random forest processing
    scaler = StandardScaler()
    num_cols = ["Age", "Annual_Premium", "Vintage"]
    df[num_cols] = scaler.fit_transform(df[num_cols])

    return df