from flask import Flask, request, jsonify

app = Flask(__name__)

blocked_ips = ["192.168.1.10", "10.0.0.1"]
blocked_keywords = ["DROP", "malicious", "attack"]


@app.route("/")
def home():
    return "Firewall Service Running"


@app.route("/check", methods=["POST"])
def firewall_check():
    data = request.json
    ip = request.headers.get("X-Forwarded-For", "unknown")
    content = str(data)

    if ip in blocked_ips:
        return jsonify({"status": "blocked", "reason": "IP blocked"}), 403

    for keyword in blocked_keywords:
        if keyword.lower() in content.lower():
            return jsonify({"status": "blocked", "reason": "malicious content"}), 403

    return jsonify({"status": "allowed"}), 200


@app.route("/rules", methods=["GET"])
def get_rules():
    return jsonify({"blocked_ips": blocked_ips, "blocked_keywords": blocked_keywords}), 200


@app.route("/rules/ip", methods=["POST"])
def manage_ip():
    data = request.json
    action = data.get("action")
    ip = data.get("ip")

    if not action or not ip:
        return jsonify({"error": "provide 'action' (add/remove) and 'ip'"}), 400

    if action == "add":
        if ip not in blocked_ips:
            blocked_ips.append(ip)
        return jsonify({"message": f"{ip} added to blacklist"}), 200
    elif action == "remove":
        if ip in blocked_ips:
            blocked_ips.remove(ip)
        return jsonify({"message": f"{ip} removed from blacklist"}), 200
    else:
        return jsonify({"error": "action must be 'add' or 'remove'"}), 400


@app.route("/rules/keyword", methods=["POST"])
def manage_keyword():
    data = request.json
    action = data.get("action")
    keyword = data.get("keyword")

    if not action or not keyword:
        return jsonify({"error": "provide 'action' (add/remove) and 'keyword'"}), 400

    if action == "add":
        if keyword not in blocked_keywords:
            blocked_keywords.append(keyword)
        return jsonify({"message": f"'{keyword}' added to blocked keywords"}), 200
    elif action == "remove":
        if keyword in blocked_keywords:
            blocked_keywords.remove(keyword)
        return jsonify({"message": f"'{keyword}' removed from blocked keywords"}), 200
    else:
        return jsonify({"error": "action must be 'add' or 'remove'"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)











