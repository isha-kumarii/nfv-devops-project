from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

logs = []

@app.route("/")
def home():
    return "Monitor Service Running"

@app.route("/log", methods=["POST"])
def log_request():
    data = request.json
    ip = request.headers.get("X-Forwarded-For", "unknown")

    entry = {
        "ip": ip,
        "data": data,
        "timestamp": datetime.now().isoformat()
    }

    logs.append(entry)

    print("LOG:", entry)

    return jsonify({"status": "logged"}), 200


@app.route("/logs", methods=["GET"])
def get_logs():
    return jsonify(logs), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
