import requests

PROM_URL = "http://prometheus-kube-prometheus-prometheus.monitoring.svc:9090"

def query(promql):
    r = requests.get(f"{PROM_URL}/api/v1/query", params={"query": promql})
    result = r.json()

    if result["data"]["result"]:
        return float(result["data"]["result"][0]["value"][1])
    return 0.0

def collect_metrics():
    cpu = query('rate(container_cpu_usage_seconds_total{pod=~"sketchpad-app.*"}[1m])')
    rps = query('rate(http_requests_total{pod=~"sketchpad-app.*"}[1m])')
    latency = query('histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{pod=~"sketchpad-app.*"}[1m]))')

    return {
        "cpu": cpu,
        "rps": rps,
        "latency": latency
    }