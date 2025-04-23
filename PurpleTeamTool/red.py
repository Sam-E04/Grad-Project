import subprocess
from log_manager import log_attack

class RedTeam:

    def run_payload(self, command, name):
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
                log_attack(name, "172.26.204.72", command, simplified_output)
            return simplified_output

        except Exception as e:
            return f"[ERROR] {str(e)}"


    def sqli_basic(self):
        payload = 'curl -i "http://172.26.204.72/index.html?user=admin%27%20OR%201%3D1--"'
        return self.run_payload(payload, "SQLi")

    def xss_basic(self):
        payload = 'curl -i "http://172.26.204.72/index.html?q=<script>alert(\'XSS\')</script>"'
        return self.run_payload(payload, "XSS")

    def command_injection(self):
        payload = 'curl -i -X POST "http://172.26.204.72/login" -d "username=admin;phpinfo();" -A "curl"'
        return self.run_payload(payload, "CMDi")

    def lfi_basic(self):
        payload = 'curl -i "http://172.26.204.72/index.html?page=../../../../etc/passwd"'
        return self.run_payload(payload, "LFI")

    def false_positive(self):
        payload = 'curl -i "http://172.26.204.72/index.html?contact=%22+SELECT+FROM+help"'
        return self.run_payload(payload, "False Positive")

red_team = RedTeam()
