from sklearn.ensemble import RandomForestClassifier

# FIRST RANDOM FOREST TRAINING RUN, BASELINE WITH UNLIMITED 
def train_baseline_rf(X_train, y_train):
    rf1 = RandomForestClassifier(random_state=42)
    rf1.fit(X_train, y_train)
    print("RF Baseline trained:", rf1.n_estimators, "trees, max_depth =", rf1.max_depth)
    return rf1

# SECOND RANDOM FOREST TRAINING RUN
# 'targets the class-imbalance problem via class_weight="balanced", which reweights the loss so misclassifying the minority class ("Response=1") costs more during training, pushing the model to actually try to catch positives'
def train_balanced_rf(X_train, y_train):
    # n_estimators=200, max_depth=10, class_weight="balanced" define the balnced training run
    rf2 = RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        class_weight="balanced",
        random_state=42
    )
    rf2.fit(X_train, y_train)
    print("RF Tuned/Balanced trained:", rf2.n_estimators, "trees, max_depth =", rf2.max_depth)
    return rf2