import json
from typing import List, Dict

def load_logs(file_path: str) -> List[Dict]:
    """Load JSON log files."""
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"[WARNING] File not found: {file_path}")
        return []

def compare_logs(attack_logs: List[Dict], detection_logs: List[Dict]) -> Dict[str, List[Dict]]:
    """Compare attack and detection logs, and categorize outcomes."""
    results = {
        "detected_attacks": [],
        "missed_attacks": [],
        "false_positives": []
    }

    # Track matched detections to identify false positives later
    matched_detections = []

    for attack in attack_logs:
        match = next(
            (detection for detection in detection_logs
             if detection['event_type'] == attack['event_type']
             and detection['target'] == attack['target']
             and detection['source_ip'] == attack['attacker_ip']),
            None
        )

        if match:
            results["detected_attacks"].append({
                "attack": attack,
                "detection": match
            })
            matched_detections.append(match)
        else:
            results["missed_attacks"].append(attack)

    # Detect false positives: detections with no matching attacks
    for detection in detection_logs:
        if detection not in matched_detections:
            results["false_positives"].append(detection)

    return results

def run_purple_team_analysis(attack_log_path: str, detection_log_path: str) -> Dict[str, List[Dict]]:
    """Main function to run purple team analysis."""
    attack_logs = load_logs(attack_log_path)
    detection_logs = load_logs(detection_log_path)

    results = compare_logs(attack_logs, detection_logs)

    return results
