# 🔐 Automated IDS + Windows Firewall Blocking via Telegram

## 📖 Overview
This project integrates Windows Event Log monitoring with a Telegram bot to automatically block suspicious IP addresses on the Windows firewall.

When the script detects **multiple failed login attempts** (`Event ID 4625`) from the same IP in under 2 minutes, it sends a Telegram alert.  
You can then reply with:

- `block <IP>` → Adds inbound & outbound block rules in Windows Firewall  
- `dismiss <IP>` → Ignores the alert  

---

## ⚙ Requirements
- Python 3.x  
- `pywin32`  
- `Flask`  
- `requests`  
- Windows OS with admin privileges  
- `ngrok` for exposing the webhook  
- A Telegram Bot (via [BotFather](https://t.me/BotFather))  

---

## 🚀 Installation
```bash
pip install pywin32 flask requests
```
### 📡 Setting up the Telegram Webhook
```bash
ngrok http 5000
```
### Then configure the webhook in PowerShell:
```bash
curl.exe -X POST https://api.telegram.org/bot[Telegram Bot API]/setWebhook -d url=[ngrok.app link]/[Telegram bot api]
```
---

## 🛡 Run as Administrator
Both scripts must be executed with elevated privileges:

Script 1: Reads Windows Security logs (requires admin)

Script 2: Modifies firewall rules (requires admin)

---
## 📂 Project Structure
```bash
IDS-IPS.py
webhook.py
```

## 🔍 Workflow
Detection: IDS-IPS.py detects Event ID 4625 (failed logons)

Alert: Sends a Telegram message with IP and reason

Decision: User replies block <IP> or dismiss <IP>

Action: webhook.py reeives telegram response and updates Windows Firewall rules depending on the response
---

## 📸 Example Alert
```vbnet
🚨 Possible risk factor: 192.168.1.45 attempted to authenticate 6 times in 2 minutes.
Would you like to Block this IP or Dismiss the alert?

Format of response:
(Block or Dismiss) (IP)
```






