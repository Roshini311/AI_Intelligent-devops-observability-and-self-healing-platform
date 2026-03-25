# AI-Driven DevOps Observability & Self-Healing Platform

An intelligent DevOps observability platform combining real-time telemetry ingestion, machine learning-based anomaly detection, predictive failure analysis, and automated self-healing for cloud environments.

## Architecture

1. **Simulated Infrastructure Engine**: Injects dynamic telemetry data (CPU, Memory, Request Latency, Error Rates) mimicking microservices running in a cloud/DevOps environment.
2. **Machine Learning Model (`scikit-learn` Isolation Forest)**: Continuously trained and run against system metrics to detect hidden system anomalies and predict cascading failure states before they disrupt the system.
3. **Observability Backend (`FastAPI`)**: High-performance REST and WebSocket API ingest server. Processes data through the ML model in real-time.
4. **Self-Healing Automation Module**: Triggered strictly when telemetry violates intelligent health degradation thresholds; resolves issues via automated recovery commands.
5. **Real-time Dashboard (`HTML/TailwindCSS/Chart.js`)**: Modern, dark-mode visual interface monitoring the live heartbeat of the infrastructure components.

## Running Locally

1. **Install dependencies**:
   ```bash
   pip install fastapi uvicorn scikit-learn pandas websockets
   ```
2. **Train the initial ML model & generate data**:
   ```bash
   cd backend
   python data_generator.py
   python ml_model.py
   ```
3. **Start the FastAPI backend server**:
   ```bash
   python main.py
   ```
4. **Start the live infrastructure simulator**:
   ```bash
   python simulator.py
   ```
5. **Open the Observability Dashboard**:
   Open `frontend/index.html` in your web browser, or serve it:
   ```bash
   cd frontend
   python -m http.server 3000
   ```
   Navigate to `http://localhost:3000`

## Author
Developed as a prototype implementation for the research paper: *An Intelligent DevOps Observability Platform with Automated Self-Healing Mechanisms for Cloud Infrastructure.*
