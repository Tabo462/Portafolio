from flask import Flask, request
import requests
import subprocess

TOKEN = "ADD YOUR TELEGRAM BOT TOKEN HERE"
CHAT_ID = "ADD YOUR TELEGRAM CHAT ID HERE"

app = Flask(__name__)

# 📥 Endpoint where the IDS sends the suspicious IP
@app.route(f"/{TOKEN}", methods=["POST"])

def receive_message():
    data = request.get_json()
    
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        message = data["message"]["text"].strip().lower()

        send_alert(f"📩 Message received: {message.capitalize()}")

        if message.startswith("block"):
            ip = message.split()[-1]
            block_ip(ip)
            send_alert(f"✅ Action: IP {ip} blocked on firewall.")
        
        elif message.startswith("dismiss"):
            ip = message.split()[-1]
            send_alert(f"❌ Action: Alert for IP {ip} dismissed.")

    return "OK", 200


def block_ip(ip):
    try:
        subprocess.run(
            ["netsh", "advfirewall", "firewall", "add", "rule",
             f"name=Block_{ip}", "dir=in", "action=block", f"remoteip={ip}"],
            check=True
        )
        subprocess.run(
            ["netsh", "advfirewall", "firewall", "add", "rule",
             f"name=Block_{ip}", "dir=out", "action=block", f"remoteip={ip}"],
            check=True
        )
    except Exception as e:
        send_alert(f"⚠️ Error blocking {ip}: {e}")


def send_alert(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=payload)


if __name__ == "__main__":
    app.run(port=5000)