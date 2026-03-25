import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
import os

BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, 'data', 'anomaly_model.joblib')
FEATURES_PATH = os.path.join(BASE_DIR, 'data', 'features.joblib')

def train_model():
    df = pd.read_csv(os.path.join(BASE_DIR, 'data', 'dataset.csv'))
    
    features = ['cpu_percent', 'memory_percent', 'request_latency_ms', 'error_rate']
    X = df[features]
    
    model = IsolationForest(contamination=0.1, random_state=42, n_estimators=100)
    model.fit(X)
    
    joblib.dump(model, MODEL_PATH)
    joblib.dump(features, FEATURES_PATH)
    print(f"Model trained and saved to {MODEL_PATH}")

def load_model():
    return joblib.load(MODEL_PATH)

def predict_anomaly(data_dict):
    model = load_model()
    features = joblib.load(FEATURES_PATH)
    
    df = pd.DataFrame([data_dict])
    df = df[features] # ensure ordering
    
    prediction = model.predict(df)
    score = model.score_samples(df)[0]
    
    # prediction == -1 means anomaly
    return bool(prediction[0] == -1), float(-score) # convert -score to positive value for UI

if __name__ == '__main__':
    train_model()
