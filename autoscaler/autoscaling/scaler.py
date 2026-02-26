import math

def compute_replicas(predicted_load, target, min_replicas, max_replicas):
    """
    Compute desired replicas based on predicted load.
    """

    replicas = math.ceil(predicted_load / target)

    replicas = max(min_replicas, replicas)
    replicas = min(max_replicas, replicas)

    return replicas