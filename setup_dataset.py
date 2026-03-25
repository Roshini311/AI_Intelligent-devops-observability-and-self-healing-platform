import kagglehub
import shutil
import os
import pandas as pd

print("Downloading dataset...", flush=True)
path = kagglehub.dataset_download("shivanandmn/cloud-infrastructure-anomaly-detection-data")
print("Downloaded to:", path)

target_dir = os.path.join(os.getcwd(), 'backend', 'data')
os.makedirs(target_dir, exist_ok=True)

for file in os.listdir(path):
    if file.endswith('.csv'):
        source_file = os.path.join(path, file)
        target_file = os.path.join(target_dir, 'dataset.csv')
        shutil.copy(source_file, target_file)
        print("Dataset copied to", target_file)
        
        # print first few rows to see features
        df = pd.read_csv(target_file)
        print("\nDataset columns:", df.columns.tolist())
        print("Sample data:\n", df.head(2))
        break
