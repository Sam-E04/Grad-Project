import json
import os
from datetime import datetime

LOG_DIR = "logs"
ATTACK_LOG_FILE = os.path.join(LOG_DIR, "attack_logs.json")
DETECTION_LOG_FILE = os.path.join(LOG_DIR, "detection_logs.json")

# Ensure logs directory exists
os.makedirs(LOG_DIR, exist_ok=True)

def log_event(log_file, event_type, details):
    """Logs events into a JSON file."""
    event_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "event_type": event_type,
        "details": details
    }

    # Load existing logs
    logs = []
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            logs = json.load(f)

    # Append new event
    logs.append(event_entry)

    # Save logs back to file
    with open(log_file, "w") as f:
        json.dump(logs, f, indent=4)

def log_attack(attack_type, target, result):
    """Logs Red Team attacks."""
    log_event(ATTACK_LOG_FILE, attack_type, {"target": target, "result": result})

def log_detection(threat_type, data):
    """Logs Blue Team detections."""
    log_event(DETECTION_LOG_FILE, threat_type, {"detected_input": data, "action": "Blocked"})
