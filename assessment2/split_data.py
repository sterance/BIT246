from sklearn.model_selection import train_test_split

# CALCULATES THE SPLIT BETWEEN THE RESPONSES
def split_data(df):
    X = df.drop(columns=["id", "Response"]) # removes id because it has no statistical meaning, and Response as it is the target that is being predicted, not input
    y = df["Response"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # prints the results of sklearn.model_selection applied to the dataset
    print("X_train:", X_train.shape, "| X_test:", X_test.shape)
    print("y_train class balance:")
    print(y_train.value_counts(normalize=True))

    return X_train, X_test, y_train, y_test