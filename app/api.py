import random, time

from flask import Flask,jsonify
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)


##---MÉTRICAS
login_failures = Counter(
    "login_failures_total",
    "Total failed login attempts"
)

login_latency= Histogram(
    "login_latency_seconds",
    "Login latency in seconds"
)

login_requests_total = Counter(
    "login_requests_total",
    "Total login requests"
)

#---ROTAS

@app.route("/healthz")
def health():
    return jsonify({"status":"ok"}), 200

@app.route("/metrics")
def metrics():
    data = generate_latest()
    return data, 200, {"Content-Type": CONTENT_TYPE_LATEST}

@app.route("/login")
def login():
    start_time = time.time()
    login_requests_total.inc()
    time.sleep(random.uniform(0.05, 0.3))

    if random.random() < 0.3:
        login_failures.inc()
        elapsed = time.time() - start_time
        login_latency.observe(elapsed)
        return jsonify({"status":"fail"}), 401
    
    elapsed = time.time() - start_time
    login_latency.observe(elapsed)
    return jsonify({"status":"ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)