import time
import numpy as np
import torch
from metrics.prometheus import collect_metrics
from autoscaling.scaler import compute_replicas
from k8s.client import scale_deployment
from models.lstm_model import LSTMModel

WINDOW = 10
TARGET = 0.5
COOLDOWN = 60

sequence = []
last_scaled = 0

model = LSTMModel()
model.load_state_dict(torch.load("lstm.pt"))
model.eval()

while True:
    metrics = collect_metrics()

    input_vector = np.array([
        metrics["cpu"],
        metrics["rps"] / 200,
        metrics["latency"] / 2
    ])

    sequence.append(input_vector)

    if len(sequence) >= WINDOW:
        input_seq = torch.tensor(
            np.array(sequence[-WINDOW:])
        ).float().unsqueeze(0)

        with torch.no_grad():
            predicted_cpu = model(input_seq).item()

        replicas = compute_replicas(predicted_cpu, TARGET, 1, 5)

        now = time.time()
        if now - last_scaled > COOLDOWN:
            scale_deployment("sketchpad-app", "default", replicas)
            print(f"Predicted CPU: {predicted_cpu}, Scaling to {replicas}")
            last_scaled = now

    time.sleep(15)