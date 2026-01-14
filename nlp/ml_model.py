import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

# ---------------- TRAINING DATA ----------------
# [income, year]
X = np.array([
    [100000, 1],
    [150000, 1],
    [200000, 2],
    [250000, 2],
    [300000, 3],
    [400000, 3],
    [500000, 4],
    [600000, 4]
])

# 1 = Eligible, 0 = Not Eligible
y = np.array([1,1,1,1,1,0,0,0])

# ---------------- FEATURE SCALING ----------------
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ---------------- MODEL TRAIN ----------------
model = LogisticRegression()
model.fit(X_scaled, y)

# ---------------- PREDICTION FUNCTION ----------------
def predict_eligibility(income, year):
    try:
        income = float(income)
        year = int(year)

        if income <= 0 or year <= 0:
            return 0

        features = scaler.transform([[income, year]])
        prob = model.predict_proba(features)[0][1]
        return round(prob * 100, 2)

    except Exception as e:
        print("Prediction Error:", e)
        return 0
