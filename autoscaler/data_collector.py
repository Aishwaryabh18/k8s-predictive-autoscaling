import requests
import time
import csv

PROM_URL = "http://localhost:9090"

def query(promql):
    r = requests.get(f"{PROM_URL}/api/v1/query", params={"query": promql})
    result = r.json()
    if result["data"]["result"]:
        return float(result["data"]["result"][0]["value"][1])
    return 0.0

with open("metrics.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["cpu", "rps", "latency"])

    while True:
        cpu = query('rate(container_cpu_usage_seconds_total{pod=~"sketchpad-app.*"}[1m])')
        rps = query('rate(http_requests_total{pod=~"sketchpad-app.*"}[1m])')
        latency = query('histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{pod=~"sketchpad-app.*"}[1m]))')

        writer.writerow([cpu, rps, latency])
        print(cpu, rps, latency)

        time.sleep(15)