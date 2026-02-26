import time
from metrics.prometheus import collect_metrics
from autoscaling.scaler import compute_replicas
from k8s.client import scale_deployment

# -----------------------------
# CONFIGURATION
# -----------------------------

TARGET_UTILIZATION = 0.15   # Target normalized load
COOLDOWN = 60              # seconds between scaling actions
MIN_REPLICAS = 1
MAX_REPLICAS = 5

last_scaled_time = 0


# -----------------------------
# MULTI-METRIC LOAD FUNCTION
# -----------------------------

def calculate_predicted_load(metrics):
    """
    Combine CPU, Request Rate, and Latency
    into a single normalized load score.
    """

    cpu = metrics["cpu"]                     # already 0–1 range usually
    rps = metrics["rps"] / 200               # normalize approx max 200 rps
    latency = metrics["latency"] / 2         # normalize approx 2s max

    # Weighted multi-metric formula
    predicted_load = (
        0.5 * cpu +
        0.3 * rps +
        0.2 * latency
    )

    return predicted_load


# -----------------------------
# MAIN CONTROL LOOP
# -----------------------------

def main():
    global last_scaled_time

    print("Multi-metric autoscaler started...")

    while True:
        try:
            metrics = collect_metrics()

            predicted_load = calculate_predicted_load(metrics)

            replicas = compute_replicas(
                predicted_load,
                TARGET_UTILIZATION,
                MIN_REPLICAS,
                MAX_REPLICAS
            )

            current_time = time.time()

            if current_time - last_scaled_time > COOLDOWN:
                scale_deployment("sketchpad-app", "default", replicas)

                print(
                    f"[INFO] CPU={metrics['cpu']:.3f}, "
                    f"RPS={metrics['rps']:.2f}, "
                    f"Latency={metrics['latency']:.3f}, "
                    f"PredictedLoad={predicted_load:.3f}, "
                    f"ScalingTo={replicas}"
                )

                last_scaled_time = current_time

        except Exception as e:
            print(f"[ERROR] {e}")

        time.sleep(15)


if __name__ == "__main__":
    main()