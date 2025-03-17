import sys
import json
import datetime
from PyQt6.QtWidgets import (
    QApplication, QLabel, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLineEdit, QTabWidget
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl
import requests
from red import RedTeam
from blue import BlueTeam
from log_manager import log_attack

class PurpleTeamGUI(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize Red & Blue Team modules
        self.red_team = RedTeam()
        self.blue_team = BlueTeam()

        # Window settings
        self.setWindowTitle("Purple Team Security Tool")
        self.setGeometry(100, 100, 900, 600)

        # Create Tabs
        self.tabs = QTabWidget()
        self.red_team_tab = QWidget()
        self.blue_team_tab = QWidget()
        self.custom_attack_tab = QWidget()  # New tab for manual attacks

        # Add tabs
        self.tabs.addTab(self.red_team_tab, "Red Team (Attack)")
        self.tabs.addTab(self.blue_team_tab, "Blue Team (Defense)")
        self.tabs.addTab(self.custom_attack_tab, "Custom Attacks")  # New

        # Initialize tab layouts
        self.init_red_team_ui()
        self.init_blue_team_ui()
        self.init_custom_attack_ui()  # New

        # Set layout
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        self.setLayout(layout)

    ## ------------------ RED TEAM UI ------------------ ##
    def init_red_team_ui(self):
        """Sets up the Red Team (Attack) UI"""
        layout = QVBoxLayout()

        # Attack Buttons
        self.sqli_attack_button = QPushButton("Launch SQL Injection")
        self.sqli_attack_button.clicked.connect(self.launch_sql_injection)
        layout.addWidget(self.sqli_attack_button)

        self.xss_attack_button = QPushButton("Launch XSS Attack")
        self.xss_attack_button.clicked.connect(self.launch_xss_attack)
        layout.addWidget(self.xss_attack_button)

        self.rce_attack_button = QPushButton("Launch RCE Attack")
        self.rce_attack_button.clicked.connect(self.launch_rce_attack)
        layout.addWidget(self.rce_attack_button)

        # Log Display
        self.red_team_log = QTextEdit(self)
        self.red_team_log.setReadOnly(True)
        layout.addWidget(self.red_team_log)

        self.red_team_tab.setLayout(layout)

    ## ------------------ BLUE TEAM UI ------------------ ##
    def init_blue_team_ui(self):
        """Sets up the Blue Team (Defense) UI"""
        layout = QVBoxLayout()

        # Detection Buttons
        self.sqli_detect_button = QPushButton("Detect SQL Injection")
        self.sqli_detect_button.clicked.connect(self.detect_sql_injection)
        layout.addWidget(self.sqli_detect_button)

        self.xss_detect_button = QPushButton("Detect XSS Attack")
        self.xss_detect_button.clicked.connect(self.detect_xss)
        layout.addWidget(self.xss_detect_button)

        self.rce_detect_button = QPushButton("Detect RCE Attack")
        self.rce_detect_button.clicked.connect(self.detect_rce)
        layout.addWidget(self.rce_detect_button)

        # Log Display
        self.blue_team_log = QTextEdit(self)
        self.blue_team_log.setReadOnly(True)
        layout.addWidget(self.blue_team_log)

        self.blue_team_tab.setLayout(layout)

    ## ------------------ CUSTOM ATTACK UI ------------------ ##
    def init_custom_attack_ui(self):
        """Sets up the Custom Attack UI where users can manually enter attack payloads."""
        layout = QVBoxLayout()

        # Web Browser to Load Target Website
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://testphp.vulnweb.com"))  # Default page
        layout.addWidget(self.browser)

        # Input Field for Custom Attack
        self.attack_input = QLineEdit()
        self.attack_input.setPlaceholderText("Enter your custom attack payload here...")
        layout.addWidget(self.attack_input)

        # Send Attack Button
        self.send_attack_button = QPushButton("Send Attack")
        self.send_attack_button.clicked.connect(self.send_custom_attack)
        layout.addWidget(self.send_attack_button)

        # Custom Attack Log
        self.custom_attack_log = QTextEdit()
        self.custom_attack_log.setReadOnly(True)
        layout.addWidget(self.custom_attack_log)

        self.custom_attack_tab.setLayout(layout)

    ## ------------------ RED TEAM ATTACK FUNCTIONS ------------------ ##
    def launch_sql_injection(self):
        """Executes an SQL Injection attack & logs output."""
        target = "http://testphp.vulnweb.com"
        output = self.red_team.sql_injection(target)
        self.red_team_log.append(f"[RED TEAM] SQL Injection executed:\n{output}")

    def launch_xss_attack(self):
        """Executes an XSS attack & logs output."""
        target = "http://testphp.vulnweb.com"
        output = self.red_team.xss_attack(target)
        self.red_team_log.append(f"[RED TEAM] XSS Attack executed:\n{output}")

    def launch_rce_attack(self):
        """Executes an RCE attack & logs output."""
        command = "whoami"
        output = self.red_team.rce_attack(command)
        self.red_team_log.append(f"[RED TEAM] RCE executed:\n{output}")

    ## ------------------ BLUE TEAM DETECTION FUNCTIONS ------------------ ##
    def detect_sql_injection(self):
        """Runs Blue Team threat detection for SQL Injection."""
        query = "SELECT * FROM users WHERE username = 'admin' --"
        detection_result = self.blue_team.detect_sql_injection(query)
        self.blue_team_log.append(f"[BLUE TEAM] {detection_result}")

    def detect_xss(self):
        """Runs Blue Team threat detection for XSS."""
        payload = "<script>alert('XSS')</script>"
        detection_result = self.blue_team.detect_xss(payload)
        self.blue_team_log.append(f"[BLUE TEAM] {detection_result}")

    def detect_rce(self):
        """Runs Blue Team threat detection for RCE."""
        command = "rm -rf /"
        detection_result = self.blue_team.detect_rce(command)
        self.blue_team_log.append(f"[BLUE TEAM] {detection_result}")

    ## ------------------ CUSTOM ATTACK UI ------------------ ##
    def init_custom_attack_ui(self):
        """Sets up the Custom Attack UI where users manually input attack logs."""
        layout = QVBoxLayout()

        # Web Browser for User to Perform Attacks
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://testphp.vulnweb.com"))  # Default page
        layout.addWidget(self.browser)

        # Input Fields for Manual Log Entry
        self.log_type_label = QLabel("Attack Type (SQLi, XSS, RCE):")
        layout.addWidget(self.log_type_label)
        self.log_type_input = QLineEdit()
        layout.addWidget(self.log_type_input)

        self.target_label = QLabel("Target URL:")
        layout.addWidget(self.target_label)
        self.target_input = QLineEdit()
        layout.addWidget(self.target_input)

        self.details_label = QLabel("Attack Details:")
        layout.addWidget(self.details_label)
        self.details_input = QTextEdit()
        layout.addWidget(self.details_input)

        # Button to Log the Attack
        self.log_attack_button = QPushButton("Log Attack")
        self.log_attack_button.clicked.connect(self.log_manual_attack)
        layout.addWidget(self.log_attack_button)

        # Log Display
        self.custom_attack_log = QTextEdit()
        self.custom_attack_log.setReadOnly(True)
        layout.addWidget(self.custom_attack_log)

        self.custom_attack_tab.setLayout(layout)

    ## ------------------ CUSTOM ATTACK LOGGING FUNCTION ------------------ ##
    def log_manual_attack(self):
        """Logs a manually entered attack in JSON format."""
        attack_type = self.log_type_input.text().strip()
        target = self.target_input.text().strip()
        details = self.details_input.toPlainText().strip()

        if not attack_type or not target or not details:
            self.custom_attack_log.append("[ERROR] All fields must be filled out.")
            return

        # Append log entry to JSON file
        try:
            log_attack(attack_type, target, details)
            self.custom_attack_log.append(f"[LOGGED] {attack_type} attack on {target}")
        except Exception as e:
            self.custom_attack_log.append(f"[ERROR] Failed to write log: {str(e)}")


# Run Application
app = QApplication(sys.argv)
window = PurpleTeamGUI()
window.show()
sys.exit(app.exec())
