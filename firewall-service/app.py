from flask import Flask, request, jsonify

app = Flask(__name__)

# Simulated blacklist
BLOCKED_IPS = ["192.168.1.10", "10.0.0.1"]

# Simple malicious patterns
BLOCKED_KEYWORDS = ["DROP", "malicious", "attack"]

@app.route("/")
def home():
    return "Firewall Service Running"

@app.route("/check", methods=["POST"])
def firewall_check():
    data = request.json
    ip = request.headers.get("X-Forwarded-For", "unknown")
    content = str(data)

    # Check IP
    if ip in BLOCKED_IPS:
        return jsonify({"status": "blocked", "reason": "IP blocked"}), 403

    # Check malicious content
    for keyword in BLOCKED_KEYWORDS:
        if keyword.lower() in content.lower():
            return jsonify({"status": "blocked", "reason": "malicious content"}), 403

    return jsonify({"status": "allowed"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
