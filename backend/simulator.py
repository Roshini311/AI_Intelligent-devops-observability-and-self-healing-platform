import requests
import time
import random

API_URL = "http://localhost:8000/ingest"

def simulate_realtime_data():
    anomaly_probability = 0.05
    
    print("Starting real-time simulator. Press Ctrl+C to stop.")
    
    while True:
        # Base healthy metrics
        cpu = random.uniform(20, 40)
        mem = random.uniform(30, 50)
        latency = random.uniform(20, 80)
        err = random.uniform(0.001, 0.01)
        
        # Inject occasional anomaly
        if random.random() < anomaly_probability:
            print("--- INJECTING ANOMALY ---")
            anomaly_type = random.choice(['cpu', 'mem', 'latency'])
            if anomaly_type == 'cpu':
                cpu = random.uniform(85, 100)
            elif anomaly_type == 'mem':
                mem = random.uniform(90, 100)
            else:
                latency = random.uniform(1000, 2000)
                err = random.uniform(0.1, 0.3)
                
        payload = {
            "cpu_percent": cpu,
            "memory_percent": mem,
            "request_latency_ms": latency,
            "error_rate": err
        }
        
        try:
            requests.post(API_URL, json=payload)
        except requests.exceptions.ConnectionError:
            print("API not available. Retrying...")
            
        time.sleep(2)

if __name__ == "__main__":
    simulate_realtime_data()
