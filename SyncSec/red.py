import subprocess
from log_manager import log_attack

def run_payload(command, name, target_ip):
    """Runs a curl-based payload, captures HTTP status and filters output for logging."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        full_output = result.stdout + "\n" + result.stderr

        # Extract lines that include HTTP info or common status indicators
        simplified_lines = []
        for line in full_output.splitlines():
            line = line.strip()
            if any(keyword in line.lower() for keyword in [
                "http", "status", "403", "200", "500", "not found", "forbidden",
                "modsecurity", "error", "alert", "access denied"
            ]):
                simplified_lines.append(line)

        simplified_output = "\n".join(simplified_lines) or "[INFO] No meaningful output found."

        if name != "False Positive":
            log_attack(name, target_ip, command, simplified_output)
        return simplified_output

    except Exception as e:
        return f"[ERROR] {str(e)}"

