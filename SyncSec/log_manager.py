import json
import os
from datetime import datetime

# Log directory and files
LOG_DIR = "../logs"
ATTACK_LOG_FILE = os.path.join(LOG_DIR, "attack_logs.json")
DETECTION_LOG_FILE = os.path.join(LOG_DIR, "detection_logs.json")
REQUEST_LOG_FILE = os.path.join(LOG_DIR, "request_logs.json")

# Ensure logs directory exists
os.makedirs(LOG_DIR, exist_ok=True)

def load_logs(log_file):
    """Safely load logs from a file."""
    if os.path.exists(log_file):
        try:
            with open(log_file, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            print(f"[WARNING] Log file corrupted or empty: {log_file}")
            return []
    return []

def save_logs(log_file, logs):
    """Save logs to a file with indentation."""
    with open(log_file, "w") as f:
        json.dump(logs, f, indent=4)

def log_event(log_file, event_data):
    """Logs events into a JSON file."""
    logs = load_logs(log_file)
    logs.append(event_data)
    save_logs(log_file, logs)

def create_event(event_type, target=None, attacker_ip=None, source_ip=None, details=None):
    """Standardized event format."""
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "event_type": event_type,
        "target": target,
        "attacker_ip": attacker_ip,
        "source_ip": source_ip,
        "details": details or {}
    }

def log_attack(attack_type, target, payload, result, attacker_ip="172.24.224.1"):
    """Logs Red Team attacks."""
    event = create_event(
        event_type=attack_type,
        target=target,
        attacker_ip=attacker_ip,
        details={
            "payload": payload,
            "result": result
        }
    )
    log_event(ATTACK_LOG_FILE, event)
