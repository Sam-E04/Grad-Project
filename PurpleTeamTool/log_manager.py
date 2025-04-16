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

def log_attack(attack_type, target, result, attacker_ip="ManualInput"):
    """Logs Red Team attacks."""
    event = create_event(
        event_type=attack_type,
        target=target,
        attacker_ip=attacker_ip,
        details={
            "payload": result,
            "result": result
        }
    )
    log_event(ATTACK_LOG_FILE, event)

def log_detection(threat_type, target, payload, source_ip="ManualInput", action="Blocked"):
    """Logs detections from Blue Team or custom defense."""
    event = create_event(
        event_type=threat_type,
        target=target,
        source_ip=source_ip,
        details={
            "payload": payload,
            "action": action
        }
    )
    log_event(DETECTION_LOG_FILE, event)

def log_request(data, client_ip):
    """Logs raw captured requests."""
    event = create_event(
        event_type="Raw Request",
        target=data.get('url'),
        source_ip=client_ip,
        details={
            "url": data.get('url'),
            "body": data.get('body'),
            "client_ip": client_ip
        }
    )
    log_event(REQUEST_LOG_FILE, event)
    print(f"[DEBUG] Logged request: {event}")

def read_request():
    """Read raw request logs and format as string."""
    try:
        logs = load_logs(REQUEST_LOG_FILE)
        return "\n\n".join(
            [f"[{entry['timestamp']}] IP: {entry.get('source_ip', 'Unknown')}, URL: {entry.get('target', 'Unknown')}, Body: {entry['details'].get('body', 'No Body')}"
             for entry in logs]
        )
    except Exception as e:
        return f"[ERROR] Could not read log: {str(e)}"
