from sklearn.ensemble import IsolationForest
import pandas as pd

def detect_anomalies(df):
    features = df[['ip_fail_count','user_fail_count']]
    model = IsolationForest(contamination=0.1, random_state=42)
    df['risk_score'] = model.fit_predict(features)
    df['risk_score'] = df['risk_score'].apply(lambda x: 1 if x==-1 else 0)
    return df

def explain_risk(row):
    reasons = []
    if row['ip_fail_count'] > 3:
        reasons.append("IP fails > 3")
    if row['user_fail_count'] > 3:
        reasons.append("User fails > 3")
    return ", ".join(reasons)

def add_explanations(df):
    df['reason'] = df.apply(explain_risk, axis=1)
    return df
