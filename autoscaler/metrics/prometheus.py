import requests

PROM_URL = "http://prometheus-kube-prometheus-prometheus.monitoring.svc:9090"

def query(promql):
    r = requests.get(f"{PROM_URL}/api/v1/query", params={"query": promql})
    result = r.json()
    return float(result["data"]["result"][0]["value"][1])

def collect_metrics():
    cpu = query('rate(container_cpu_usage_seconds_total{pod=~"sketchpad-app.*"}[1m])')
    return {"cpu": cpu}