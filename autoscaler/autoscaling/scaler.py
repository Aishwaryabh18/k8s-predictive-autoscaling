import math

def compute_replicas(predicted_cpu, target_cpu):
    replicas = math.ceil(predicted_cpu / target_cpu)
    return max(1, min(replicas, 5))