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