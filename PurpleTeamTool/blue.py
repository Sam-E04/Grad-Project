from log_manager import log_detection

class BlueTeam:
    def detect_sql_injection(self, query):
        """Detects SQL Injection based on common attack patterns."""
        sql_keywords = ["SELECT", "DROP", "INSERT", "DELETE", "--", "' OR '1'='1"]

        if any(keyword in query.upper() for keyword in sql_keywords):
            log_detection("SQL Injection", query)
            return f"[DETECTED] SQL Injection: {query} (Blocked)"

        return "[SAFE] No SQL Injection detected."

    def detect_xss(self, payload):
        """Detects Cross-Site Scripting (XSS) patterns."""
        xss_patterns = ["<script>", "onerror=", "javascript:", "alert("]

        if any(pattern in payload.lower() for pattern in xss_patterns):
            log_detection("XSS", payload)
            return f"[DETECTED] XSS Attack: {payload} (Blocked)"

        return "[SAFE] No XSS detected."

    def detect_rce(self, command):
        """Detects possible Remote Code Execution (RCE) attempts."""
        dangerous_commands = ["rm -rf", "wget ", "curl ", ";", "|", "&&"]

        if any(cmd in command.lower() for cmd in dangerous_commands):
            log_detection("RCE", command)
            return f"[DETECTED] RCE Attempt: {command} (Blocked)"

        return "[SAFE] No RCE detected."
