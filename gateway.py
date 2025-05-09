from flask import Flask, request, jsonify
import requests
import os
import threading
import time

app = Flask(__name__)

PC_PUBLIC_IP = os.getenv("PC_IP")
PC_PORT = os.getenv("PC_PORT")

@app.route("/", methods=["GET"])
def home():
    print("******NORMAL PAGE OPENED******")
    return jsonify({"message": "Shreya Bot Running!!"}), 200

@app.route("/api", methods=["POST"])
def forward_request():
    try:
        data = request.get_json()
        print("******DATA RECIEVED******", data)
        print(f"http://{PC_PUBLIC_IP}:{PC_PORT}/query")
        response = requests.post(f"http://{PC_PUBLIC_IP}:{PC_PORT}/query", json=data)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/ping", methods=["GET"])
def ping():
    print("******PONG******")
    return "Pong!", 200

# Function to keep pinging itself
def keep_alive():
    while True:
        try:
            requests.get("https://shreyabotapi.onrender.com")
            print("Ping sent!")
        except Exception as e:
            print(f"Ping failed: {e}")
        time.sleep(300)

if __name__ == "__main__":
    print("SERVICE STARTED")
    app.run(debug=True)
