from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

FIREWALL_URL = "http://localhost:5000/check"
MONITOR_URL = "http://localhost:5002/log"

@app.route("/")
def home():
    return "Switch Service Running"

@app.route("/route", methods=["POST"])
def route_request():
    try:
        headers = {
            "Content-Type": "application/json",
            "X-Forwarded-For": request.headers.get("X-Forwarded-For", "unknown")
        }

        # Step 1: Send to Firewall
        fw_response = requests.post(
            FIREWALL_URL,
            json=request.json,
            headers=headers
        )

        # Step 2: Send to Monitor (log everything)
        requests.post(
            MONITOR_URL,
            json=request.json,
            headers=headers
        )

        return jsonify(fw_response.json()), fw_response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
