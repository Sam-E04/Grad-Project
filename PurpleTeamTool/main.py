import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel
from red import RedTeam
from blue import BlueTeam

class PurpleTeamGUI(QWidget):
    def __init__(self):
        super().__init__()
        
        self.red_team = RedTeam()
        self.blue_team = BlueTeam()

        # Window settings
        self.setWindowTitle("Purple Team Security Tool")
        self.setGeometry(100, 100, 700, 500)
        layout = QVBoxLayout()

        # Attack & Detection Buttons
        self.attack_button = QPushButton("Launch SQL Injection")
        self.attack_button.clicked.connect(self.launch_sql_injection)
        layout.addWidget(self.attack_button)

        self.detect_button = QPushButton("Run Threat Detection")
        self.detect_button.clicked.connect(self.run_threat_detection)
        layout.addWidget(self.detect_button)

        # Log Display
        self.log_output = QTextEdit(self)
        self.log_output.setReadOnly(True)
        layout.addWidget(self.log_output)

        # Set Layout
        self.setLayout(layout)

    def launch_sql_injection(self):
        """Executes an SQL Injection attack & logs output."""
        target = "http://testphp.vulnweb.com"  # Example target
        output = self.red_team.sql_injection(target)
        self.log_output.append(f"[RED TEAM] SQL Injection executed:\n{output}")

    def run_threat_detection(self):
        """Runs Blue Team threat detection & logs results."""
        attack_query = "SELECT * FROM users WHERE username = 'admin' --"
        detection_result = self.blue_team.detect_sql_injection(attack_query)
        self.log_output.append(f"[BLUE TEAM] {detection_result}")

# Run Application
app = QApplication(sys.argv)
window = PurpleTeamGUI()
window.show()
sys.exit(app.exec())
