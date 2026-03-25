from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import json
import random
import time
from ml_model import predict_anomaly

app = FastAPI(title="DevOps Observability API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TelemetryData(BaseModel):
    cpu_percent: float
    memory_percent: float
    request_latency_ms: float
    error_rate: float

active_connections = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        active_connections.remove(websocket)

async def broadcast_telemetry(data: dict):
    for connection in active_connections:
        await connection.send_text(json.dumps(data))

# System state variables
system_state = {
    "status": "healthy", # healthy, degraded, self_healing
    "uptime": time.time(),
    "last_anomaly": None,
    "recovery_actions": []
}

def self_heal():
    # Simulate an automated self-healing action
    print("Executing self-healing: Restarting dummy service and scaling resources...")
    action = {"time": time.time(), "action": "Restarted specific pod due to high resource usage"}
    system_state["recovery_actions"].append(action)
    system_state["status"] = "healthy"

@app.post("/ingest")
async def ingest_telemetry(data: TelemetryData):
    start_time = time.time()
    data_dict = data.dict()
    
    # Run ML Inference
    is_anomaly, score = predict_anomaly(data_dict)
    
    response_data = {
        "timestamp": time.time(),
        "metrics": data_dict,
        "is_anomaly": is_anomaly,
        "anomaly_score": score,
        "system_status": system_state["status"]
    }
    
    if is_anomaly and system_state["status"] == "healthy":
        system_state["status"] = "degraded"
        system_state["last_anomaly"] = time.time()
        print("Anomaly Detected! State set to degraded.")
        
        # Trigger async self-healing (mock delay)
        asyncio.create_task(trigger_self_healing())
        
    await broadcast_telemetry(response_data)
    
    return {"status": "ok", "inference_time_ms": (time.time() - start_time) * 1000}

async def trigger_self_healing():
    system_state["status"] = "self_healing"
    await broadcast_telemetry({"event": "self_healing_started"})
    await asyncio.sleep(3) # Mock the time to restart a service
    self_heal()
    await broadcast_telemetry({"event": "self_healing_completed", "actions": system_state["recovery_actions"]})

@app.get("/health")
def health_check():
    return system_state

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
