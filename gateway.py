from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from urllib.parse import urlparse
import requests
import threading
import time
import os
import json
import random

app = Flask(__name__)
app.secret_key = "alphaflowerHukaLalaHurr121928gwigybi"
ngrok_link = ""
SECRET_KEY = "alphaflowerHukaLalaHurr121928gwigybi"

@app.route("/receive_ngrok_link", methods=["POST"])
def receive_link():
    global ngrok_link

    auth_key = request.headers.get("Authorization")
    if auth_key != SECRET_KEY:
        return {"status": "error", "message": "Unauthorized"}, 403  # Reject if key is incorrect

    data = request.get_json()
    ngrok_link = data.get("ngrok_link", "")
    print(f"Received Ngrok Link: {ngrok_link}")
    return {"status": "success", "received_link": ngrok_link}


@app.route("/", methods=["GET"])
def home():
    print("******NORMAL PAGE OPENED******")
    return jsonify({"message": "IndPak Running!!"}), 200

@app.route("/api", methods=["POST"])
def forward_request():
    try:
        data = request.get_json()
        if not data or "text" not in data:
            return jsonify({"error": "Missing 'text' field"}), 400

        print("******DATA RECEIVED******", data)

        response = requests.post(
            f"{ngrok_link}/query",
            json={"text": data["text"]},
            headers={
                "ngrok-skip-browser-warning": "true",
                "Content-Type": "application/json"
            }
        )

        return (response.text, response.status_code, response.headers.items())

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/a/<path:link>", methods=["GET"])
def forward_via_path(link):
    try:
        print("******PATH RECEIVED******", link)
        
        # Prepend https:// if not present
        full_link = link if link.startswith("http") else f"https://{link}"
        
        # Parse and remove query parameters
        parsed_url = urlparse(full_link)
        cleaned_link = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"

        print("******CLEANED LINK******", cleaned_link)

        response = requests.post(
            f"{ngrok_link}/query",
            json={"text": cleaned_link},
            headers={
                "ngrok-skip-browser-warning": "true",
                "Content-Type": "application/json"
            }
        )

        return (response.text, response.status_code, response.headers.items())

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/ping")
def ping():
    global ngrok_link 
    status_message = "IndPak link - Online\n"
    api_url = f"{ngrok_link}/ping" if ngrok_link else None
    api_status = "Offline"

    if api_url:
        try:
            response = requests.get(api_url, timeout=5)  # 5s timeout
            if response.status_code == 200 and response.text.strip() == "Pong!":
                api_status = "Online"
        except requests.exceptions.RequestException:
            api_status = "Offline"

    status_message += f"IndPak API - {api_status}"

    return status_message, 200
@app.route("/change_link")
def clink():
    api_url = f"{ngrok_link}/change_link" if ngrok_link else None
    requests.get(api_url)
    return jsonify({"message": f"IndPak Rrunning at {ngrok_link}"}), 200


@app.route("/whatislink")
def wil():
    return ngrok_link   
def keep_alive():
    while True:
        try:
            requests.get("https://indpak.onrender.com")
            print("Ping sent!")
        except Exception as e:
            print(f"Ping failed: {e}")
        time.sleep(300)    
if __name__ == "__main__":
    print("SERVICE STARTED")
    app.run(debug=True)
