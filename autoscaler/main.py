import time
from metrics.prometheus import collect_metrics
from autoscaling.scaler import compute_replicas
from k8s.client import scale_deployment

TARGET_CPU = 0.1

while True:
    metrics = collect_metrics()
    predicted_cpu = metrics["cpu"]  # temporary (replace with LSTM later)

    replicas = compute_replicas(predicted_cpu, TARGET_CPU)

    scale_deployment("sketchpad-app", "default", replicas)

    time.sleep(15)