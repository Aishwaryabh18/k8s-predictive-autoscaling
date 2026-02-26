import numpy as np

def preprocess(metrics):
    cpu = metrics["cpu"]
    rps = metrics["rps"]
    latency = metrics["latency"]

    # simple normalization
    cpu_n = cpu
    rps_n = rps / 200
    latency_n = latency / 2

    return np.array([cpu_n, rps_n, latency_n])