import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import os

BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, 'data', 'anomaly_model.joblib')
FEATURES_PATH = os.path.join(BASE_DIR, 'data', 'features.joblib')

def train_model():
    df = pd.read_csv(os.path.join(BASE_DIR, 'data', 'dataset.csv'))
    
    features = ['cpu_percent', 'memory_percent', 'request_latency_ms', 'error_rate']
    X = df[features]
    y = df['label'] # 1.0 is normal, -1.0 is anomaly
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=50, max_depth=5, random_state=42)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    
    # Train on full data for deployment
    model.fit(X, y)
    
    joblib.dump(model, MODEL_PATH)
    joblib.dump(features, FEATURES_PATH)
    print(f"Model trained successfully. Validation Accuracy: {acc * 100:.2f}%")
    print(f"Model saved to {MODEL_PATH}")

def load_model():
    return joblib.load(MODEL_PATH)

def predict_anomaly(data_dict):
    model = load_model()
    features = joblib.load(FEATURES_PATH)
    
    df = pd.DataFrame([data_dict])
    df = df[features] # ensure ordering
    
    prediction = model.predict(df)[0]
    
    # Get probability for the anomaly class
    classes = list(model.classes_)
    if -1.0 in classes:
        anomaly_idx = classes.index(-1.0)
        score = model.predict_proba(df)[0][anomaly_idx]
    else:
        score = 1.0 if prediction == -1.0 else 0.0
    
    # prediction == -1.0 means anomaly
    return bool(prediction == -1.0), float(score)

def forecast_cpu(cpu_history, steps=5):
    """
    Very simple linear trend forecasting for CPU to demonstrate the capability.
    cpu_history is a list of recent cpu_percent values.
    """
    if len(cpu_history) < 2:
        return [cpu_history[-1]] * steps if cpu_history else [0] * steps
        
    # calculate average delta over the history
    deltas = [cpu_history[i] - cpu_history[i-1] for i in range(1, len(cpu_history))]
    avg_delta = sum(deltas) / len(deltas)
    
    # damp the delta so it doesn't trend to infinity
    damped_delta = avg_delta * 0.5
    
    forecasts = []
    current = cpu_history[-1]
    for _ in range(steps):
        current = current + damped_delta
        # bounded between 0 and 100
        current = max(0, min(100, current))
        forecasts.append(current)
        
    return forecasts

if __name__ == '__main__':
    train_model()
