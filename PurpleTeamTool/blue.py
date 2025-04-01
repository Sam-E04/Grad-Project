import re
import subprocess
from flask import Flask, request, jsonify
from log_manager import log_detection
import threading

GUI_CALLBACK = None

class BlueTeam:
    def __init__(self, gui_callback=None):
        global GUI_CALLBACK
        GUI_CALLBACK = gui_callback  # GUI updates
        self.gui_callback = gui_callback  # GUI updates
        self.app = Flask(__name__)
        self.setup_routes()
        
        # Start Flask server in a separate thread
        self.server_thread = threading.Thread(target=self.run_flask, daemon=True)
        self.server_thread.start()

    def capture_request(self):
                print("Received request at /capture")  # Debugging print
                data = request.get_json()
                
                if not data:
                    print("Error: No JSON data received!")
                elif 'url' not in data or 'body' not in data:
                    print(f"Error: Missing keys in JSON: {data}")

                if not data or 'url' not in data or 'body' not in data:
                    return jsonify({"error": "Invalid request format"}), 400

                print(f"Valid data received: {data}")  # Debugging print

                class Flow:
                    class Request:
                        def __init__(self, url, body):
                            self.pretty_url = url
                            self.body = body
                        
                        def get_text(self):
                            return self.body

                    class ClientConn:
                        address = (request.remote_addr, 0)

                    def __init__(self, url, body):
                        self.request = self.Request(url, body)
                        self.client_conn = self.ClientConn()

                flow = Flow(data['url'], data['body'])
                self.detect_attack(flow)
                return jsonify({"status": "processed"})

    def setup_routes(self):
        """Defines API routes for receiving HTTP requests."""
        
        # @self.app.route('/capture', methods=['POST'])
        self.app.add_url_rule('/capture', 'capture_request', self.capture_request, methods=['POST'])
        
    def run_flask(self):
        """Runs Flask server on a separate thread."""
        self.app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)

    def detect_attack(self, flow):
        """Detects web-based attacks by inspecting request content."""
        global GUI_CALLBACK
        self.gui_callback = GUI_CALLBACK
        request_data = flow.request.get_text()
        
        # Send all received requests to the GUI for manual review
        if self.gui_callback:
            self.gui_callback(f"[TRAFFIC] {flow.request.pretty_url} - {request_data}")

        # Detection rules
        sqli_pattern = r"('|\"|`|\bUNION\b|\bSELECT\b|\bDROP\b|\bINSERT\b|\bDELETE\b)"
        xss_pattern = r"(<script>|onerror=|javascript:|alert\()"
        rce_pattern = r"(;|&&|\||\bcat\b|\bping\b|\bwget\b|\bcurl\b|\brm -rf\b)"

        detected_threat = None
        if re.search(sqli_pattern, request_data, re.IGNORECASE):
            detected_threat = "SQL Injection"
        elif re.search(xss_pattern, request_data, re.IGNORECASE):
            detected_threat = "XSS Attack"
        elif re.search(rce_pattern, request_data, re.IGNORECASE):
            detected_threat = "RCE Attack"

        if detected_threat:
            log_detection(detected_threat, flow.request.pretty_url, request_data)

            # Send only alerts to the GUI alert section
            if self.gui_callback:
                self.gui_callback(f"[ALERT] {detected_threat} detected on {flow.request.pretty_url}")



# Ensure Flask server starts when BlueTeam is initialized
blue_team = BlueTeam()
