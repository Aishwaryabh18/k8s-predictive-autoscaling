from flask import Flask, render_template_string
import time
import random
from prometheus_client import Counter, Histogram, generate_latest,  CONTENT_TYPE_LATEST

app = Flask(__name__)

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP Requests"
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP Request Latency"
)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Simple Sketchpad App</title>
</head>
<body>
    <h1>Welcome to Sketchpad App</h1>
    <p>This is a simple workload application.</p>
</body>
</html>
"""

@app.route("/")
def home():
    start = time.time()

    # simulate processing delay
    time.sleep(random.uniform(0.05, 0.2))

    REQUEST_COUNT.inc()
    REQUEST_LATENCY.observe(time.time() - start)

    return render_template_string(HTML_PAGE)

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {
        "Content-Type": CONTENT_TYPE_LATEST # commit: updating content type to text/plain 
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)