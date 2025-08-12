import win32evtlog
import requests
from collections import defaultdict, deque
from datetime import timedelta
import time


MAX_EVENTS = 30
MAX_TIME = timedelta(minutes=2)
ATTEMPT_THRESHOLD = 5

TOKEN = "ADD YOUR TELEGRAM BOT TOKEN HERE"
CHAT_ID = "ADD YOUR TELEGRAM CHAT ID HERE"

attempts_per_ip = defaultdict(lambda: deque(maxlen=MAX_EVENTS))
alerted_ips = set()

server = 'localhost'
log_type = 'Security'

hand = win32evtlog.OpenEventLog(server, log_type)
flags = win32evtlog.EVENTLOG_SEQUENTIAL_READ | win32evtlog.EVENTLOG_FORWARDS_READ 

NTLM_ERROR_CODES = {
    "0xc000006a": "STATUS_WRONG_PASSWORD - Incorrect password.",
    "0xc0000064": "STATUS_NO_SUCH_USER - User does not exist.",
    "0xc0000234": "STATUS_ACCOUNT_LOCKED_OUT - Account locked.",
    "0xc0000070": "STATUS_INVALID_LOGON_HOURS - Attempt outside permitted hours.",
    "0xc0000071": "STATUS_PASSWORD_EXPIRED - Password expired.",
    "0xc0000193": "STATUS_ACCOUNT_EXPIRED - Account expired.",
    "0xc0000225": "STATUS_NOT_FOUND - No logon rights.",
    "0xc000015b": "STATUS_LOGON_TYPE_NOT_GRANTED - Logon type not allowed.",
    "0xc000006d": "STATUS_LOGON_FAILURE - Generic logon failure (invalid user or password)."
}

def send_alert(mensaje):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensaje}
    requests.post(url, data=payload)

def interpret_ntlm_code(hex_code):
    return NTLM_ERROR_CODES.get(hex_code.lower(), "Unknown code")

def register_event(ip, event_time):
    attempts_per_ip[ip].append(event_time)
    now = event_time
    recent_events = [f for f in attempts_per_ip[ip] if now - f <= MAX_TIME]
    if len(recent_events) >= ATTEMPT_THRESHOLD:
        if ip not in alerted_ips:
            send_alert(f"🚨 Possible risk factor: {ip} attempted to authenticate {len(recent_events)} times in 2 minutes.\n"
                       "Would you like to Block this IP or Dismiss the alert?\n"
                       "Format of response:\n"
                       "(Block or Dismiss) (IP)")
            alerted_ips.add(ip)

print("📡 Monitoring failed login attempts (ID 4625)...\n")

last_record = 0 

while True:
    events = win32evtlog.ReadEventLog(hand, flags, 0)
    if not events:
        time.sleep(130)  
        continue

    for event in events:
        if event.RecordNumber <= last_record:
            continue 

        last_record = event.RecordNumber

        if event.EventID == 4625:
            try:
                inserts = event.StringInserts
                user = inserts[5]
                domain = inserts[6]
                ip_address = inserts[19]
                if ip_address == "-" or ip_address == "127.0.0.1":
                    continue
                reason = interpret_ntlm_code(inserts[9])
                print(f"[{event.TimeGenerated}] User: {user} | Domain: {domain} | IP: {ip_address} | Reason: {reason}")
                register_event(ip_address, event.TimeGenerated)
            except Exception as e:
                print(f"Error extracting event details: {e}")