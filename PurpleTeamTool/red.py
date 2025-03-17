import subprocess
import requests
from log_manager import log_attack

class RedTeam:
    def sql_injection(self, target_url):
        """Launches SQL Injection on the target website."""
        command = f"sqlmap -u {target_url} --batch --dbs --forms --crawl=2"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        log_attack("SQL Injection", target_url, result)
        return result

    def xss_attack(self, target_url):
        """Uses XSStrike to specifically test the vulnerable search parameter."""
        try:
            # Explicitly test the "search" parameter
            command = (
                f"xsstrike -u \"{target_url}?search=XSS\" --params --fuzzer "
                f"--headers \"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\""
            )
            result = subprocess.run(command, shell=True, capture_output=True, text=True)

            log_attack("XSS", target_url, result.stdout)
            return result.stdout if result.stdout else "[FAILED] No XSS vulnerabilities found."

        except Exception as e:
            return f"[ERROR] {str(e)}"

    def rce_attack(self, command):
        """Attempts Remote Code Execution (RCE)"""
        dangerous_commands = ["rm -rf", "shutdown", "wget", "curl"]
        if any(cmd in command for cmd in dangerous_commands):
            return "[ERROR] Dangerous command blocked."

        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        log_attack("RCE", "Local System", result)
        return result
