import requests
import os
import json

LOG_DEST = "logs/detection_logs.json"
REMOTE_API = "http://192.168.8.133:5001/get_detection_logs"  # Ubuntu IP

def update_detection_logs():
    try:
        response = requests.get(REMOTE_API)
        response.raise_for_status()
        with open(LOG_DEST, "w") as f:
            f.write(response.text)
        print(f"[+] Logs updated from {REMOTE_API}")
    except Exception as e:
        print(f"[-] Failed to fetch detection logs: {e}")

update_detection_logs()