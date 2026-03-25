import pandas as pd
import numpy as np
import os

def generate_data(num_samples=2000):
    np.random.seed(42)
    
    # Normal behavior
    cpu = np.random.normal(30, 10, num_samples) # Mean 30%, std 10%
    mem = np.random.normal(40, 15, num_samples) # Mean 40%, std 15%
    latency = np.random.normal(50, 20, num_samples) # 50ms
    error_rate = np.random.exponential(0.01, num_samples)
    
    # Clip normal values to proper bounds
    cpu = np.clip(cpu, 1, 99)
    mem = np.clip(mem, 5, 99)
    latency = np.clip(latency, 10, 500)
    error_rate = np.clip(error_rate, 0, 1)

    labels = np.ones(num_samples) # 1 = normal

    # Inject Anomalies (approx 10%)
    num_anomalies = int(num_samples * 0.1)
    anomaly_indices = np.random.choice(num_samples, num_anomalies, replace=False)
    
    for idx in anomaly_indices:
        anomaly_type = np.random.choice(['high_cpu', 'memory_leak', 'high_latency'])
        if anomaly_type == 'high_cpu':
            cpu[idx] = np.random.uniform(85, 100)
        elif anomaly_type == 'memory_leak':
            mem[idx] = np.random.uniform(90, 100)
        elif anomaly_type == 'high_latency':
            latency[idx] = np.random.uniform(500, 2000)
            error_rate[idx] = np.random.uniform(0.1, 0.5)
        
        labels[idx] = -1 # -1 = anomaly

    df = pd.DataFrame({
        'cpu_percent': cpu,
        'memory_percent': mem,
        'request_latency_ms': latency,
        'error_rate': error_rate,
        'label': labels
    })
    
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    os.makedirs(data_dir, exist_ok=True)
    df.to_csv(os.path.join(data_dir, 'dataset.csv'), index=False)
    print(f"Generated {num_samples} samples with {num_anomalies} anomalies.")

if __name__ == '__main__':
    generate_data()
